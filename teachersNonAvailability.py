#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 23:36:14 2019

@author: ajit
"""

import pickle
instructorSetPickle = open('instructorSet.pickle','rb')
instructorSet = pickle.load(instructorSetPickle) 


slotsPickle = open('slots.pickle','rb')
slots = pickle.load(slotsPickle)

days = ['M','T','W','Th','F']

import xlrd
instructorsOnCampus = set()
instructorsOnCampusFile = "InstructorsOnCampus.xlsx"
wb = xlrd.open_workbook(instructorsOnCampusFile) 
sheet = wb.sheet_by_index(0) # get first sheet
for i in range(1,sheet.nrows):    
    instructorsOnCampus.add(sheet.cell_value(i,0))

        
teachersNotAvailalbeSlots = {
        'Divya  Shrivastava[20500160]':['08:00','08:30','09:00','09:30','17:00','17:30'],
        'Ajit  Kumar[20500008]':['08:00','08:30','09:00','09:30','17:00','17:30'],
        'Ranendra Narayan Biswas[20500321]': ['13:00','13:30'],
        'Rohit  Singh[20501073]': ['13:00','13:30'],
        'Upendra Kumar Pandey[20501071]': ['13:00','13:30'],
        'Sonal  Singhal[20500080]': ['08:00','08:30','13:00','13:30','17:00','17:30'],
        'Ashish  Gupta[20500190]': ['08:00','08:30'],
        'Sumit Tiwari': ['13:00','13:30'],
        'harpreet  Singh Grewal[20500440]':['08:00','08:30','09:00','09:30','17:00','17:30'],
        'Biswajit Guchhait' : ['08:00','08:30'],
        'N.  Sukumar[20500050]': ['08:00','08:30'],
        'Kshatresh Dutta Dubey[20501049]': ['08:00','08:30'],
        }

teachersNotAvailalbeDays = {
        'Sanjeev  Agrawal[20500033]' : ['M']
        }

genNonAvailability = {'M':['08:00', '08:30', '17:00', '17:30'],
                      'T':['08:00', '08:30', '17:00', '17:30'],
                      'W':['08:00', '08:30', '17:00', '17:30'],
                      'Th':['08:00', '08:30', '17:00', '17:30'],
                      'F':['08:00', '08:30', '17:00', '17:30']}

onCampusNonAvailability = {'M':['08:00', '08:30'],
                      'T':['08:00', '08:30' ],
                      'W':['08:00', '08:30'],
                      'Th':['08:00', '08:30'],
                      'F':['08:00', '08:30']}
        
import copy
x = ''
for i in instructorSet:
        
    iNonAvailability = copy.deepcopy(genNonAvailability)
    
    for j in instructorsOnCampus:
        if j[-10:] == i[-10:]:
            iNonAvailability = copy.deepcopy(onCampusNonAvailability)
            continue
    
    # tweak iNonAvailability slots
    if i in teachersNotAvailalbeSlots:
        for d in ['M','T','W','Th','F']:
            iNonAvailability[d] = teachersNotAvailalbeSlots[i]
            
    # add whole slots on non availalbe days
    if i in teachersNotAvailalbeDays:
        for d in teachersNotAvailalbeDays[i]:
            iNonAvailability[d] = slots
            
    numSlots = 0
    slotsXML = ''
    for d in iNonAvailability:
        numSlots = numSlots +len(iNonAvailability[d])
        for s in iNonAvailability[d]:
            slotsXML = slotsXML+ '\t<Not_Available_Time>\n\t\t<Day>'+d+'</Day>\n\t\t<Hour>'+s+'</Hour>\n\t</Not_Available_Time>\n'
        
        # teacher not available slot
    xi = "<ConstraintTeacherNotAvailableTimes>\n\
	<Weight_Percentage>100</Weight_Percentage>\n\
	<Teacher>"+i+"</Teacher>\n\
	<Number_of_Not_Available_Times>"+str(numSlots)+"</Number_of_Not_Available_Times>\n"
    
    xi = xi + slotsXML
    xi = xi + "	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintTeacherNotAvailableTimes>\n"
    x = x+xi
        
