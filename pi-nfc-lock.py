import csv
import logging
import time
import atexit
import sys
import signal
import hashlib
import subprocess
import RPi.GPIO as GPIO

from cmreslogging.handlers import CMRESHandler
from config import Config

log = logging.getLogger("wvg_key")
known_uid_to_name_dict = {}

#################
# CONFIG        #
#################
configFile = file('pi-nfc-lock.conf')
config = Config(configFile)

#################
# CLASSES       #
#################
class Timeout(Exception):
    pass

#################
# METHODS       #
#################

def init_logging():
    # define logging information and timestamp format
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")

    # create logger
    log.setLevel(logging.DEBUG)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.FileHandler('./wvg-lock.log')
    fh.setLevel(logging.DEBUG)

    # create elasticsearch handler
    eh = CMRESHandler(hosts=[{'host': config.elasticsearch_host, 'port': config.elasticsearch_port}],
                           auth_type=CMRESHandler.AuthType.NO_AUTH,
                           es_index_name=config.elasticsearch_index)

    # link logger formatter and handler
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    log.addHandler(ch)
    log.addHandler(fh)
    log.addHandler(eh)

def parse_allowed_uids():
    with open('accessAllowed.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            known_uid_to_name_dict.update({row[0]: row[1]})

def signal_timeout(signal, frame):
    raise Timeout

def signal_handler(signal, frame):
    sys.exit(0)


def on_known():
    GPIO.output(38,1)
    time.sleep(config.lock_open_in_seconds)
    GPIO.output(38,0)
    time.sleep(config.lock_pause_after_open_in_seconds)

def on_unknown():
    time.sleep(config.lock_pause_after_unknown_in_seconds)

def on_shutdown():
    log.info("System shutdown")


#################
# INIT          #
#################

init_logging()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGALRM, signal_timeout)
atexit.register(on_shutdown)

parse_allowed_uids()

log.info("System startup: " + `len(known_uid_to_name_dict)` + " known Uid(s)")

#################
# LOGIC         #
#################

while True:
    try:
        signal.alarm(3)
        uid = str(subprocess.Popen(["python", "./get_uid.py"], stdout=subprocess.PIPE).communicate()[0]).rstrip()
        signal.alarm(0)
        if uid:
            if uid in known_uid_to_name_dict.keys():
                log.info("Access granted for " + known_uid_to_name_dict[uid] + " [" + uid[0:15] + "]")
                on_known()
            else:
                log.warn("No Access " + uid)
                on_unknown()
    except:
        # We do not want an unknown exception to kill our python script.
        log.error("Unexpected error: " + str(sys.exc_info()[0]))
        time.sleep(60)
