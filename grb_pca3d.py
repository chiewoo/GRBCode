#!/usr/bin/env python

import numpy as np
import math
from sklearn.decomposition import PCA
import pylab as pl
import matplotlib as mpl
import matplotlib.pyplot as plt
import hotshot, hotshot.stats
from mpl_toolkits.mplot3d import Axes3D
import os
import glob

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
parser.add_option("-n", "--nop", action="store", type="int", default=2, help="Number of principal axes; Default is 2")
parser.add_option("-p", "--pca-dir", action="store", type="string", default="pcaed", help="PCAed File Directory; Default is pcaed")

(opts,files)=parser.parse_args()
filename   = '.'.join(((opts.filename.split('/'))[-1].split('.'))[:-1])
extension  = '.'.join(((opts.filename.split('/'))[-1].split('.'))[-1:])
input_dir = opts.input_dir
input_file = input_dir+'/'+opts.filename
output_dir = opts.output_dir
log_dir = opts.log_dir
nopax = opts.nop
pca_dir = opts.pca_dir

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

if isdir(pca_dir):
    logfiles=glob.glob('pca_dir/*')
    print "Directory exists:", pca_dir
else:
    print "Creating directory:", pca_dir
    makedirs(pca_dir)
    

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

# Load Data Sets

data=np.loadtxt(log_dir+'/'+filename+'_tfd.txt')
cls=np.loadtxt(log_dir+'/'+filename+'_tfdcls.txt')

#print "The number of Principal Axes: %d" %nopax

# PCA Transform

X=data
y=cls
target_names = ['class 1','class 2']

pca=PCA(n_components=nopax)
X_r=pca.fit(X).transform(X)

# Data Normalization and Writing

f=open(log_dir+'/'+filename+'_Xr_data.txt','a')
i=0
j=0

# Normalization

for j in range(len(X_r[0])):
    Xr_max = max(X_r.T[j])
    Xr_min = min(X_r.T[j])
    for i in range(len(X_r)):
        if Xr_min <0:
            X_r.T[j][i] = (X_r.T[j][i] + abs(Xr_min))/(Xr_max + abs(Xr_min))
        else:
            X_r.T[j][i] = (X_r.T[j][i] - abs(Xr_min))/(Xr_max - abs(Xr_min))
#print X_r
#print max(X_r.T[0]), min(X_r.T[0]), max(X_r.T[1]), min(X_r.T[1]), max(X_r.T[2]), min(X_r.T[2])
 
# Data Writing

for i in range(len(X_r)):
    for j in range(nopax):
        f.write(str(X_r[i][j]))
        if j<nopax:
            f.write(' ')
        else:
            pass
    f.write('\n')
f.close()



print "Generating transformed X_r data file..."


# PCAed Data Generation (.ann input files)

g=open(pca_dir+'/'+'PCAed_'+filename+'.ann','a')
f=open(log_dir+'/'+filename+'_Xr_data.txt','r')
l=open(log_dir+'/'+filename+'_tfdcls.txt','r')
g.write(str(len(X_r)))
g.write(' ')
g.write(str(len(X_r[0])))
g.write(' ')
g.write('1')
g.write('\n')
while 1:
    XrD=f.readline().strip()
    Tfdcls=l.readline().strip()
    if not Tfdcls: break
    if i==len(Tfdcls):
        g.write(XrD)
        g.write(Tfdcls)
    else:
        g.write(XrD)
        g.write('\n')
        g.write(Tfdcls)
        g.write('\n')
l.close()
f.close()
g.close()

print "Generating PCAed .ann Input files..."

# Percentage of variance explained for each components                                                                    
print('explained variance ratio (major components): %s'
      % str(pca.explained_variance_ratio_))

cumEVR = 0
for i in range(nopax):
    cumEVR += pca.explained_variance_ratio_[i]

print('Cumulative explained variance ratio: %s' %str(cumEVR))

print('Drawing PCA figure....')


# 3D Plotting

fig=plt.figure()
ax=fig.add_subplot(221,projection='3d')
for c, i, d in zip("rbg", [0, 1, 2], ['r','b']):
    ax.scatter(X_r[y==i, 0], X_r[y==i, 1], X_r[y==i, 2], s=3, c=c, edgecolor=d)
