# *********************************************************************
# This file illustrates how to execute a command and get it's output
# *********************************************************************

import subprocess

# Run ls command, get output, and print it
output = subprocess.getstatusoutput('ls -l')
for line in output:
    print(line)

