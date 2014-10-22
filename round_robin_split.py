#!/usr/bin/env python
###################################################################
#                         round_robin_split.py
#
#         Used Modules: Numpy, Data_Process
#          Generate round-robin training/evaluation data for NN
#                          2014. 5. 22 
#                    Author: John J. Oh (NIMS)
#                              v.1.2
####################################################################
import numpy as np
import os
import glob

from os import makedirs
from os.path import isdir, exists
from sys import exit
from optparse import *
from data_process import file_splitter

parser=OptionParser(usage="Round-robin split from input data", version="NA")
parser.add_option("-f","--filename", action="store", type="string", default="none", help="Input Filename: Default is none")
parser.add_option("-o","--output-dir", action="store", type="string", default="output", help="Output Directory: Default is output")
parser.add_option("-i","--input-dir", action="store", type="string", default=".", help="Input Data Directory: Default is .")
parser.add_option("-l","--log-dir", action="store", type="string", default="log_dir", help="Log directory: default is log_dir")
parser.add_option("-n","--no_of_round_robin", action="store", type="int", default="10", help="number of round-robin files: default is 10")
parser.add_option("-t","--tag", action="store", type="string", default="none", help="tag what you want")

(opts,files)=parser.parse_args()
filename   = '.'.join(((opts.filename.split('/'))[-1].split('.'))[:-1])
input_dir = opts.input_dir
input_file = input_dir+'/'+opts.filename
output_dir = opts.output_dir
log_dir = opts.log_dir
tag=opts.tag
norr=opts.no_of_round_robin

if isdir(output_dir):
    print "Directory exists:", output_dir
else:
    print "Creating directory:", output_dir
    makedirs(output_dir)
if isdir(log_dir):
    logfiles=glob.glob('log_dir/*')
    print "Directory exists:", log_dir
    for f in logfiles:
        os.remove(f)
    print "Removing all log files..."
else:
    print "Creating directory:", log_dir
    makedirs(log_dir)

# Data Processing                                                                                                                           
if exists(input_file):
    file_splitter(input_file, filename, output_dir)
else:
    print "No input file:",input_file
    exit()



# Load Data Sets                                                                                                                      
dat=np.loadtxt(output_dir+'/'+filename+'_dat.txt')
cls=np.loadtxt(output_dir+'/'+filename+'_cls.txt')

g=open(input_file,'r')
leng=g.readline().split()
g.close()

sp=divmod(int(leng[0]),norr)[0]
sd=divmod(int(leng[0]),norr)[1]

# Evaluation Data Set Generation
for id in range(norr):
    f=open(output_dir+'/'+tag+'_rr'+str(norr)+'_'+str(id)+'_evaluation_reduced.ann','a')
    print 'Generating '+str(id)+'-th round-robin evaluation data set.'
    if id < norr-1:
        f.write(str(sp))
        f.write(' ')
        f.write(str(leng[1]))
        f.write(' ')
        f.write(str(leng[2]))
        f.write('\n')
        for i in range(id*sp,(id+1)*sp):
            for j in range(int(leng[1])):
                f.write(str(dat[i][j]))
                f.write(' ')
            f.write('\n')
            f.write(str(cls[i]))
            f.write('\n')
    elif id == norr-1:
        f.write(str(sp+sd))
        f.write(' ')
        f.write(str(leng[1]))
        f.write(' ')
        f.write(str(leng[2]))
        f.write('\n')
        for i in range(id*sp,int(leng[0])):
            for j in range(int(leng[1])):
                f.write(str(dat[i][j]))
                f.write(' ')
            f.write('\n')
            f.write(str(cls[i]))
            f.write('\n')
    f.close()

# Training Data Set Generation
for id in range(norr):
    g=open(output_dir+'/'+tag+'_rr'+str(norr)+'_'+str(id)+'_training_reduced.ann','a')
    print 'Generating '+str(id)+'-th round_robin training data set.'
    if id == norr-1:
        g.write(str(int(leng[0])-int(sp+sd)))
        g.write(' ')
        g.write(str(leng[1]))
        g.write(' ')
        g.write(str(leng[2]))
        g.write('\n')
        p=range(norr)
        p.remove(id)
        for k in p:
            for i in range(k*sp, (k+1)*sp):
                for j in range(int(leng[1])):
                    g.write(str(dat[i][j]))
                    g.write(' ')
                g.write('\n')
                g.write(str(cls[i]))
                g.write('\n')
    else:
        g.write(str(int(leng[0])-int(sp)))
        g.write(' ')
        g.write(str(leng[1]))
        g.write(' ')
        g.write(str(leng[2]))
        g.write('\n')
        p=range(norr)
        p.remove(id)
        for k in p:
            if k==p[-1]:
                for i in range(k*sp,int(leng[0])):
                    for j in range(int(leng[1])):
                        g.write(str(dat[i][j]))
                        g.write(' ')
                    g.write('\n')
                    g.write(str(cls[i]))
                    g.write('\n')
            else:
                for i in range(k*sp, (k+1)*sp):
                    for j in range(int(leng[1])):
                        g.write(str(dat[i][j]))
                        g.write(' ')
                    g.write('\n')
                    g.write(str(cls[i]))
                    g.write('\n')
    p.append(id)
    p.sort()

