import csv
import logging
import nxppy
import time
import atexit
import sys
import signal
import hashlib

log = logging.getLogger("wvg_key")
known_uid_to_name_dict = {}


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

    # link logger formatter and handler
    ch.setFormatter(formatter)
    log.addHandler(ch)


def parse_allowed_uids():
    with open('accessAllowed.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            known_uid_to_name_dict.update({row[0]: row[1]})


def signal_handler(signal, frame):
    sys.exit(0)


def on_known():
    pass


def on_unknown():
    pass


def on_shutdown():
    log.info("System shutdown")


#################
# INIT          #
#################

init_logging()

signal.signal(signal.SIGINT, signal_handler)
atexit.register(on_shutdown)

parse_allowed_uids()

mifare = nxppy.Mifare()

log.info("System startup: " + `len(known_uid_to_name_dict)` + " known Uid(s)")

#################
# LOGIC         #
#################

while True:
    try:
        uid = hashlib.sha224(mifare.select()).hexdigest()
        if uid in known_uid_to_name_dict.keys():
            log.info("Access granted for " + known_uid_to_name_dict[uid] + " [" + uid[0:15] + "]")
            on_known()
        else:
            log.warn("No Access " + uid)
            on_unknown()
    except nxppy.SelectError:
        # SelectError is raised if no card is in the field.
        pass
    except:
        # We do not want an unknown exception to kill our python script.
        log.error("Unexpected error: " + sys.exc_info()[0])
        pass

    time.sleep(1)
