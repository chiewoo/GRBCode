#!/usr/bin/env python
###################################################################
#                         Compute_Mic.py
#
#         Used Modules: Scikit-Learn, Numpy, Scipy, Data_Process
#         Mutual Information Feature Selection Code
#                          2014. 5. 22 
#                    Author: John J. Oh (NIMS)
#                              v.1.2
# Functional Summary:
#  a) Input data and class files
#  b) Compute Mutual Information Indexes based on NMIFS algorithm
#  c) Generate Highly correlated feature index
#  d) Removing Uncorrelated features and Regenerate Reduced Files
# Usage: e.g) 
#   python compute_mic.py -f ALL_S6_full_set_full_combined.ann 
#  -o S6/combined_full/mic_500 -i S6/combined_full/ 
#  -l S6/combined_full/mic_500/logs -k 500
####################################################################
import numpy as np
import scipy as sp
import math
import os
import glob
import hotshot, hotshot.stats
import sys
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import mutual_info_score
from os import makedirs
from os.path import isdir, exists
from sys import exit
from optparse import *
from data_process import feat_remover
from data_process import file_splitter
from data_process import null_remover
from data_process import file_merger

class Log:
    def __init__(self, stdout, logpath):
        self.stdout = stdout
        self.logfile = open(logpath, 'w')
    def write(self, s):
        self.stdout.write(s)
        self.logfile.write(s)
#    def close(self):
#        self.logfile.close()

parser=OptionParser(usage="Computing MIC with a given data", version="none")
parser.add_option("-f","--filename", action="store", type="string", default="NoFile", help="Input data file; Default is NoFile")
parser.add_option("-o","--output-dir", action="store", type="string", default="output", help="Output directory; Default is output")
parser.add_option("-i","--input-dir", action="store", type="string", default=".", help="Input directory; Default is .")
parser.add_option("-l", "--log-dir", action="store", type="string", default="log_dir", help="Log-file directory; Default is log_dir")
parser.add_option("-k", "--k", action="store", type="int", default="5", help="no of selected features")
#parser.add_option("-C", "--chan-anal", action="store_true", default="False", dest='flag', help="Channel Analysis: Default is False")
parser.add_option("-d", "--cinput-dir", action="store", type="string", default=".", help="directory where the channel list file locates")
parser.add_option("-c", "--chan-file", action="store", type="string", default="NoFile", help="Channel List Filename")

(opts,files)=parser.parse_args()
filename   = '.'.join(((opts.filename.split('/'))[-1].split('.'))[:-1])
input_dir = opts.input_dir
input_file = input_dir+'/'+opts.filename
output_dir = opts.output_dir
log_dir = opts.log_dir
k = opts.k
#flag = opts.chan_anal
cinput_dir = opts.cinput_dir
chan_input = cinput_dir+'/'+opts.chan_file

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

sys.stdout = Log(sys.stdout, output_dir+'/'+'MIC_Report.log')

profile_filename=log_dir+'/'+"Profiling.result"
prof=hotshot.Profile(profile_filename)
prof.start()

file_splitter(input_file, filename, output_dir)

################################
#
# Data Load and Compute MIC: Based on NMIFS Algorithm
# P.A.Estevez et. al. IEEE Transaction on Neural Networks, Vol.20, No.2, 189 (2009)
#
#######
## Step1. Initialization
#######

f = np.loadtxt(output_dir+'/'+filename+'_dat.txt')
cls = np.loadtxt(output_dir+'/'+filename+'_cls.txt')
s=[]
mi_stack=[]
fi=range(len(f.T))

########
## Step2 & 3. Compute MI w.r.t classes and find the 1st feature:
########
for i in range(len(f.T)):
    mi = mutual_info_score(f.T[i],cls)
    mi_stack.append(mi)
print 'Evaluating the normalized mutual information coefficient w.r.t. the classes'

max=np.max(mi_stack)

for i in range(len(f.T)):
    if mi_stack[i] == max:
        s.append(i)
        fi.remove(i)
print '(max_mi,max_mi_index):', (max, s[0])
print 'The rest feature index:', fi

