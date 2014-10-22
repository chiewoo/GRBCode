#!/usr/bin/env python                                                                                                 
###################################################################                                 
#                   FS_pearson_combined_class.py
#                                                                                                                      
#                    Used Modules: Numpy, Scipy
#               Feature Selection by Pearson's Correlation
#                          2014. 5. 26                                                                                 
#                    Author: John J. Oh (NIMS)                                                                         
#                              v.1.0                                                                                   
# Usage: e.g) python FS_pearson_combined_mdfyd.py --help
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
parser.add_option("-n", "--num-of-features", action="store", type="int", default="6", help="Number of Features that you want to have")

(opts,files)=parser.parse_args()
filename   = '.'.join(((opts.filename.split('/'))[-1].split('.'))[:-1])
extension  = '.'.join(((opts.filename.split('/'))[-1].split('.'))[-1:])
input_dir = opts.input_dir
input_file = input_dir+'/'+opts.filename
output_dir = opts.output_dir
log_dir = opts.log_dir
num = opts.num_of_features

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
# Compute Pearson's Correlation Coefficient between Features and Class
# if PCC > 80 then Write
# else discard
# Generate selected .ann input
# (PCC, p-value) 
# if PCC > pcc_thrshd and p-value < pv_thrshd then take:
#

# Load Data Sets                                                                                                                       

data=np.loadtxt(log_dir+'/'+filename+'_dat.txt')
cls=np.loadtxt(log_dir+'/'+filename+'_cls.txt')

f=open(log_dir+'/'+filename+'_pearson_result.txt','a')
stack = []
max_pearson=[]
max_index=[]
for i in range(len(data.T)):
    pcc = sp.stats.pearsonr(data.T[i],cls)
    print (pcc[0],pcc[1])
    print 'feature index:', i
    stack.append([pcc[0],i])
for i in range(num):
    max_value=max(stack)
    max_pearson.append(max_value[0])
    max_index.append(max_value[1])
    stack.remove(max_value)
print 'Selected PCC value:', max_pearson
print 'Highly Correlated Index:', max_index
f.write('Selected PCC value:')
f.write(str(max_pearson))
f.write('\n')
f.write('Highly Correlated Feature Index:')
f.write(str(max_index))
f.write('\n')
f.close()


# Removing Uncorrelated feature column
rmf=range(0,12)
for i in range(len(max_index)):
    rmf.remove(max_index[i])

print 'Uncorrelated Feature Index:', rmf


for i in range(len(rmf)):
    data = np.delete(data.T, rmf[i]-i, 0).T



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
