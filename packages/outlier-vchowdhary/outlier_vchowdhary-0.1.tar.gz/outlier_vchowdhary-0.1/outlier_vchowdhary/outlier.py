# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:53:32 2020

@author: Dell
"""

def detect_outlier(d):
     r1=d.shape[0] 
     q1=d.quantile(0.25)
     q3=d.quantile(0.75)
     iqr=q3-q1
     d=d[~((d<(q1-1.5*iqr))|(d>(q3+1.5*iqr))).any(axis=1)] #axis=1 means row
     r2=d.shape[0]
     x=r1-r2
     print('dataset after removing outlier:')
     print(d)
     print('number of rows removed :'+str(x))