###########
## Step4. Greedy Selection: Repeat unitl |S|=k.
## a) Calculate MI btw features: I(f_i;f_s) for all pairs (f_i,f_s).
## b) Select the next feature that maximizes measure:
##       G=I(C;f_i)-1/|S| sum (NI(f_i;f_s)) 
## The formula shown in P. A. Estevez et. al. (IEEE Transaction on Neural Networks, Vol.20, No.2 (2009))
## And Set F <- F\{f_i} and S<-{f_i}
###########
mi2=0
mi2_sum=0
while 1:
    mi2_stack=[]
    G_stack=[]
    print 'Number of Selected Features:', len(s)
    if len(s)==k: break
    for i in fi:
        for j in s:
            mi2=normalized_mutual_info_score(f.T[i], f.T[j])
            mi2_stack.append(mi2)
            mi2_sum+=mi2
        mi = mutual_info_score(f.T[i],cls)
        G=mi-1/len(s)*mi2_sum
        G_stack.append([G,i])
    max_G=G_stack[np.argmax(G_stack,axis=0)[0]][0]
    max_G_index=G_stack[np.argmax(G_stack,axis=0)[0]][1]
    print '(max_mi, max_mi_index):', (max_G, max_G_index)
    s.append(max_G_index)
    fi.remove(max_G_index)
    print 'The rest of feature index:', fi

s.sort()
print 'Highly Correlated Feature Index:', s
#print 'Uncorrelated Feature Index:', fi

# Removing features

rmvd_f=feat_remover(f, cls, s)
#rest_f=feat_remover(f, cls, fi)

# Generate .ann file                                                                                                    
#print 'Eliminating the higly correlated features...'
print'Eliminating the Uncorrelated features....'

p=open(output_dir+'/'+filename+'_reduced_temp_dat.txt','a')
for i in range(len(rmvd_f)):
    for j in range(len(rmvd_f[0])):
        p.write(str(rmvd_f[i][j]).strip())
        p.write(' ')
    p.write('\n')
p.close()

#for i in range(len(rest_f)):
 #   for j in range(len(rest_f[0])):
 #       p.write(str(rest_f[i][j]).strip())
 #       p.write(' ')
 #   p.write('\n')
#p.close()

print'Generating feature reduced .ann file....'
g=open(output_dir+'/'+filename+'_reduced_temp_dat.txt','r')
k=open(output_dir+'/'+filename+'_cls.txt','r')
h=open(output_dir+'/'+filename+'_reduced.ann','a')
h.write(str(len(rmvd_f)))
#h.write(str(len(rest_f)))
h.write(' ')
h.write(str(len(rmvd_f[0])))
#h.write(str(len(rest_f[0])))
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

#print 'Removing null vectors....'
#rmv_input=output_dir+'/'+filename+'_reduced_temp_dat.txt'
#null_remover(rmv_input, filename, output_dir)

#print 'Generating reduced and null-removed .ann file....'
#dat_file=oupput_dir+'/'filename+'_reduced_null_rmvd_dat.txt'
#dat_file=output_dir+'/'+filename+'_reduced_temp_dat.txt'
#cls_file=output_dir+'/'+filename+'_cls.txt'

#file_merger(dat_file, cls_file, filename, output_dir)

flag=True

if flag=='False':
    pass
else:
    print 'Starting channel analysis...'
    f=open(chan_input,'r')
    list=f.readlines()
#    attrib=['signif','dt']
    chlist=[]
    chan=[]
    for i in range(0,12):
#        for j in range(0,2):
        chlist.append(list[i].strip())
    for i in range(0,len(chlist)):
        chan.append((i,chlist[i]))
    g=open(output_dir+'/'+filename+'_channel_analysis.log','a')
    print 'Highly Correlated Channels:'
    g.write('Highly Correlated Channels:')
    g.write('\n')
    for i in range(len(chan)):
        #    if chan[i][0] in fi:
        if chan[i][0] in s:
            print chan[i]
            g.write(str(chan[i][0]))
            g.write(':')
            g.write(str(chan[i][1]))
            g.write('\n')
    g.close()
    f.close()
        

print 'All computation done.'

prof.stop()
prof.close()
stats=hotshot.stats.load(profile_filename)
stats.strip_dirs()
stats.sort_stats('time','calls')
stats.print_stats(0)


