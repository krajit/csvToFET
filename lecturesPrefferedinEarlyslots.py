#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 03:06:21 2019

@author: ajit
"""

prefSlotsXML = ''
prefSlots = ['09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30']
days = ['M','T','W','Th','F']

n = len(prefSlots)*len(days)
for d in days:
    for s in prefSlots:
        x = '	<Preferred_Time_Slot>\n\
		<Preferred_Day>'+d+'</Preferred_Day>\n\
		<Preferred_Hour>'+s+'</Preferred_Hour>\n\
	</Preferred_Time_Slot>\n'
        prefSlotsXML = prefSlotsXML + x
    


LEC1early = '<ConstraintActivitiesPreferredTimeSlots>\n\
	<Weight_Percentage>100</Weight_Percentage>\n\
	<Teacher_Name></Teacher_Name>\n\
	<Students_Name></Students_Name>\n\
	<Subject_Name></Subject_Name>\n\
	<Activity_Tag_Name>LargeClass</Activity_Tag_Name>\n\
	<Duration></Duration>\n\
	<Number_of_Preferred_Time_Slots>NUMSLOTS</Number_of_Preferred_Time_Slots>\n\
    PREFERREDTIMESLOTS\
	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintActivitiesPreferredTimeSlots>\n'

LEC1early = LEC1early.replace('NUMSLOTS', str(n))
LEC1early = LEC1early.replace('PREFERREDTIMESLOTS', prefSlotsXML)
