#!/usr/bin/env python                                                                                                                  
import numpy as np
import math
import scipy as sp
from scipy.stats import pearsonr
import os
import glob
import hotshot, hotshot.stats

from os import makedirs
from os.path import isdir, exists
from sys import exit
from optparse import *

parser=OptionParser(usage="Generating .ann input file with highly correlated features using Pearson's Correlation", version="NA")
parser.add_option("-t","--t-filename", action="store", type="string", default="NoFile", help="Prefix of Training Filename; Default is NoFile")
parser.add_option("-e","--e-filename", action="store", type="string", default="NoFile", help="Prefix of Evaluation Filename; Default is NoFile")
parser.add_option("-o","--output-dir", action="store", type="string", default="output", help="Output directory; Default is output")
parser.add_option("-i","--input-dir", action="store", type="string", default=".", help="Input directory; Default is .")
parser.add_option("-l", "--log-dir", action="store", type="string", default="log_dir", help="Log-file directory; Default is log_dir")

(opts,files)=parser.parse_args()
tfilename   = '.'.join(((opts.t_filename.split('/'))[-1].split('.'))[:-1])
efilename   = '.'.join(((opts.e_filename.split('/'))[-1].split('.'))[:-1])
extension  = '.'.join(((opts.t_filename.split('/'))[-1].split('.'))[-1:])
input_dir = opts.input_dir
input_file1 = input_dir+'/'+opts.t_filename
input_file2 = input_dir+'/'+opts.e_filename
output_dir = opts.output_dir
log_dir = opts.log_dir

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

profile_filename=log_dir+'/'+"Profiling.result"
prof=hotshot.Profile(profile_filename)
prof.start()


# Data Handling
# .ann / .pat input
#
if exists(input_file1):
    f=open(input_file1,'r')
    i=0
    while 1:
        data=f.readline()
        if not data: break
        g=open(log_dir+'/'+tfilename+'_tfd.txt','a')
        l=open(log_dir+'/'+tfilename+'_tfdcls.txt','a')
        if extension == 'pat': # .pat input
            if i < 2 :
                pass
            else:
                l.write(data[-9:-1])
                l.write('\n')
                g.write(data[0:-10])
                g.write('\n')
        elif extension == 'ann': # .ann input
            if i==0:
                pass
            elif (i % 2)==0:
                l.write(data[0:-1])
                l.write('\n')
            else:
                g.write(data[0:-1])
                g.write('\n')
        g.close()
        l.close()
        i+=1
    f.close()
else:
    print "No input file:",input_file1
    exit()
print "Writing processed data:"+tfilename+"_tfd.txt"
print "Writing Processed class:"+tfilename+"_tfdcls.txt"

if exists(input_file2):
    f=open(input_file2,'r')
    i=0
    while 1:
        data=f.readline()
        if not data: break
        g=open(log_dir+'/'+efilename+'_tfd.txt','a')
        l=open(log_dir+'/'+efilename+'_tfdcls.txt','a')
        if extension == 'pat': # .pat input
            if i < 2 :
                pass
            else:
                l.write(data[-9:-1])
                l.write('\n')
                g.write(data[0:-10])
                g.write('\n')
        elif extension == 'ann': # .ann input
            if i==0:
                pass
            elif (i % 2)==0:
                l.write(data[0:-1])
                l.write('\n')
            else:
                g.write(data[0:-1])
                g.write('\n')
        g.close()
        l.close()
        i+=1
    f.close()
else:
    print "No input file:",input_file2
    exit()
print "Writing processed data:"+efilename+"_tfd.txt"
print "Writing Processed class:"+efilename+"_tfdcls.txt"


# Compute Pearson's Correlation Coefficient
# if PCC > 80 then Write
# else discard
# Generate selected .ann input
# (PCC, p-value) 
# if PCC > 0.8 and p-value < 0.001 then take:
#

# Load Data Sets                                                                                                                       

datat=np.loadtxt(log_dir+'/'+tfilename+'_tfd.txt')
clst=np.loadtxt(log_dir+'/'+tfilename+'_tfdcls.txt')
datae=np.loadtxt(log_dir+'/'+efilename+'_tfd.txt')
clse=np.loadtxt(log_dir+'/'+efilename+'_tfdcls.txt')

S=[]
stackt = []
stacke = []
for i in range(len(datat.T)):
    for j in range(i+1,len(datat.T)):
        pcct = sp.stats.pearsonr(datat.T[i],datat.T[j])
        if pcct[0] > 0.8 and pcct[1] < 0.01:
            print pcct, (i,j)
            if j in stackt:
                pass
            else:
                stackt.append(j)

for k in range(len(datae.T)):
    for l in range(k+1,len(datae.T)):
        pcce= sp.stats.pearsonr(datae.T[k],datae.T[l])
        if pcce[0] > 0.8 and pcce[1] < 0.01:
            print pcce, (k,l)
            if l in stacke:
                pass
            else:
                stacke.append(l)

for ele in stackt:
    if ele in stacke:
        S.append(ele)

print 'removable feature index:', S


# Generate .ann file




prof.stop()
prof.close()
stats=hotshot.stats.load(profile_filename)
stats.strip_dirs()
stats.sort_stats('time','calls')
stats.print_stats(0)
