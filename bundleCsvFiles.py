# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 23:25:05 2019

@author: Simon
"""

from glob import glob
import os

pwd="stores"
os.chdir(pwd)

with open('main.csv', 'a') as singleFile:
    for csv in glob('*.csv'):
        if csv == 'main.csv':
            pass
        else:
            for line in open(csv, 'r'):
                singleFile.write(line)