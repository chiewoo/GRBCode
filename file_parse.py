#/usr/bin/python

import numpy as np
import math
import os

f=open('S5_coh_grb_GRB070923_NSBH10_H1L1V1_gann_rr10_wo_bestnr_0_evaluation.ann','r')
while 1:
    data=f.readline()
    if not data: break
    g=open('transformed.txt','a')
    l=open('transformedres.txt','a')
    if len(data)<10 and data[0]==str(2):
        pass
    elif len(data)<10:
        l.write(data[0:-1])
        l.write('\n')
    else:
        g.write(data[0:-1])
        g.write('\n')
    g.close()
    l.close()
f.close()
