#!/usr/bin/env python
###################################################################                                 
#                         file_combiner.py
#                                                                                                                      
#                    Used Modules: Numpy, Scipy
#                Combining RR individual Data Sets
#                          2014. 4. 7                                                                                 
#                    Author: John J. Oh (NIMS)                                                                         
#                              v.1.0                                                                                   
# Usage: e.g) python file_combiner.py --help
#   
####################################################################  
import numpy as np
import os
import hotshot, hotshot.stats
import glob

from os import makedirs
from os.path import isdir, exists
from sys import exit
from optparse import *

parser=OptionParser(usage="Generating .ann input file with Combining ten RR files", version="NA")
parser.add_option("-o","--output-dir", action="store", type="string", default="output", help="Output directory; Default is output")
parser.add_option("-i","--input-dir", action="store", type="string", default=".", help="Input directory; Default is .")
parser.add_option("-l", "--log-dir", action="store", type="string", default="log_dir", help="Log-file directory; Default is log_dir")
parser.add_option("-t", "--tag", action="store", type="string",default="none")

(opts,files)=parser.parse_args()
input_dir = opts.input_dir
output_dir = opts.output_dir
log_dir = opts.log_dir
tag=opts.tag

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

# Data Handling                                                                                                                       # .ann / .pat input 
#                                                                                                                                     

for i in range(0,10):
    g=open(input_dir+'/'+'S5VSR1_coh_grb_GRB070714B_NSNS10_H1L1V1_rr10_'+str(i)+'_off_evaluation.ann','r')
    p=0
    while 1:
        h=open(log_dir+'/'+tag+'_combined_dat.txt','a')
        m=open(log_dir+'/'+tag+'_combined_cls.txt','a')
        data=g.readline()
        if not data: break
        if p==0:
            pass
        elif (p % 2)==0:
            m.write(data[0:-1])
            m.write('\n')
        else:
            h.write(data[0:-1])
            h.write('\n')
        m.close()
        h.close()
        p+=1
hdat=np.loadtxt(log_dir+'/'+tag+'_combined_dat.txt')
print len(hdat), len(hdat[0])

for i in range(0,10):
    f=open(output_dir+'/'+tag+'_combined.ann','a')
    g=open(input_dir+'/'+'S5VSR1_coh_grb_GRB070714B_NSNS10_H1L1V1_rr10_'+str(i)+'_off_evaluation.ann','r')
    if i==0:
        k=0
        while 1:
            data = g.readline()
            if not data: break
            if k==0:
                f.write(str(len(hdat)))
                f.write(' ')
                f.write(str(len(hdat[0])))
                f.write(' ')
                f.write('1')
                f.write('\n')
            else:
                f.write(data[0:-1])
                f.write('\n')
            k+=1
    else:
        j=0
        while 1:
            data=g.readline()
            if not data: break
            if j==0:
                pass
            else:
                f.write(data[0:-1])
                f.write('\n')
            j+=1
    g.close()
    f.close()


print "Generating a combined .ann input file...:"+tag+"_combined.ann"

print "All Jobs Done."

prof.stop()
prof.close()
stats=hotshot.stats.load(profile_filename)
stats.strip_dirs()
stats.sort_stats('time','calls')
stats.print_stats(0)

