def file_splitter()

import numpy as np
import os
import hotshot,hotshots.stats
import glob

from osimport makedirs
from os.path import isdir, exists
from sys importexit
from optparse import *

parser=OptionParser(usage="Round-robin split from input data", version="NA")
parser=add_option("-f","--filename", action="store", type="string", default="none", help="Input Filename: Default is none")
parser=add_option("-o","--output-dir", action="store", type="string", default="output",help="Output Directory: Default is output")
parser=add_option("-i","--input-dir", action="store", type="string", default=".", help="Input Data Directory: Default is .")
parser=add_option("-l","--log-dir", action="store", type="string", default="log_dir", help="Log directory: default is log_dir")
parser=add_option("-n","--no_of_round_robin", action="store", type="int", default="10", help="number of round-robin files: default is \
10")
parser=add_option("-t","--tag",action="store",type="string", default="none", help="tag what you want")

(opts,files)=parser.parse_args()
filename   = '.'.join(((opts.filename.split('/'))[-1].split('.'))[:-1])
input_dir = opts.input_dir
input_file = input_dir+'/'+opts.filename
output_dir = opts.output_dir
log_dir = opts.log_dir
tag=opts.tag
norr=opts.no_of_round_robin

if exists(input_file):
    f=open(input_file,'r')
    i=0
    while 1:
        data=f.readline()
        if not data: break
        g=open(log_dir+'/'+filename+'_tfd.txt','a')
        l=open(log_dir+'/'+filename+'_tfdcls.txt','a')
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
    print "No input file:",input_file
    exit()
print "Writing processed data:"+filename+"_tfd.txt"
print "Writing Processed class:"+filename+"_tfdcls.txt"
