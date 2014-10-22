#!/usr/bin/env python                                                                                                                 ###################################################################                                                                   
#                      FS_pearson_combined.py                                                                                      
#                                                                                                                                     
#                    Used Modules: Numpy, Scipy                                                                                       
#               Feature Selection by Pearson's Correlation                                                                            
#                     Removing Redundant Features
#                          2014. 4. 7                                                                                                 
#                    Author: John J. Oh (NIMS)                                                                                        
#                              v.1.0                                                                                                  
# Usage: e.g) python FS_pearson_combined.py --help                                                                              
#                                                                                                                                     
####################################################################  
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
parser.add_option("-f","--filename", action="store", type="string", default="NoFile", help="Prefix of Filename; Default is NoFile")
parser.add_option("-o","--output-dir", action="store", type="string", default="output", help="Output directory; Default is output")
parser.add_option("-i","--input-dir", action="store", type="string", default=".", help="Input directory; Default is .")
parser.add_option("-l", "--log-dir", action="store", type="string", default="log_dir", help="Log-file directory; Default is log_dir")
parser.add_option("-c", "--pcc-thrshd", action="store", type="float", default="0.8", help="Decision threshold of Pearson's Correlation Coefficient: Default is 0.8")
parser.add_option("-v", "--pv-thrshd", action="store", type="float", default="0.01", help="Decision threshold of 2-tailed p-value: Default is 0.01")

(opts,files)=parser.parse_args()
filename   = '.'.join(((opts.filename.split('/'))[-1].split('.'))[:-1])
extension  = '.'.join(((opts.filename.split('/'))[-1].split('.'))[-1:])
input_dir = opts.input_dir
input_file = input_dir+'/'+opts.filename
output_dir = opts.output_dir
log_dir = opts.log_dir
pcc_thrshd = opts.pcc_thrshd
pv_thrshd = opts.pv_thrshd

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

# File Decompose - Data-Class

if exists(log_dir+'/'+filename+'_dat.txt'):
    pass
else:
    g=open(input_file,'r')
    p=0
    h=open(log_dir+'/'+filename+'_dat.txt','a')
    m=open(log_dir+'/'+filename+'_cls.txt','a')
    while 1:
        data=g.readline()
        if not data: break
        if p==0:
            pass
        elif (p % 2)==0:
            m.write(str(data[0:-1]))
            m.write('\n')
        else:
            h.write(str(data[0:-1]))
            h.write('\n')
        p+=1
    h.close()
    m.close()
    g.close()
# Compute Pearson's Correlation Coefficient
# if PCC > 80 then Write
# else discard
# Generate selected .ann input
# (PCC, p-value) 
# if PCC > pcc_thrshd and p-value < pv_thrshd then take:
#

# Load Data Sets                                                                                                                       

data=np.loadtxt(log_dir+'/'+filename+'_dat.txt')
cls=np.loadtxt(log_dir+'/'+filename+'_cls.txt')

f=open(log_dir+'/'+filename+'pearson_result.txt','a')
stack = []
for i in range(len(data.T)):
    for j in range(i+1,len(data.T)):
        if i==j:
            pass
        else:
            pcc = sp.stats.pearsonr(data.T[i],data.T[j])
            if pcc[0] > pcc_thrshd and pcc[1] < pv_thrshd:
                print pcc, (i,j)
                f.write(str(pcc))
                f.write(':')
                f.write(str((i,j)))
                f.write('\n')
                if j in stack and i in stack:
                    pass
                elif j in stack and i not in stack:
                    stack.append(i)
                else:
                    stack.append(j)                
print 'Redundant Feature Index:', stack
f.write('Redundant Feature Index:')
f.write(str(stack))
f.write('\n')
f.close()


# Removing redundant feature column

for i in range(len(stack)):
    data = np.delete(data.T, stack[i]-i, 0).T



# Generate .ann file

print 'Eliminating the redundant features....'



f=open(log_dir+'/'+filename+'_reduced_temp.ann','a')

for i in range(len(data)):
    for j in range(len(data[0])):
        f.write(str(data[i][j]).strip())
        f.write(' ')
    f.write('\n')
f.close()
        

print 'Generating feature reduced .ann file....'

g=open(log_dir+'/'+filename+'_reduced_temp.ann','r')
k=open(log_dir+'/'+filename+'_cls.txt','r')
h=open(output_dir+'/'+filename+'_reduced.ann','a')
h.write(str(len(data)))
h.write(' ')
h.write(str(len(data[0])))
h.write(' ')
h.write('1')
h.write('\n')
while 1:
    data=g.readline()
    cls=k.readline()
    if not data: break
    h.write(data[0:-1])
    h.write('\n')
    h.write(cls[0:-1])
    h.write('\n')
h.close()
k.close()
g.close()


print 'All Jobs Done.'

prof.stop()
prof.close()
stats=hotshot.stats.load(profile_filename)
stats.strip_dirs()
stats.sort_stats('time','calls')
stats.print_stats(0)
