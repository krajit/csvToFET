#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:14:43 2019

@author: ajit
"""

"17:00" "17:30" "18:00" "18:30" "19:00" "19:30"
import os, re
#----------------------------------------------------------------
simTimeLimit = 60

# import xlsxwriter module 
import xlsxwriter 
  
workbook = xlsxwriter.Workbook('report_T'+str(simTimeLimit)+'_seconds.xlsx') 
worksheet = workbook.add_worksheet() 

rowsDict = dict()

offset = 2

for numCCC in [0 , 1, 2]:
    for maxNumOfAllowedUWE in [0, 1, 2]:
        for numMajorElectives in [0, 1, 2]:
            
            rowi = str(numCCC)+str(maxNumOfAllowedUWE)+str(numMajorElectives)
            rowsDict[rowi] = offset
            offset = offset+1
            
colsDict = {'17:00':3, '17:30': 4, '18:00': 5, '18:30': 6, '19:00': 7, '19:30': 8}

for numCCC in [0 , 1, 2]:
    for maxNumOfAllowedUWE in [0, 1, 2]:
        for numMajorElectives in [0, 1, 2]:
            for w in ['17:00', '17:30', '18:00', '18:30', '19:00', '19:30']:
                reportFolder = 'terminalReports_Timelimit_'+str(simTimeLimit)+'_seconds/'
                logFile = 'znCCC_'+str(numCCC)+'_nUWE_'+str(maxNumOfAllowedUWE)+\
                '_nMajElecive_'+str(numMajorElectives)+'_'+w+''+'.log'
                
                logFilePath = reportFolder+logFile
                exists = os.path.isfile(logFilePath)
                if exists:
                    caseReport = open(logFilePath,"r").read()
                    
                    rowi = str(numCCC)+str(maxNumOfAllowedUWE)+str(numMajorElectives)
                    m = rowsDict[rowi]
                    n = colsDict[w]
                    
                    if 'Simulation successful' in caseReport:
                        
            
                        caseReport = caseReport.split('\n')[-3]
                        ti =  int(re.search(r'\d+', caseReport).group())
                        
                        
                    else:
                        caseReport = caseReport.split('\n')[-5:]
                        if 'Time exceeded' in caseReport[-2]:
                            ti = 'Time over'
                        elif  'aborting' in caseReport[-2]:
                            ti = 'impossible'
                        else:
                            ti = 'unknown error'
                            
                    worksheet.write(m,n, ti)


workbook.close() 