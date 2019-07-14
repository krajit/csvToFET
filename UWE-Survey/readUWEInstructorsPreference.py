#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:58:37 2019

@author: ajit
"""
import xlrd, xlsxwriter 

wb = xlrd.open_workbook("UWE_offerings.xlsx") 
sheet = wb.sheet_by_index(0) # get first sheet

UWEcourses = dict()

for i in range(1,sheet.nrows):
    cCode = sheet.cell_value(i,0)[0:6]
    instructor = sheet.cell_value(i,3)
    title = sheet.cell_value(i,1)
    UWEcourses[cCode] = {'title': title, 'instructor': instructor}
    
    
# look into survey responses and delete code found in the responses
wb = xlrd.open_workbook("Survey of identifying UWEs target students (Responses).xlsx") 
sheet = wb.sheet_by_index(0) # get first sheet

for i in range(1,sheet.nrows):
    cCode = sheet.cell_value(i,2)[0:6]
    
    pref1 = ''
    pref2 = ''
    pref3 = ''
    
    if (sheet.cell_type(i,3) != xlrd.XL_CELL_EMPTY):
        pref1 = sheet.cell_value(i,3)
        UWEcourses[cCode]['pref1'] = pref1
    
    if (sheet.cell_type(i,4) != xlrd.XL_CELL_EMPTY):
        pref2 = sheet.cell_value(i,4)
        UWEcourses[cCode]['pref2'] = pref2
    
    if (sheet.cell_type(i,5) != xlrd.XL_CELL_EMPTY):
        pref3 = sheet.cell_value(i,5)
        UWEcourses[cCode]['pref3'] = pref3
                
     # second course if mentioned
    if (sheet.cell_type(i,6) != xlrd.XL_CELL_EMPTY):
        cCode = sheet.cell_value(i,6)[0:6]
        
        if (sheet.cell_type(i,7) != xlrd.XL_CELL_EMPTY):
            pref1 = sheet.cell_value(i,7)
            UWEcourses[cCode]['pref1'] = pref1

        
        if (sheet.cell_type(i,8) != xlrd.XL_CELL_EMPTY):
            pref2 = sheet.cell_value(i,8)
            UWEcourses[cCode]['pref2'] = pref2

            
        
        if (sheet.cell_type(i,9) != xlrd.XL_CELL_EMPTY):
            pref3 = sheet.cell_value(i,9)
            UWEcourses[cCode]['pref3'] = pref3

            
    
    
# write preferences of all UWE in an excel file
workbook = xlsxwriter.Workbook('UWEpreferredTargetAurdience.xlsx') 
worksheet = workbook.add_worksheet() 
        
worksheet.write(0, 0, 'cCode')
worksheet.write(0, 1, 'Title')
worksheet.write(0, 2, 'Instructor')
worksheet.write(0, 3, 'Pref 1')
worksheet.write(0, 4, 'Pref 2')
worksheet.write(0, 5, 'Pref 3')
row = 0

for cCode in UWEcourses:
    row = row+1
    worksheet.write(row, 0, cCode)
    worksheet.write(row, 1, UWEcourses[cCode]['title'])
    worksheet.write(row, 2, UWEcourses[cCode]['instructor'])
    
    if 'pref1' in UWEcourses[cCode]:
        worksheet.write(row, 3, UWEcourses[cCode]['pref1'])
        
    if 'pref2' in UWEcourses[cCode]:
        worksheet.write(row, 4, UWEcourses[cCode]['pref2'])
    
    if 'pref3' in UWEcourses[cCode]:
        worksheet.write(row, 5, UWEcourses[cCode]['pref3'])    
    
    


workbook.close() 

    