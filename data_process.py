##########
#  data_process.py : A Module file containing functions
#            Author: John J. Oh (NIMS)
#               2014. 5. 20 (Tue)
#                      v.1.0
###########
#  File Splitter: Split data column and class column in .ann file
#  Usage: from data_process import file_splitter
##
import numpy as np

def file_splitter(input_file, filename, output_dir):
    f=open(input_file,'r')
    i=0
    while 1:
        data=f.readline()
        if not data: break
        g=open(output_dir+'/'+filename+'_dat.txt','a')
        l=open(output_dir+'/'+filename+'_cls.txt','a')
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
    print "Writing processed data:"+filename+"_dat.txt"
    print "Writing Processed class:"+filename+"_cls.txt"


##
# Feature Remover: Removing Uncorrelated Features based on NMIFS
# and Generating Reduced .ann file
# Usage: from data_process import feat_remmover
##
def feat_remover(f, cls, s):
    rmf = range(0,len(f[0]))
    for i in range(len(s)):
        rmf.remove(s[i])
    print 'Uncorrelated Feature Index:', rmf
    for i in range(len(rmf)):
        f=np.delete(f.T,rmf[i]-i,0).T
    return f

##
# Removing Null Vectors
#
# 
###
def null_remover(input_txt, filename, output_dir):
    data=np.loadtxt(input_txt)
    for i in range(len(data)):
        temp=0.0
        k=open(output_dir+'/'+filename+'_reduced_null_rmvd_dat.txt','a')
        for j in range(len(data[i])):
            temp+=data[i][j]
        if temp == 0.0:
            pass
        else:
            for m in range(len(data[i])):
                k.write(str(data[i][m]))
                k.write(' ')
            k.write('\n')
        k.close()

##
# File Merger from _dat and _cls data to .ann
#
##
def file_merger(dat_file, cls_file, filename, output_dir):
    data2=np.loadtxt(dat_file)
    g=open(dat_file,'r')
    m=open(cls_file,'r')
    f=open(output_dir+'/'+filename+'_rmvd_null_reduced.ann','a')
    f.write(str(len(data2)))
    f.write(' ')
    f.write(str(len(data2[0])))
    f.write(' ')
    f.write('1')
    f.write('\n')
    while 1:
        rmv_dat=g.readline()
        cls=m.readline()
        if not rmv_dat: break
        f.write(rmv_dat[0:-1])
        f.write('\n')
        f.write(cls[0:-1])
        f.write('\n')
    f.close()
    m.close()
    g.close()

##
# Feature Normalization : individual normalization for each feature
#
##
def feat_normalize(data):
    for j in range(len(data[0])):
        dmax=max(data.T[j])
        dmin=min(data.T[j])
        for i in range(len(data)):
            if dmin < 0:
                data.T[j][i] = (data.T[j][i]+abs(dmin))/(dmax+abs(dmin))
            else:
                data.T[j][i] = (data.T[j][i]-abs(dmin))/(dmax+abs(dmin))
    return data

