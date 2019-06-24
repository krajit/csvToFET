#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 13:20:24 2019

@author: ajit
"""

import xlrd

wb = xlrd.open_workbook('studentDatabase/SNU-electivesdata.xlsx') 
sheet = wb.sheet_by_index(0) # get first sheet

electives = dict()

for i in range(2,sheet.nrows):
    major = sheet.cell_value(i,1)
    electives[major] = dict()
    electives[major]['UWEpool'] = list(sheet.cell_value(i,27).split(','))
    electives[major]['numMajorElectives'] = dict()
    electives[major]['numUWE'] = dict()
    electives[major]['numCCC'] = dict()

    for j in range(2,24,3):
        semNum = int((j+1)/3)
        electives[major]['numMajorElectives']['Sem'+str(semNum)] = int(sheet.cell_value(i,j))
        electives[major]['numUWE']['Sem'+str(semNum)] = int(sheet.cell_value(i,j+1))
        electives[major]['numCCC']['Sem'+str(semNum)] = int(sheet.cell_value(i,j+2))
    

        
    
    
