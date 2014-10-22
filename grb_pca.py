#!/usr/bin/env python

import numpy as np
import math
from sklearn.decomposition import PCA
import pylab as pl
import matplotlib as mpl
import matplotlib.pyplot as plt
import hotshot, hotshot.stats

from os import makedirs
from os.path import isdir, exists
from sys import exit
from optparse import *

parser=OptionParser(usage="Make Scattered-plot of PCA analysis", version="NA")
parser.add_option("-f","--filename", action="store", type="string", default="NoFile", help="Prefix of filename; Default is NoFile")
parser.add_option("-o","--output-dir", action="store", type="string", default="output", help="Output directory; Default is output")
parser.add_option("-i","--input-dir", action="store", type="string", default=".", help="Input directory; Default is .")
parser.add_option("-F", "--font-size", action="store", type="int", default=6, help="font size; default is 6")
parser.add_option("-l", "--log-dir", action="store", type="string", default="log_dir", help="Log-file directory; Default is log_dir")

(opts,files)=parser.parse_args()


if isdir(output_dir):
    print "Directory exists:", output_dir
else:
    print "Creating directory:", output_dir
    makedirs(output_dir)

if isdir(log_dir):
    print "Directory exists:", log_dir
else:
    print "Creating directory:", log_dir
    makedirs(log_dir)

filename   = '.'.join(((opts.filename.split('/'))[-1].split('.'))[:-1])
input_dir = opts.input_dir
input_file = input_dir+'/'+opts.filename
output_dir = opts.output_dir
log_dir = opts.log_dir

profile_filename=log_dir+'/'+filename+"_prof.result"
prof=hotshot.Profile(profile_filename)
prof.start()

# Data Processing

if exists(input_file):
    f=open(input_file,'r')
    i=0
    while 1:
        data=f.readline()
        if not data: break
        g=open(log_dir+'/'+filename+'_tfd.txt','a')
        l=open(log_dir+'/'+filename+'_tfdcls.txt','a')
        if i == 0:
            pass
        elif len(data)<10:
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
    print "No input file:",in_file
    exit()
print "Writing processed data:"+filename+"_tfd.txt"
print "Writing Processed class:"+filename+"_tfdcls.txt"

# Load Data Sets

data=np.loadtxt(log_dir+'/'+filename+'_tfd.txt')
cls=np.loadtxt(log_dir+'/'+filename+'_tfdcls.txt')


# PCA Transform

X=data
y=cls
target_names = ['class 1','class 2']

pca=PCA(n_components=2)
X_r=pca.fit(X).transform(X)

f=open(log_dir+'/'+filename+'_Xr_data.txt','a')
for i in range(len(X_r)):
    f.write(str(X_r[i][0]))
    f.write(' ')
    f.write(str(X_r[i][1]))
    f.write('\n')
f.close()
print "Generating transformed X_r data file..."


# Percentage of variance explained for each components                                                                    
print('explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))
print('Drawing PCA figure....')


# Plotting

for c, i, target_name in zip("rbg", [0, 1, 2], target_names):
    plt.scatter(X_r[y == i, 0], X_r[y == i, 1], c=c, label=target_name)
plt.legend()
plt.suptitle('PCA of GRB Data', fontsize=14, fontweight='bold')
plt.title(filename, fontsize=10)
plt.savefig(output_dir+'/'+filename+'_pcafig.png', format='PNG')
#plt.show()
plt.close()

print "All Jobs Done."
print ('\n')

prof.stop()
prof.close()
stats=hotshot.stats.load(profile_filename)
stats.strip_dirs()
stats.sort_stats('time','calls')
stats.print_stats(0)
