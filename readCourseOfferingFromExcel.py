#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:49:44 2019

@author: ajit
"""

from readMajorMinorPreferences import *

# Reading an excel file using Python 
import xlrd # Ajit: panda can also be used for excel reading
# load course offering file
  
filePath = "testData/Offered_Course_List_spring2019.xlsx"
wb = xlrd.open_workbook(filePath) 
sheet = wb.sheet_by_index(0) # get first sheet
  
# column heading numbers
School	=	0
Department	=	1
CourseCode	=	2
CourseTitle	=	3
Credits	=	4
CourseType	=	5
OpenasUWE	=	6
PartofMinoras	=	7
Programs	=	[8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
CourseCapacity	=	18
LectureHoursPerWeek	=	19
TutorialHoursPerWeek	=	20
PracticalHoursPerWeek	=	21
LectureDuration	=	22
LectureSections	=	23
TutorialSections	=	24
PracticalSections	=	25
LectureInstructors	=	26
TutorialInstructors	=	27
PracticalInstructors	=	28
LabRoomNumber	=	29
LabCapacity	=	30
SpecialRequirement	=	31
LectureSlottedoutsideMonFriand95	=	32
TutorialSlottedoutsideMonFriand95	=	33
PracticalSlottedoutsideMonFriand95	=	34
LectureRemarks	=	35
TutorialRemarks	=	36
PracticalRemarks	=	37
CourseCoordinator	=	38
LectureCredits	=	39
TutorialCredits	=	40
PracticalCredits	=	41
AssessmentTypeWeightage	=	42
CrossListedwith	=	43
Prerequisite	=	44
Crosslistedcourseoffered	=	45
Lasttimeofferedsemester	=	46





courseList = dict()

for i in range(1,sheet.nrows):
    
    
    # loop over courseCode column, make a dictionary for each course
    # if a cell in this column is empty, that means that row has details of 
    # last defined course code
    
    # skip over empty cells 
    if (sheet.cell_type(i,CourseCode) == xlrd.XL_CELL_EMPTY):
        continue
        
    j = 0 # How many EXTRA rows for a particular course
    if ((i+j+1) < sheet.nrows):
        while (sheet.cell_type(i+j+1,CourseCode) == xlrd.XL_CELL_EMPTY):
            j = j+1
       
    cCode = sheet.cell_value(i,CourseCode)

    courseList[cCode] = dict()
    
    courseI = courseList[cCode]
    courseI['Credits'] = int(sheet.cell_value(i,Credits))
    courseI['Title'] = sheet.cell_value(i,CourseTitle)
    courseI['CourseType'] = sheet.cell_value(i,CourseType)
    
    if (courseI['CourseType'] != 'CCC'):
        courseI['level'] = cCode[-3]
    else:
        courseI['level'] = 0
    
    courseI['OpenasUWE'] = sheet.cell_value(i,OpenasUWE)
    courseI['PartofMinoras'] = sheet.cell_value(i,PartofMinoras)
    
    
    # read target audience of the course
    courseI['programs'] = dict()
    for p in Programs:
        if (sheet.cell_type(i,p) != xlrd.XL_CELL_EMPTY):
            cellVal = sheet.cell_value(i,p)
            cellVal = sName[cellVal[:-1]]+cellVal[-1]
            courseI['programs'][cellVal] = studentsGroup[cellVal]['number']
            
    # read number lecture hours    
    if (sheet.cell_type(i,LectureHoursPerWeek) == xlrd.XL_CELL_EMPTY):
        courseI['LectureHoursPerWeek']=0
    else:
        courseI['LectureHoursPerWeek']=int(2*float(sheet.cell_value(i,LectureHoursPerWeek)))
        courseI['LectureDuration']=int(2*float(sheet.cell_value(i,LectureDuration)))
        
        
        
    #read number of tutorials hours
    if (sheet.cell_type(i,TutorialHoursPerWeek) == xlrd.XL_CELL_EMPTY):
        courseI['TutorialHoursPerWeek']=0
    else:
        courseI['TutorialHoursPerWeek']=int(2*float(sheet.cell_value(i,TutorialHoursPerWeek)))
        
    #read number of lab hours
    if (sheet.cell_type(i,PracticalHoursPerWeek) == xlrd.XL_CELL_EMPTY):
        courseI['PracticalHoursPerWeek']=0
    else:
        courseI['PracticalHoursPerWeek']=int(2*float(sheet.cell_value(i,PracticalHoursPerWeek)))
        
    # read lecture sections and respective instructors
    if (courseI['LectureHoursPerWeek'] >= 1):
        
        courseI['lecSections'] = dict()
        if (j == 0):
            seci = 'LEC1'
            courseI['lecSections'][seci] = dict()
            courseI['lecSections'][seci]['instructors'] = sheet.cell_value(i,LectureInstructors).split(',\n')[:-1]
            courseI['lecSections'][seci]['students'] = set()
        else:
            for k in range(i,i+j+1):
                if (sheet.cell_type(k,LectureSections) != xlrd.XL_CELL_EMPTY):
                    seci = sheet.cell_value(k,LectureSections)
                    courseI['lecSections'][seci] = dict()
                    courseI['lecSections'][seci]['instructors'] = sheet.cell_value(k,LectureInstructors).split(',\n')[:-1]
                    courseI['lecSections'][seci]['students'] = set()
         
            
    # read tut sections and respective instructors
    
    if (courseI['TutorialHoursPerWeek'] >= 1):
        courseI['tutSections'] = dict()
        
        if (j == 0) :
            seci = 'TUT1'
            courseI['tutSections'][seci] = dict()
            courseI['tutSections'][seci]['instructors'] = sheet.cell_value(i,TutorialInstructors).split(',\n')[:-1]
            courseI['tutSections'][seci]['students'] = set()
        else:
            for k in range(i,i+j+1):
                if (sheet.cell_type(k,TutorialSections) != xlrd.XL_CELL_EMPTY):
                    seci = sheet.cell_value(k,TutorialSections)
                    courseI['tutSections'][seci] = dict()
                    courseI['tutSections'][seci]['instructors'] = sheet.cell_value(k,TutorialInstructors).split(',\n')[:-1]
                    courseI['tutSections'][seci]['students'] = set()
            

    # read Lab sections, respective instructors, and lab room number
    if (courseI['PracticalHoursPerWeek'] >= 1):
       courseI['labSections'] = dict()
       if (j == 0):
           praci = 'PRAC1'
           courseI['labSections'][praci] = dict()
           courseI['labSections'][praci]['instructors'] =  sheet.cell_value(i,PracticalInstructors).split(',\n')[:-1]
           courseI['labSections'][praci]['students'] =  set()
           courseI['labSections'][praci]['room'] =  sheet.cell_value(i,LabRoomNumber) 
           courseI['labSections'][praci]['students'] = set()
            
       else:
           for k in range(i,i+j+1):
               if (sheet.cell_type(k,PracticalSections) != xlrd.XL_CELL_EMPTY):
                    praci = sheet.cell_value(k,PracticalSections)
                    courseI['labSections'][praci] = dict()
                    courseI['labSections'][praci]['instructors'] =  sheet.cell_value(k,PracticalInstructors).split(',\n')[:-1]
                    courseI['labSections'][praci]['room'] =  sheet.cell_value(k,LabRoomNumber)
                    courseI['labSections'][praci]['students'] = set()
        
    
    
        
        
    


