import os
from os import listdir
from os.path import isfile, join
import syslog

mypath= "/home/stanley/addXmcDevices/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

syslog.syslog("myXmc_sensor: All files -> %s " % onlyfiles)

# filter on only csv files
for f in onlyfiles:
    if ".csv" in f:
        print "File is -> %s " % f
        #only trigger on files that have content
        if os.path.getsize(mypath+f) > 0:
            # get the files contents
            # prepare the contents for injection to the workflow
            # Should we now delete the file? Or should the workflow?
            pass
