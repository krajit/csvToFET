#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:49:44 2019

@author: ajit
"""

# Reading an excel file using Python 
import xlrd # Ajit: panda can also be used for excel reading
# load course offering file
  
filePath = "testData/SNU - popular minors data survey (Responses).xlsx"
## NOTE: make sure to remove duplicate department rows manually

# excel files have rather long names, lets shorten them
sName = {
        'Chemical Engineering' : 'CHD',
        'Civil Engineering' : 'CED',
        'Computer Science and Engineering' : 'CSD',
        'Electrical Engineering' : 'EED',
        'Mechanical Engineering' : 'MED',
        'Art & Performing Art' : 'ADP',
        'Communication' : 'COM',
        'Design' : 'DES',
        'Economics' : 'ECO',
        'English' : 'ENG',
        'History' : 'HIS', 
        'International Relations and Governance Studies' : 'INT',
        'Sociology' : 'SOC',
        'Management': 'MGT',
        'Chemistry' : 'CHY',
        'Life Sciences' : 'BIO', 
        'Mathematics' : 'MAT',
        'Physics' : 'PHY',
        'Archaeology' : 'HIS', # TODO: check which dept offers history 
        'Biotechnology' : 'BIO',
        'Chemistry' : 'CHY',
        'Dance' : 'ADP',  # TODO: check which dept offers dance
        'Data Analytics': 'MGT', # TODO: check which dept offers data analytics
        'Electronics and Communication Engineering' : 'ECE',
        'International Relations and Public Affairs': 'INT',
        'Electrical and Electronics Engineering': 'EED',
        'International Relations': 'INT',
        'Art Design and Performing Arts': 'ADP',
        'Bachelor of Management Studies': 'MGT',
        'Under Graduate': 'UG',
        'OHM': 'MGT',
        'General Management': 'MGT',
        'FAC': 'MGT',
        'STM': 'MGT',
        'DOM': 'MGT'         
        }



wb = xlrd.open_workbook(filePath) 
sheet = wb.sheet_by_index(0) # get first sheet
  
deptCol = 3
popularMinor = dict() # major(students) and minors(dept)

for i in range(1,sheet.nrows):
    dept = sheet.cell_value(i,deptCol) # read dept names
    dept = sName[dept]                 # get short name for dept
    popularMinor[dept] = []
    
    for j in range(deptCol+1,deptCol+6):
        if (sheet.cell_type(i,j) != xlrd.XL_CELL_EMPTY):
            if (sheet.cell_value(i,j) != 'None'):
                popularMinor[dept].append(sName[sheet.cell_value(i,j)])
    
minorSeeker = dict()
numMinor = 2 # only first two pref are accounted for now. 
             # Change this value to 5 to include all pref

for i,dep in popularMinor.items():
    k = min(len(dep), numMinor)
    
    for j in range(k):
        if dep[j] in minorSeeker:
            minorSeeker[dep[j]].add(i)
        else:
            minorSeeker[dep[j]] = set()
            minorSeeker[dep[j]].add(i)
            
            
#            
#studentSet = {'BIO1',  'BIO2',  'BIO3',  'BIO4',  'CED1',  'CED2',  'CED3',  'CED4',
# 'CHD1',  'CHD2',  'CHD3',  'CHD4',  'CHY1',  'CHY2',  'CHY3',  'CHY4',
# 'CSD1',  'CSD2',  'CSD3',  'CSD4',  'ECE1',  'ECE2',  'ECE3',  'ECE4',
# 'ECO1',  'ECO2',  'ECO3',  'ECO4',  'EED1',  'EED2',  'EED3',  'EED4',
# 'ENG1',  'ENG2',  'ENG3',  'ENG4',  'HIS1',  'HIS2',  'HIS3',  'HIS4',  'INT1', 'INT2',
# 'MAT1',  'MAT2',  'MAT3',  'MAT4',  'MED1',  'MED2',  'MED3',  'MED4',
# 'MGT1',  'MGT2',  'MGT3',  'MGT4',  'PHY1',  'PHY2',  'PHY3',  'PHY4',
# 'SOC1',  'SOC2',  'SOC3',  'SOC4',  'UG1'}
#            
#            


wb = xlrd.open_workbook('testData/studentsData.xlsx') 
sheet = wb.sheet_by_index(0) # get first sheet
   
studentsGroup = dict()
for i in range(1,sheet.nrows):
    s = sheet.cell_value(i,0)
    n = int(sheet.cell_value(i,1))
    
    studentsGroup[s] = dict()
    studentsGroup[s]['number'] = n
    studentsGroup[s]['subgroups'] = {s+'NoMinor': n}
    

# make subgroups in studentGroup
# only in 2nd to 4th year
for sIndex, s in studentsGroup.items():
    
    y = sIndex[-1] #year
    d = sIndex[:-1] # dept
    
    # pass over first year students
    # TODO: Work on grouping first year studetns
    if (y == '1'):
        continue
    
    if d in popularMinor:
        n = min(len(popularMinor[d]),numMinor) # number of subgroups
        # weights
        # w1 + w2 + ... wn = 1
        # wi = i*a
        a = 2.0/(n*(n+1))
        for i in reversed(range(n)):
            wi = (i+1)*a
            ni = round(wi*int(s['number']))
            si = sIndex+popularMinor[d][i]
            s['subgroups'][si] = ni
            s['subgroups'][sIndex+'NoMinor'] = s['subgroups'][sIndex+'NoMinor'] - ni 
# end grouping students

# write subgroups in csv
            
studentToCsv = 'Year,Number of Students per Year,Group, Number of Students per Group,Subgroup, Number of Students per Subgroup\n'

for sIndex, s in studentsGroup.items():
    for sgIndex, sg in s['subgroups'].items():
        rowi = sIndex+','+str(s['number'])+','+sgIndex+','+ str(sg)+' , ,\n'
        
        #try without any subgroup
        #rowi = sIndex+','+str(s['number'])+','+''+','+ ''+' , ,\n'
        studentToCsv = studentToCsv + rowi
        
f = open("studentsGroup.csv", "w")
f.write(studentToCsv)
f.close()    
    

    
    
    
    
    
