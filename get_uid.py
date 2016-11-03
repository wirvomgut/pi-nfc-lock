import nxppy

try:
        print nxppy.Mifare().select()
except:
        # We do not care
        pass
        
