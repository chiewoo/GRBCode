#!/usr/bin/env python
###################################################################
#                         sample_counter.py
#
#        Counting number of signal and background samples
#                          2014. 5. 23
#                    Author: John J. Oh (NIMS)
#                              v.1.0
####################################################################
import numpy as np
import math
import os
import glob
import sys
from os import makedirs
from os.path import isdir, exists
from sys import exit
from optparse import *
from data_process import file_splitter

class Log:
    def __init__(self, stdout, logpath):
        self.stdout = stdout
        self.logfile = open(logpath, 'w')
    def write(self, s):
        self.stdout.write(s)
        self.logfile.write(s)
#    def close(self):
#        self.logfile.close()

parser=OptionParser(usage="Sample Counter", version="1.0")
parser.add_option("-f","--filename", action="store", type="string", default="NoFile", help="Input data file with .ann format; Default is NoFile")
parser.add_option("-o","--output-dir", action="store", type="string", default="output", help="Output directory; Default is output")
parser.add_option("-i","--input-dir", action="store", type="string", default=".", help="Input directory; Default is .")

(opts,files)=parser.parse_args()
filename   = '.'.join(((opts.filename.split('/'))[-1].split('.'))[:-1])
input_dir = opts.input_dir
input_file = input_dir+'/'+opts.filename
output_dir = opts.output_dir

if isdir(output_dir):
    print "Directory exists:", output_dir
else:
    print "Creating directory:", output_dir
    makedirs(output_dir)
#if isdir(log_dir):
#    logfiles=glob.glob('log_dir/*')
#    print "Directory exists:", log_dir
#    for f in logfiles:
#        os.remove(f)
#    print "Removing all log files..."
#else:
#    print "Creating directory:", log_dir
#    makedirs(log_dir)

sys.stdout = Log(sys.stdout, output_dir+'/'+'Sample_Counter_Report.log')

file_splitter(input_file, filename, output_dir)

cls=np.loadtxt(output_dir+'/'+filename+'_cls.txt')
sgnl=0
bgrd=0
for i in range(len(cls)):
    if cls[i] == 1.0:
        sgnl+=1
    else:
        bgrd+=1

print 'Signal Samples:', sgnl
print 'Background Samples:', bgrd
