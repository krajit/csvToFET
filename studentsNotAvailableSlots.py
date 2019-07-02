#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 00:35:43 2019

@author: ajit
"""

import pickle
studentGroupsPickle = open('studentGroups.pickle','rb')
studentGroups = pickle.load(studentGroupsPickle) 

studentsNotAvailableAfter5Template = "<ConstraintStudentsSetNotAvailableTimes>\n\
	<Weight_Percentage>100</Weight_Percentage>\n\
	<Students>GROUPNAME</Students>\n\
	<Number_of_Not_Available_Times>10</Number_of_Not_Available_Times>\n\
	<Not_Available_Time>\n\
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
	</Not_Available_Time>\n\
	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintStudentsSetNotAvailableTimes>\n" 

# only BIO1 needs to go beyond 5 pm
studentsNotAvailalbeAfter5XML = ''
for y in ['year2', 'year3', 'year4']:
    xi = studentsNotAvailableAfter5Template
    xi = xi.replace('GROUPNAME',y)
    studentsNotAvailalbeAfter5XML = studentsNotAvailalbeAfter5XML + xi
    
for y in studentGroups['year1']:
    if y != 'BIO1':
        xi = studentsNotAvailableAfter5Template
        xi = xi.replace('GROUPNAME',y)
        studentsNotAvailalbeAfter5XML = studentsNotAvailalbeAfter5XML + xi
    
    

    
    

