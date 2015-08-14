import sys
import glob
import errno
from datetime import datetime

result = []
file = open('/var/ossec/logs/alerts/alerts.log','r')
FMT = '%Y%b%d%H:%M:%S'

#path = '/var/ossec/logs/alerts/*.log'   
#files = glob.glob(path)   
#for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
a = datetime.now()
try:
    #with open(files) as f: # No need to specify 'r': this is the default.
    data = [line for line in file.readlines()]
    for line in data:
        if line.startswith("**"):
            index = data.index(line)
            res1 = data[index+1].split(" ")
            #print res1
            timestamp1 = res1[0] , res1[1] , res1[2] , res1[3]
            timestamp1 = ''.join(timestamp1) 
            print "Timestamp: " , timestamp1
            print "Location: " + res1[4]
            res2 = data[index+2].split("->")
            rule = res2[0].find("Rule: ")
            print "Rule Number: ",res2[0][6] + res2[0][7] #+ res2[0][8] + res2[0][9] 
            level = res2[0].find("level")
            print "Level: ",res2[0][16]
            print "Event = " + res2[1]
            res3 = data[index+3]
            print "Detailed Description: " + res3
            #print res3
            t1 = datetime.strptime(timestamp1, FMT)
            b = datetime.now()
            print "Initial Timestamp: ",a ,"\n","Alert Timestamp: " , t1 ,"\n","Final Timestamp: ", b
            delta = b-a
            delta2 = t1 - a
            delta3 = b - t1
            print "delta1",delta.total_seconds()
            print "delta2",delta2.total_seconds()
            print "delta3",delta3.total_seconds()
            print "--------------------------------------------------------------------------------"

except IOError as exc:
    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
        raise # Propagate other kinds of IOError.

