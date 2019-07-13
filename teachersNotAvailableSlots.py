#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 01:32:46 2019

@author: ajit
"""
import pickle
instructorSetPickle = open('instructorSet.pickle','rb')
instructorSet = pickle.load(instructorSetPickle) 


import xlrd
instructorsOnCampus = set()
instructorsOnCampusFile = "InstructorsOnCampus.xlsx"
wb = xlrd.open_workbook(instructorsOnCampusFile) 
sheet = wb.sheet_by_index(0) # get first sheet
for i in range(1,sheet.nrows):    
    instructorsOnCampus.add(sheet.cell_value(i,0))

        
teachersNotAvailalbeSlots = {
        'Divya  Shrivastava[20500160]':{'8to9': False, '9to10': False,'5to6': False},
        'Ajit  Kumar[20500008]':{'8to9': False, '9to10': False,'5to6': False},
        'Ranendra Narayan Biswas[20500321]': {'8to9': True, 
                                '5to6': True,
                                '1to2': False},
        'Rohit  Singh[20501073]': {'8to9': True, 
                                '5to6': True,
                                '1to2': False},
        'Upendra Kumar Pandey[20501071]': {'8to9': True, 
                                '5to6': True,
                                '1to2': False},
        'Sonal  Singhal[20500080]': {'1to2': False},
        'Ashish  Gupta[20500190]': {'5to6': True}
        }

eightToNineXML = '<Not_Available_Time>\n\
		<Day>M</Day>\n\
		<Hour>08:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>M</Day>\n\
		<Hour>08:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>T</Day>\n\
		<Hour>08:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>T</Day>\n\
		<Hour>08:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>W</Day>\n\
		<Hour>08:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>W</Day>\n\
		<Hour>08:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>Th</Day>\n\
		<Hour>08:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>Th</Day>\n\
		<Hour>08:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>F</Day>\n\
		<Hour>08:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>F</Day>\n\
		<Hour>08:30</Hour>\n\
	</Not_Available_Time>\n'

nineToTenXML = '<Not_Available_Time>\n\
		<Day>M</Day>\n\
		<Hour>09:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>M</Day>\n\
		<Hour>09:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>T</Day>\n\
		<Hour>09:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>T</Day>\n\
		<Hour>09:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>W</Day>\n\
		<Hour>09:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>W</Day>\n\
		<Hour>09:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>Th</Day>\n\
		<Hour>09:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>Th</Day>\n\
		<Hour>09:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>F</Day>\n\
		<Hour>09:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>F</Day>\n\
		<Hour>09:30</Hour>\n\
	</Not_Available_Time>\n'

fiveToSixXML = '<Not_Available_Time>\n\
		<Day>M</Day>\n\
		<Hour>17:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>M</Day>\n\
		<Hour>17:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>T</Day>\n\
		<Hour>17:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>T</Day>\n\
		<Hour>17:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>W</Day>\n\
		<Hour>17:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>W</Day>\n\
		<Hour>17:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>Th</Day>\n\
		<Hour>17:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>Th</Day>\n\
		<Hour>17:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>F</Day>\n\
		<Hour>17:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>F</Day>\n\
		<Hour>17:30</Hour>\n\
	</Not_Available_Time>\n'


lunchXML = '<Not_Available_Time>\n\
		<Day>M</Day>\n\
		<Hour>13:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>M</Day>\n\
		<Hour>13:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>T</Day>\n\
		<Hour>13:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>T</Day>\n\
		<Hour>13:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>W</Day>\n\
		<Hour>13:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>W</Day>\n\
		<Hour>13:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>Th</Day>\n\
		<Hour>13:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>Th</Day>\n\
		<Hour>13:30</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>F</Day>\n\
		<Hour>13:00</Hour>\n\
	</Not_Available_Time>\n\
	<Not_Available_Time>\n\
		<Day>F</Day>\n\
		<Hour>13:30</Hour>\n\
	</Not_Available_Time>\n'


x = ''
for i in instructorSet:
    
    availableIn8to9 = False
    availableIn9to10 = True
    availableIn5to6 = False
    availableIn1to2 = True 
    iOnCampus = False
    
    for j in instructorsOnCampus:
        if j[-10:] == i[-10:]:
            iOnCampus = True
            continue
            
    if iOnCampus:
        availableIn8to9 = False # remove this
        availableIn5to6 = False
        
        
    if i in teachersNotAvailalbeSlots:
        if '8to9' in teachersNotAvailalbeSlots[i]:
            availableIn8to9 = teachersNotAvailalbeSlots[i]['8to9']
        if '9to10' in teachersNotAvailalbeSlots[i]:
            availableIn9to10 = teachersNotAvailalbeSlots[i]['9to10']
        if '5to6' in teachersNotAvailalbeSlots[i]:
            availableIn5to6 = teachersNotAvailalbeSlots[i]['5to6']
        if '1to2' in teachersNotAvailalbeSlots[i]:
            availableIn1to2 = teachersNotAvailalbeSlots[i]['1to2']
            

    numSlots=0
    notSlots = ''
    if not availableIn8to9:
        numSlots = numSlots + 10
        notSlots = notSlots + eightToNineXML
    if not availableIn9to10:
        numSlots = numSlots + 10
        notSlots = notSlots + nineToTenXML
    if not availableIn5to6:
        numSlots = numSlots + 10
        notSlots = notSlots + fiveToSixXML
    if not availableIn1to2:
        numSlots = numSlots + 10
        notSlots = notSlots + lunchXML
            
    # teacher not available slot
    xi = "<ConstraintTeacherNotAvailableTimes>\n\
	<Weight_Percentage>100</Weight_Percentage>\n\
	<Teacher>"+i+"</Teacher>\n\
	<Number_of_Not_Available_Times>"+str(numSlots)+"</Number_of_Not_Available_Times>\n"
    
    xi = xi + notSlots
    xi = xi + "	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintTeacherNotAvailableTimes>\n"
    x = x+xi
        

        
