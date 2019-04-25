#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:13:28 2019

@author: ajit
"""

import pandas as pd 
import xlrd as xl 
from pandas import ExcelWriter
from pandas import ExcelFile 

xl=pd.read_excel("testData/dataFromZia.xls")

df = pd.DataFrame(xl)

i = 0
for courseCode in df['Course Code'].fillna(''): # fill empty cells with ''
    
    if (courseCode != ''):                      # loop over 
        numTut = (df['Tutorial Hours Per Week'].fillna('')[i])
        if (numTut):
            tutIntstrctors = [];
            numTut = int(numTut)
            
            for j in range(numTut):
                tutIntstrctors.append(df['Tutorial Instructors'].fillna('')[i+j][:-2])
            
            print (tutIntstrctors)
            print(numTut)
    i = i +1    