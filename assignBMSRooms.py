#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 18:14:41 2019

@author: ajit
"""

#read latest rooms availability
import pickle, xlrd
roomsPickle = open('roomsAvailability.pickle','rb')
rooms = pickle.load(roomsPickle) 

# read BMS course sheet
courses = dict()
roomFile = "BMS_Schedule.xlsx"
wb = xlrd.open_workbook(roomFile) 
sheet = wb.sheet_by_index(0) # get first sheet

mTimeCol = 10 
tTimeCol = 11
wTimeCol = 12
thTimeCol = 13
fTimeCol = 14
sTimeCol = 15


for i in range(1,sheet.nrows):
    cCode = sheet.cell_value(i,0)
    
    if cCode not in courses:
        courses[cCode] = dict()

    
    
    timings = dict()
    
    if  (sheet.cell_type(i,mTimeCol) != xlrd.XL_CELL_EMPTY):
        timings['M'] = sheet.cell_value(i,mTimeCol).split(',')
    if  (sheet.cell_type(i,tTimeCol) != xlrd.XL_CELL_EMPTY):
        timings['T'] = sheet.cell_value(i,tTimeCol).split(',')
    if  (sheet.cell_type(i,wTimeCol) != xlrd.XL_CELL_EMPTY):
        timings['W'] = sheet.cell_value(i,wTimeCol).split(',')
    if  (sheet.cell_type(i,thTimeCol) != xlrd.XL_CELL_EMPTY):
        timings['Th'] = sheet.cell_value(i,thTimeCol).split(',')
    if  (sheet.cell_type(i,fTimeCol) != xlrd.XL_CELL_EMPTY):
        timings['F'] = sheet.cell_value(i,fTimeCol).split(',')
    if  (sheet.cell_type(i,sTimeCol) != xlrd.XL_CELL_EMPTY):
        timings['S'] = sheet.cell_value(i,sTimeCol).split(',')
    
    
    ltp = sheet.cell_value(i,1)
    
    if 'LEC' in ltp:
        if 'lecSections' not in courses[cCode]:
            courses[cCode]['lecSections'] = dict()
            courses[cCode]['students'] = sheet.cell_value(i,8)
            courses[cCode]['openAsUWE'] = sheet.cell_value(i,9)
            courses[cCode]['courseCapacity'] = int(sheet.cell_value(i,6))
            
        courses[cCode]['lecSections'][ltp] = dict()
        courses[cCode]['lecSections'][ltp]['timings'] = timings 
        courses[cCode]['lecSections'][ltp]['instructors'] = sheet.cell_value(i,3)
        
        
    if 'TUT' in ltp:
        if 'tutSections' not in courses[cCode]:
            courses[cCode]['tutSections'] = dict()
        courses[cCode]['tutSections'][ltp] = dict()
        courses[cCode]['tutSections'][ltp]['timings'] = timings 
        courses[cCode]['tutSections'][ltp]['instructors'] = sheet.cell_value(i,3)
        
    if 'PRAC' in ltp:
        if 'labSections' not in courses[cCode]:
            courses[cCode]['labSections'] = dict()
        courses[cCode]['labSections'][ltp] = dict()
        courses[cCode]['labSections'][ltp]['timings'] = timings 
        courses[cCode]['labSections'][ltp]['instructors'] = sheet.cell_value(i,3)
        
            
# assign rooms
for ci in courses:
    c = courses[ci]
    biometricRoomNeeded = False
    if (ci[3] == '1' or ci[3] == '0'):
        biometricRoomNeeded = True
    
    if 'lecSections' in c:
        for li in c['lecSections']:
            lecTimes = courses[ci]['lecSections'][li]['timings']
            # lecTimes is a dictionary holding information for all the times this lecture is happening
            # find the smallest rooms that fits this lecture capacity and is available
            lecCapacity = c['courseCapacity']
            lecRoom = 'no room'
            roomAssigned = False
            for r in rooms:
                if biometricRoomNeeded and (not rooms[r]['isBiometric']):
                    continue
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
            if not roomAssigned:
                print(ci ,'lec, room not found')
                roomNotAssigned.append(ci)


    if 'tutSections' in c:
        for li in c['tutSections']:
            lecTimes = courses[ci]['tutSections'][li]['timings']
            # lecTimes is a dictionary holding information for all the times this lecture is happening
            # find the smallest rooms that fits this lecture capacity and is available
            lecCapacity = c['courseCapacity']
            # pretend that lecCapacity for MAT103 is 300
            lecRoom = 'no room'
            roomAssigned = False
            for r in rooms:
                if biometricRoomNeeded and (not rooms[r]['isBiometric']):
                    continue
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
                print(ci, 'tute, room not found')
                                    
                        
    if 'labSections' in c:
        for li in c['labSections']:
            lecTimes = courses[ci]['labSections'][li]['timings']
            # lecTimes is a dictionary holding information for all the times this lecture is happening
            # find the smallest rooms that fits this lecture capacity and is available
            lecCapacity = c['courseCapacity']
            # pretend that lecCapacity for MAT103 is 300
            lecRoom = 'no room'
            roomAssigned = False
            for r in rooms:
                if biometricRoomNeeded and (not rooms[r]['isBiometric']):
                    continue
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
                            courses[ci]['labSections'][li]['room'] = lecRoom
                            roomAssigned = True
                            # mark non availability this room in these slots
                            for d in lecTimes: # loop over lec days 
                                for s in lecTimes[d]: # loop over lec times
                                    rooms[r]['slots'][d][s] = ci+'T'
            if not roomAssigned:
                print(ci, 'tute, room not found')
    





# write in excel
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
        

def cleanInstructor(ins):
    x = ins.split('[')
    return x[0]
        
# record popular choices
# import xlsxwriter module 
import xlsxwriter 
workbook = xlsxwriter.Workbook('BMS-timeTable-SNU-Fall2019.xlsx') 
worksheet = workbook.add_worksheet()

row = 0
codeCol = 0
meetingType = 1 # lec,tut,prac
timeCol = 2
instructorCol = 3
studentCol = 4
roomCol = 5
capacityCol = 6
uweCol = 7

# header row
worksheet.write(row, codeCol, 'cCode')
worksheet.write(row, meetingType, 'LTP')
worksheet.write(row, timeCol, 'Time')
worksheet.write(row, instructorCol, 'Instructor')
worksheet.write(row, studentCol, 'Students')
worksheet.write(row, roomCol, 'Room')
worksheet.write(row, capacityCol, 'Course Capacity')
worksheet.write(row, uweCol, 'UWE?')


row = row+1

def sortedDays(times, cCode):
    
    # sort days
    x = dict()
    
    if 'M' in times:
        x['M'] = times['M']
    if 'T' in times:
        x['T'] = times['T']
    if 'W' in times:
        x['W'] = times['W']
    if 'Th' in times:
        x['Th'] = times['Th']
    if 'F' in times:
        x['F'] = times['F']
    if 'S' in times:
        x['S'] = times['S']
        
        
    days = list(x)
    D = ''
    hh = formatTime( times[days[0]])
    
    for d in days:
        if (times[d] != times[days[0]]):
            print(cCode, 'error', times)
            return(str(x))
        D = D+d
    
    x = D+' '+hh
    return(x)
    
for ci in courses:
    c = courses[ci]
    print(ci)
    if 'lecSections' in c:
        for li in c['lecSections']:
            if 'timings' in c['lecSections'][li]:
                time = sortedDays(c['lecSections'][li]['timings'],ci)
                
                room = ''
                if 'room' in c['lecSections'][li]:
                    room = c['lecSections'][li]['room']
                else:
                    room = 'TBA'
                
                instructor = c['lecSections'][li]['instructors']
                studentSet = c['students']
                cCapacity = c['courseCapacity']
                
                worksheet.write(row, codeCol, ci)
                worksheet.write(row, meetingType, li)
                worksheet.write(row, timeCol, time)
                worksheet.write(row, instructorCol, instructor)
                worksheet.write(row, studentCol, studentSet)
                worksheet.write(row, roomCol, room)
                worksheet.write(row, capacityCol, cCapacity)
                worksheet.write(row,uweCol,c['openAsUWE'])
                
                row = row+1
                
    if 'tutSections' in c:
        for li in c['tutSections']:
            if 'timings' in c['tutSections'][li]:
                time = sortedDays(c['tutSections'][li]['timings'],ci)
                
                room = c['tutSections'][li]['room']
                instructor = c['tutSections'][li]['instructors']
                studentSet = c['students']
                
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
                time = sortedDays(c['labSections'][li]['timings'],ci)
                
                room = c['labSections'][li]['room']
                instructor = c['labSections'][li]['instructors']
                studentSet = c['students']
                
                worksheet.write(row, codeCol, ci)
                worksheet.write(row, meetingType, li)
                worksheet.write(row, timeCol, time)
                worksheet.write(row, instructorCol, instructor)
                worksheet.write(row, studentCol, studentSet)
                worksheet.write(row, roomCol, room)
                
                row = row+1
workbook.close()                         


#save the instructor set for creating their non available slots
with open('roomsAvailability.pickle', 'wb') as f:
    pickle.dump(rooms, f)
