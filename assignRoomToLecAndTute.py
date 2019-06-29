#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 00:32:41 2019

@author: ajit
"""

# import slots and courses list from COS2FET
import pickle
coursesPickle = open('courses.pickle','rb')
courses = pickle.load(coursesPickle) 

slotsPickle = open('slots.pickle','rb')
slots = pickle.load(slotsPickle)


##----------------------------------------
#read exported csv format of the latest timetable

import csv
with open('csv/snu-timetable/snu-timetable_timetable.csv', 'r') as ff:
  reader = csv.reader(ff)
  activities = list(reader)
 
activitiesTime = dict()  
  
for a in activities:
    if a[0] not in activitiesTime:
        activitiesTime[a[0]] = dict()
        activitiesTime[a[0]][a[1]] = []
        activitiesTime[a[0]][a[1]].append(a[2])
    elif a[1] not in activitiesTime[a[0]]:
        activitiesTime[a[0]][a[1]] = []
        activitiesTime[a[0]][a[1]].append(a[2])
    else:
        activitiesTime[a[0]][a[1]].append(a[2])

  ##----------------------------------------
#read roomsAndBuildingFile
with open('rooms_and_buildings.csv', 'r') as ff:
  reader = csv.reader(ff)
  roomsAndBuilding = list(reader)

rooms = dict()



for r in roomsAndBuilding[1:]:
    rooms[r[0]] = dict()
    rooms[r[0]]['capacity'] = int(r[1])
    rooms[r[0]]['slots'] = dict()    
    days = ['M', 'T', 'W', 'Th', 'F']
    for d in days:
        rooms[r[0]]['slots'][d] = dict()
        for s in slots:
            rooms[r[0]]['slots'][d][s] = 'available'
          

# set lecture capacity for each lecture sections
for c in courses:
    if 'lecSections' in courses[c]:
        courses[c]['lecCapacity'] = int(int(courses[c]['CourseCapacity'])/len(courses[c]['lecSections']))
    else:
        courses[c]['lecCapacity'] = courses[c]['CourseCapacity']
    
# sort according to capacity 
# gives list
coursesList = sorted(courses.items(), key = lambda x: x[1]['lecCapacity'], reverse=True)    
# make it dictionary again
courses = dict()
for c in coursesList:
    courses[c[0]] = c[1]

# sort rooms accorig to size
# gives list
roomsList = sorted(rooms.items(), key = lambda x: x[1]['capacity'], reverse=False)

# make it into dictionry again
rooms = dict()
for r in roomsList:
    rooms[r[0]] = r[1]
    

# start filling in rooms for each of the lecture sections
# start from the biggest lecures and fit it in the smallest possible room
for ci in courses:
    c = courses[ci]
    if 'lecSections' in c:
        for li in c['lecSections']:
            lecTimes = {}
            l = c['lecSections'][li]
            lecIds = l['ids']
            for i in lecIds:
                x = activitiesTime[str(i)]
                for t in x:
                    lecTimes[t] = x[t]
            courses[ci]['lecSections'][li]['timings'] = lecTimes 
            # lecTimes is a dictionary holding information for all the times this lecture is happening
            # find the smallest rooms that fits this lecture capacity and is available
            lecCapacity = c['lecCapacity']
            # pretend that lecCapacity for MAT103 is 300
            if (lecCapacity > 300):
                lecCapacity = 300
            lecRoom = 'no room'
            roomAssigned = False
            for r in rooms:
                if not roomAssigned:
                    roomCapacity = rooms[r]['capacity']
                    # check for room capacity
                    if (lecCapacity <= roomCapacity):
                        # check if available
                        isRoomAvailable = True
                        for d in lecTimes: # loop over lec days 
                            for s in lecTimes[d]: # loop over lec times
                                if (rooms[r]['slots'][d][s] != 'available'):
                                    isRoomAvailable = False
                        # take the room if available
                        if isRoomAvailable:
                            lecRoom = r
                            courses[ci]['lecSections'][li]['room'] = lecRoom
                            roomAssigned = True
                            # mark non availability this room in these slots
                            for d in lecTimes: # loop over lec days 
                                for s in lecTimes[d]: # loop over lec times
                                    rooms[r]['slots'][d][s] = ci+'L'

    if 'tutSections' in c:
        for li in c['tutSections']:
            lecTimes = {}
            l = c['tutSections'][li]
            lecIds = l['ids']
            for i in lecIds:
                x = activitiesTime[str(i)]
                for t in x:
                    lecTimes[t] = x[t]
            courses[ci]['tutSections'][li]['timings'] = lecTimes
            # lecTimes is a dictionary holding information for all the times this lecture is happening
            # find the smallest rooms that fits this lecture capacity and is available
            lecCapacity = c['lecCapacity']
            # pretend that lecCapacity for MAT103 is 300
            lecCapacity = min(30, lecCapacity)
            lecRoom = 'no room'
            roomAssigned = False
            for r in rooms:
                if not roomAssigned:
                    roomCapacity = rooms[r]['capacity']
                    # check for room capacity
                    if (lecCapacity <= roomCapacity):
                        # check if available
                        isRoomAvailable = True
                        for d in lecTimes: # loop over lec days 
                            for s in lecTimes[d]: # loop over lec times
                                if (rooms[r]['slots'][d][s] != 'available'):
                                    isRoomAvailable = False
                        # take the room if available
                        if isRoomAvailable:
                            lecRoom = r
                            courses[ci]['tutSections'][li]['room'] = lecRoom
                            roomAssigned = True
                            # mark non availability this room in these slots
                            for d in lecTimes: # loop over lec days 
                                for s in lecTimes[d]: # loop over lec times
                                    rooms[r]['slots'][d][s] = ci+'T'
            if not roomAssigned:
                print('fucked')
                                    
                        
    if 'labSections' in c:
        for li in c['labSections']:
            lecTimes = {}
            l = c['labSections'][li]
            
            if 'ids' not in l: # ignore project courses
                continue
            
            lecIds = l['ids']
            for i in lecIds:
                x = activitiesTime[str(i)]
                for t in x:
                    lecTimes[t] = x[t]
            courses[ci]['labSections'][li]['timings'] = lecTimes
                        
            
# lets write down the time table in excel
def formatTime(slotsList):
    lastSlot = slotsList[-1]
    bhh= slotsList[0][0:2]
    bhh = str(int(bhh))
    bmm = slotsList[0][-2:]
    ehh= slotsList[-1][0:2]
    ehh = str(int(ehh))
    emm = slotsList[-1][-2:]
    if emm == '00':
        emm = '30'
    elif (emm == '30'):
        emm = '00'
        ehh=str(int(ehh)+1)
    return bhh+':'+bmm+'-'+ehh+':'+emm
        
# record popular choices
# import xlsxwriter module 
import xlsxwriter 
row = 0
workbook = xlsxwriter.Workbook('timeTable-SNU-Fall2019.xlsx') 
worksheet = workbook.add_worksheet()
for ci in courses:
    c = courses[ci]
    
    codeCol = 0
    meetingType = 1 # lec,tut,prac
    timeCol = 2
    instructorCol = 3
    studentCol = 4
    roomCol = 5
    
    
    if 'lecSections' in c:
        for li in c['lecSections']:
            if 'timings' in c['lecSections'][li]:
                time = ''
                for t in c['lecSections'][li]['timings']:
                    time = time+t+'('+formatTime(c['lecSections'][li]['timings'][t])+'),'
                time = time[0:-1]
                
                room = c['lecSections'][li]['room']
                instructor = ''
                for i in c['lecSections'][li]['instructors']:
                    instructor = instructor+i+','
                instructor = instructor[0:-1]
                
                studentSet = ''
                for s in c['lecSections'][li]['students']:
                    studentSet = studentSet+s+','
                studentSet = studentSet[0:-1]
                
                worksheet.write(row, codeCol, ci)
                worksheet.write(row, meetingType, li)
                worksheet.write(row, timeCol, time)
                worksheet.write(row, instructorCol, instructor)
                worksheet.write(row, studentCol, studentSet)
                worksheet.write(row, roomCol, room)
                
                row = row+1
                
    if 'tutSections' in c:
        for li in c['tutSections']:
            if 'timings' in c['tutSections'][li]:
                time = ''
                for t in c['tutSections'][li]['timings']:
                    time = time+t+'('+formatTime(c['tutSections'][li]['timings'][t])+'),'
                time = time[0:-1]
                
                room = c['tutSections'][li]['room']
                instructor = ''
                for i in c['tutSections'][li]['instructors']:
                    instructor = instructor+i+','
                instructor = instructor[0:-1]
                
                studentSet = ''
                for s in c['tutSections'][li]['students']:
                    studentSet = studentSet+s+','
                studentSet = studentSet[0:-1]
                
                worksheet.write(row, codeCol, ci)
                worksheet.write(row, meetingType, li)
                worksheet.write(row, timeCol, time)
                worksheet.write(row, instructorCol, instructor)
                worksheet.write(row, studentCol, studentSet)
                worksheet.write(row, roomCol, room)
                
                row = row+1
                
    if 'labSections' in c:
        for li in c['labSections']:
            if 'timings' in c['labSections'][li]:
                time = ''
                for t in c['labSections'][li]['timings']:
                    time = time+t+'('+formatTime(c['labSections'][li]['timings'][t])+'),'
                time = time[0:-1]
                
                room = c['labSections'][li]['room']
                instructor = ''
                for i in c['labSections'][li]['instructors']:
                    instructor = instructor+i+','
                instructor = instructor[0:-1]
                
                studentSet = ''
                for s in c['labSections'][li]['students']:
                    studentSet = studentSet+s+','
                studentSet = studentSet[0:-1]
                
                worksheet.write(row, codeCol, ci)
                worksheet.write(row, meetingType, li)
                worksheet.write(row, timeCol, time)
                worksheet.write(row, instructorCol, instructor)
                worksheet.write(row, studentCol, studentSet)
                worksheet.write(row, roomCol, room)
                
                row = row+1
workbook.close()                         
                    
            
            
    
    
    

    







