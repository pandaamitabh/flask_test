import sys
import os

path = os.getcwd() + "/testresult/Flag"
if sys.version_info.major < 4:
    RESULT = "Pass"
else:
    RESULT = "Fail"
    f = open(path, "w+")
    f.close()
print sys.version_info.major
print RESULT
print os.path.basename(__file__)
UPDATE = os.path.basename(__file__) + "," + RESULT
path = os.getcwd() + "/testresult/report.csv"
print path
try:
    f = open(path, "a")
except IOError:
    print path + " is opened, please close the file."
f.write("\n")
f.write(UPDATE)
f.close()
