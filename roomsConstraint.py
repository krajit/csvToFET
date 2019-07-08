#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 00:48:34 2019

@author: ajit
"""
classRoomsConstraintTemplate = '<ConstraintActivityTagPreferredRooms>\n\
	<Weight_Percentage>100</Weight_Percentage>\n\
	<Activity_Tag>ACTIVITYTAG</Activity_Tag>\n\
	<Number_of_Preferred_Rooms>NUMBEROFROOMS</Number_of_Preferred_Rooms>\n\
    LISTOFPREFERREDROOMS\
	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintActivityTagPreferredRooms>\n'

import xlrd
roomFile = "RoomNumbers.xlsx"
wb = xlrd.open_workbook(roomFile) 
sheet = wb.sheet_by_index(0) # get first sheet

preferredRoomListXML = ''
n = 0
for i in range(1,sheet.nrows):
    r = sheet.cell_value(i,0)
    preferredRoomListXML = preferredRoomListXML + '\t<Preferred_Room>'+r+'</Preferred_Room>\n'
    n = n+1
    
LEC1SpaceCons = classRoomsConstraintTemplate.replace('ACTIVITYTAG','LEC1')
LEC1SpaceCons = LEC1SpaceCons.replace('NUMBEROFROOMS',str(n))
LEC1SpaceCons = LEC1SpaceCons.replace('LISTOFPREFERREDROOMS',preferredRoomListXML)