plt.suptitle('PCA of '+str(nopax)+'P_Axes GRB Data:'+filename, fontsize=9, fontweight='bold')
ax.set_xlabel('PA-1', fontsize=8,fontweight='bold')
ax.set_ylabel('PA-2', fontsize=8,fontweight='bold')
ax.set_zlabel('PA-3', fontsize=8,fontweight='bold')
plt.tick_params(axis='both', which='major', labelsize=6)

plt.subplot(222)
for c, i, target_name, d in zip("rbg", [0, 1, 2], target_names, ['r','b']):
    plt.scatter(X_r[y==i, 0], X_r[y==i, 1], s=4, c=c, label=target_name, edgecolor=d)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.xlabel('PA-1', fontsize=8,fontweight='bold')
plt.ylabel('PA-2', fontsize=8,fontweight='bold')

plt.subplot(223)
for c, i, target_name, d in zip("rbg", [0, 1, 2], target_names, ['r','b']):
    plt.scatter(X_r[y==i, 0], X_r[y==i, 2], s=4, c=c, label=target_name, edgecolor=d)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.xlabel('PA-1', fontsize=8,fontweight='bold')
plt.ylabel('PA-3', fontsize=8,fontweight='bold')

plt.subplot(224)
for c, i, target_name, d in zip("rbg", [0, 1, 2], target_names, ['r','b']):
    plt.scatter(X_r[y==i, 1], X_r[y==i, 2], s=4, c=c, label=target_name, edgecolor=d)
plt.tick_params(axis='both', which='major', labelsize=6)
plt.xlabel('PA-2', fontsize=8,fontweight='bold')
plt.ylabel('PA-3', fontsize=8,fontweight='bold')

plt.savefig(output_dir+'/'+filename+'_pca3dfig.png', format='PNG')


# Figures that need magnified investigation

#fig=plt.figure()
#ax=fig.add_subplot(111,projection='3d')
#for c, i, d in zip("rbg", [0, 1, 2], ['r','b']):
#    ax.scatter(X_r[y==i, 0], X_r[y==i, 1], X_r[y==i, 2], s=3, c=c, edgecolor=d)
#plt.suptitle('PCA of '+str(nopax)+'P_Axes GRB Data:'+filename, fontsize=9, fontweight='bold')
#ax.set_xlabel('PA-1', fontsize=8,fontweight='bold')
#ax.set_ylabel('PA-2', fontsize=8,fontweight='bold')
#ax.set_zlabel('PA-3', fontsize=8,fontweight='bold')
#plt.tick_params(axis='both', which='major', labelsize=6)
#plt.show()

#plt.figure()
#for c, i, target_name, d in zip("rbg", [0, 1, 2], target_names, ['r','b']):
#    plt.scatter(X_r[y==i, 0], X_r[y==i, 1], s=4, c=c, label=target_name, edgecolor=d)
#    plt.tick_params(axis='both', which='major', labelsize=6)
#    plt.xlabel('PA-1', fontsize=8,fontweight='bold')
#    plt.ylabel('PA-2', fontsize=8,fontweight='bold')
#plt.figure()
#for c, i, target_name, d in zip("rbg", [0, 1, 2], target_names, ['r','b']):
#    plt.scatter(X_r[y==i, 0], X_r[y==i, 2], s=4, c=c, label=target_name, edgecolor=d)
#    plt.tick_params(axis='both', which='major', labelsize=6)
#    plt.xlabel('PA-1', fontsize=8,fontweight='bold')
#    plt.ylabel('PA-3', fontsize=8,fontweight='bold')
#plt.figure()
#for c, i, target_name, d in zip("rbg", [0, 1, 2], target_names, ['r','b']):
#    plt.scatter(X_r[y==i, 1], X_r[y==i, 2], s=4, c=c, label=target_name, edgecolor=d)
#    plt.tick_params(axis='both', which='major', labelsize=6)
#    plt.xlabel('PA-2', fontsize=8,fontweight='bold')
#    plt.ylabel('PA-3', fontsize=8,fontweight='bold')
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

