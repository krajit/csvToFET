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

# deflate instructor from CCC515
courses['CCC515']['lecSections']['LEC1']['instructors'] = courses['CCC515']['lecSections']['LEC1']['instructors'][0:1]

# copy CCC515 ids to all other CCC
for c in courses['CCC515']['overlapsWith']:
    courses[c]['lecSections']['LEC1']['ids'] = courses['CCC515']['lecSections']['LEC1']['ids']


slots = [
        '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00',
         '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
         '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', 
         '18:00', '18:30', '19:00', '19:30',
         ]


##----------------------------------------
#read exported csv format of the latest timetable
import csv
with open('csv/snu-timetable/snu-timetable_timetable.csv', 'r') as ff:
  reader = csv.reader(ff)
  activities = list(reader)
 
activitiesTime = dict()  

newCoursDict = dict()
numPracSection = dict()
prevLabStudents = ''
prevLabInstructors = ''
prevCcode = ''
  
for a in activities[1:]:
    if 'Lunch' in a:
        continue
    cCode = a[4]
    
    if cCode not in newCoursDict:
        newCoursDict[cCode] = dict()
        numPracSection[cCode] = 0
    
    ltp = a[6].split('+')[0]
    
    d = a[1]
    t = a[2]
    students = set(a[3].split('+'))
    if len(students) == 0:
        students = set()
    
    i = list(a[5].split('+'))
    if len(i) == 0:
        i = set()
    
    room = set()
    if 'LEC' in ltp:
        sectionType = 'lecSections'
    elif 'TUT' in ltp:
        sectionType = 'tutSections'
    else:
        sectionType = 'labSections'
        if (prevLabStudents != students) or (prevLabInstructors != i) or (prevCcode != cCode):
            numPracSection[cCode] = numPracSection[cCode] + 1
            room = ltp
        ltp = 'PRAC' + str(numPracSection[cCode])
        prevLabStudents = students
        prevLabInstructors = i
        prevCcode = cCode
        
    if sectionType not in newCoursDict[cCode]:
        newCoursDict[cCode][sectionType] = dict()
    if ltp not in newCoursDict[cCode][sectionType]:
        newCoursDict[cCode][sectionType][ltp] = dict()
        newCoursDict[cCode][sectionType][ltp]['instructors'] = i
        newCoursDict[cCode][sectionType][ltp]['room'] = room
    if 'students' not in newCoursDict[cCode][sectionType][ltp]:
        newCoursDict[cCode][sectionType][ltp]['students'] = students
    if 'timings' not in newCoursDict[cCode][sectionType][ltp]:
        newCoursDict[cCode][sectionType][ltp]['timings'] = dict()
    if d not in newCoursDict[cCode][sectionType][ltp]['timings']:
        newCoursDict[cCode][sectionType][ltp]['timings'][d] = []
        
    newCoursDict[cCode][sectionType][ltp]['timings'][d] = newCoursDict[cCode][sectionType][ltp]['timings'][d]+ [t]  
            
            
for ci in newCoursDict:
    newCoursDict[ci]['CourseCapacity'] = courses[ci]['CourseCapacity']
    newCoursDict[ci]['Title'] = courses[ci]['Title']
    
    
# add ccc courses in newCoursDict
# copy CCC515 ids to all other CCC
for c in courses['CCC515']['overlapsWith']:
    newCoursDict[c] =  courses[c]
    newCoursDict[c]['lecSections']['LEC1']['timings'] =  newCoursDict['CCC515']['lecSections']['LEC1']['timings']
    
   
coursesBackUp = courses
    
courses = newCoursDict



# set lecture capacity for each lecture sections
for c in courses:
    if 'lecSections' in courses[c]:
        courses[c]['lecCapacity'] = int(int(courses[c]['CourseCapacity'])/len(courses[c]['lecSections']))
    else:
        courses[c]['lecCapacity'] = courses[c]['CourseCapacity']
    
courses['ECO101']['lecCapacity'] = 90    

# sort according to capacity 
# gives list
coursesList = sorted(courses.items(), key = lambda x: x[1]['lecCapacity'], reverse=True)    
# make it dictionary again
courses = dict()
for c in coursesList:
    courses[c[0]] = c[1]
    
#-------------------------------------------------------------------
    
    
# read room inventory
import xlrd
rooms = dict()
roomFile = "RoomNumbers.xlsx"
wb = xlrd.open_workbook(roomFile) 
sheet = wb.sheet_by_index(0) # get first sheet
for i in range(1,sheet.nrows):
    r = sheet.cell_value(i,0)
    rooms[r] = dict()
    rooms[r]['capacity'] = int(sheet.cell_value(i,1))
    
    if int(sheet.cell_value(i,2)) == 1:
        rooms[r]['isBiometric'] = True
    else:
        rooms[r]['isBiometric'] = False
    
    rooms[r]['slots'] = dict()    
    days = ['M', 'T', 'W', 'Th', 'F','S']
    for d in days:
        rooms[r]['slots'][d] = dict()
        for s in slots:
            rooms[r]['slots'][d][s] = 'available'
    
#temporarily make D217 biometric
rooms['D217']['isBiometric'] = True

    
    

# sort rooms accorig to size
# gives list
roomsList = sorted(rooms.items(), key = lambda x: x[1]['capacity'], reverse=False)

# make it into dictionry again
rooms = dict()
for r in roomsList:
    rooms[r[0]] = r[1]

roomNotAssigned = []            

# start filling in rooms for each of the lecture sections
# start from the biggest lecures and fit it in the smallest possible room
def assignRooms(level = '1'):
    for ci in courses:
        c = courses[ci]
        biometricRoomNeeded = False
        if (ci[3] == '1' or ci[3] == '0'):
            biometricRoomNeeded = True
            
        if ci[3] not in level:
            continue
        
        if 'lecSections' in c:
            for li in c['lecSections']:
                lecTimes = courses[ci]['lecSections'][li]['timings']
                # lecTimes is a dictionary holding information for all the times this lecture is happening
                # find the smallest rooms that fits this lecture capacity and is available
                lecCapacity = c['lecCapacity']
                # pretend that lecCapacity for MAT103 is 300
                if (lecCapacity > 300):
                    lecCapacity = 300
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
                    print(ci,courses[ci]['lecCapacity'] ,'lec, room not found')
                    roomNotAssigned.append(ci)
    
    
        if 'tutSections' in c:
            for li in c['tutSections']:
                lecTimes = courses[ci]['tutSections'][li]['timings']
                # lecTimes is a dictionary holding information for all the times this lecture is happening
                # find the smallest rooms that fits this lecture capacity and is available
                lecCapacity = c['lecCapacity']
                # pretend that lecCapacity for MAT103 is 300
                lecCapacity = min(30, lecCapacity)
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
                
# assign rooms to  first year coures first to biometric rooms
assignRooms(level = '01')

# then assign higher level coureses to any rooms
assignRooms(level = '23456789')

#
courses['ECO101']['lecCapacity'] = 90

print('\n....')
print('Some rooms have not been assigned rooms. For these course, different days are getting mapped to different rooms...')
for ci in roomNotAssigned:
    
    # lec section 1
    lectureSlots = courses[ci]['lecSections']['LEC1']['timings']
    courses[ci]['lecSections']['LEC1']['room'] = ''
    
    for dayi in lectureSlots:
        dayiSlots = lectureSlots[dayi]
        roomAssigned = False
        
        for r in rooms:
            # skip is room is not big enough
            if rooms[r]['capacity'] < courses[ci]['lecCapacity']:
                continue
            
            isRoomAvailable = True
            for s in dayiSlots:
                if (rooms[r]['slots'][dayi][s] != 'available'):
                    isRoomAvailable = False
                    
            if isRoomAvailable:
                # make the room unavailalbe
                for s in dayiSlots:
                    rooms[r]['slots'][dayi][s] = ci
                
                # note down the room for the lecture
                courses[ci]['lecSections']['LEC1']['room'] = courses[ci]['lecSections']['LEC1']['room'] + dayi+"("+r+")"
                roomAssigned = True
                
            if roomAssigned:
                break
        if  not roomAssigned:
            print(ci,dayi, dayiSlots,'rooms not found')
            courses[ci]['lecSections']['LEC1']['room'] = 'TBA'
            
    if 'LEC2' in courses[ci]['lecSections']:
        lectureSlots = courses[ci]['lecSections']['LEC2']['timings']
        courses[ci]['lecSections']['LEC2']['room'] = ''
        
        for dayi in lectureSlots:
            dayiSlots = lectureSlots[dayi]
            roomAssigned = False
            for r in rooms:
                # skip is room is not big enough
                if rooms[r]['capacity'] < courses[ci]['lecCapacity']:
                    continue
                isRoomAvailable = True
                for s in dayiSlots:
                    if (rooms[r]['slots'][dayi][s] != 'available'):
                        isRoomAvailable = False
                if isRoomAvailable:
                    # make the room unavailalbe
                    for s in dayiSlots:
                        rooms[r]['slots'][dayi][s] = ci
                    # note down the room for the lecture
                    courses[ci]['lecSections']['LEC2']['room'] = courses[ci]['lecSections']['LEC2']['room'] + dayi+"("+r+")"
                    roomAssigned = True
                if roomAssigned:
                    break
            if  not roomAssigned:
                print(ci,dayi, dayiSlots,'rooms not found')
                courses[ci]['lecSections']['LEC2']['room'] = 'TBA'
    
    

##---------------------


##---------------------

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
workbook = xlsxwriter.Workbook('new-timeTable-SNU-Fall2019.xlsx') 
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
        

courses['ECO101']['CourseCapacity'] = '150,L1(90),L2(60)'
    
for ci in courses:
    c = courses[ci]
    if 'lecSections' in c:
        for li in c['lecSections']:
            if 'timings' in c['lecSections'][li]:
                time = sortedDays(c['lecSections'][li]['timings'],ci)
                
                room = ''
                if 'room' in c['lecSections'][li]:
                    room = c['lecSections'][li]['room']
                else:
                    room = 'TBA'
                
                instructor = ''
                for i in c['lecSections'][li]['instructors']:
                    instructor = instructor+cleanInstructor(i)+','
                instructor = instructor[0:-1]
                
                studentSet = ''
                for s in sorted(c['lecSections'][li]['students']):
                    studentSet = studentSet+s+','
                    
                studentSet = studentSet[0:-1]
                
                cCapacity = c['CourseCapacity']
                
                if 'CSD320' in ci:
                    worksheet.write(row, codeCol, ci+'(new code CSD316)')
                else:
                    worksheet.write(row, codeCol, ci)
                    
                    
                worksheet.write(row, meetingType, li)
                worksheet.write(row, timeCol, time)
                worksheet.write(row, instructorCol, instructor)
                worksheet.write(row, studentCol, studentSet)
                worksheet.write(row, roomCol, room)
                worksheet.write(row, capacityCol, cCapacity)
                worksheet.write(row,uweCol,coursesBackUp[ci]['openAsUWE'])
                
                row = row+1
                
    if 'tutSections' in c:
        for li in c['tutSections']:
            if 'timings' in c['tutSections'][li]:
                time = sortedDays(c['tutSections'][li]['timings'],ci)
                
                room = c['tutSections'][li]['room']
                instructor = ''
                for i in c['tutSections'][li]['instructors']:
                    instructor = instructor+cleanInstructor(i)+','
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
                time = sortedDays(c['labSections'][li]['timings'],ci)
                
                room = c['labSections'][li]['room']
                instructor = ''
                for i in c['labSections'][li]['instructors']:
                    instructor = instructor+cleanInstructor(i)+','
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
                    
# lets measure how many courses are available for each student group
studetGroups = dict()
cLs = set()
for c in courses:
    if c[0:3] == 'CCC':
        continue
    
    if 'lecSections' in courses[c]:
        for seci in courses[c]['lecSections']:
            cTag = c
            cTag = cTag+seci
            cLs.add(cTag)
    else:
        cTag = c
        cTag = cTag + 'xxxx'
        cLs.add(cTag)
    
cLT = set()
for ci in cLs:
    c = ci[0:6]
    if 'tutSections' in courses[c]:
        for seci in courses[c]['tutSections']:
            cLTtag = ci
            if len(seci) == 4:
                cLTtag = cLTtag+seci+'x'
            else:
                cLTtag = cLTtag+seci
            cLT.add(cLTtag)
    else:
        cLTtag = ci
        cLTtag = cLTtag + 'xxxxx'
        cLT.add(cLTtag)

cLTP = set()
for ci in cLT:
    c = ci[0:6]
    if 'labSections' in courses[c]:
        for seci in courses[c]['labSections']:
            cLTPtag = ci
            cLTPtag = cLTPtag+seci
            cLTP.add(cLTPtag)
    else:
        cLTPtag = ci
        cLTPtag = cLTPtag + 'xxxxx'
        cLTP.add(cLTPtag)

cLTP = sorted(cLTP)
##------------------------------------------------

def timeDictToTimeSet(lT):
    tSet = set()
    for d in lT:
        for t in lT[d]:
            tSet.add((d,t))
    return(tSet)

def getTimingsSet(cLTPtag):
    cCode = cLTPtag[0:6]
    lSec = cLTPtag[6:10]
    tSec = cLTPtag[10:15]
    if tSec[-1] == 'x':
        tSec = tSec[0:-1]
    pSec = cLTPtag[15:]
    tSet = set()
    if 'LEC' in lSec:
        lT = courses[cCode]['lecSections'][lSec]['timings']
        tSet = tSet.union(timeDictToTimeSet(lT))
    if 'TUT' in tSec:
        lT = courses[cCode]['tutSections'][tSec]['timings']
        tSet = tSet.union(timeDictToTimeSet(lT))
    if 'PRAC' in pSec:
        lT = courses[cCode]['labSections'][pSec]['timings']
        tSet = tSet.union(timeDictToTimeSet(lT))
    return(tSet)
    
#----------------------------------------------------------
studentsTimeSet = dict()
for c in courses:
    if 'CCC' in c:
        continue
    
    if 'lecSections' in courses[c]:
        for seci in courses[c]['lecSections']:
            tSet = courses[c]['lecSections'][seci]['timings']
            tSet = timeDictToTimeSet(tSet)
            if courses[c]['lecSections'][seci]['students'] == {''}:
                continue

            for s in  courses[c]['lecSections'][seci]['students']:
                if s not in studentsTimeSet:
                    studentsTimeSet[s] = dict()
                    studentsTimeSet[s]['busyTimes'] = set()
                studentsTimeSet[s]['busyTimes'] = studentsTimeSet[s]['busyTimes'].union(tSet)
                
    if 'tutSections' in courses[c]:
        for seci in courses[c]['tutSections']:
            tSet = courses[c]['tutSections'][seci]['timings']
            tSet = timeDictToTimeSet(tSet)
            #skip if no students
            if courses[c]['tutSections'][seci]['students'] == {''}:
                continue
            for s in  courses[c]['tutSections'][seci]['students']:
                if s not in studentsTimeSet:
                    studentsTimeSet[s] = dict()
                    studentsTimeSet[s]['busyTimes'] = set()
                studentsTimeSet[s]['busyTimes'] = studentsTimeSet[s]['busyTimes'].union(tSet)
                
    if 'labSections' in courses[c]:
        for seci in courses[c]['labSections']:
            tSet = courses[c]['labSections'][seci]['timings']
            tSet = timeDictToTimeSet(tSet)
            #skip if no students
            if courses[c]['labSections'][seci]['students'] == {''}:
                continue
            for s in  courses[c]['labSections'][seci]['students']:
                if s not in studentsTimeSet:
                    studentsTimeSet[s] = dict()
                    studentsTimeSet[s]['busyTimes'] = set()
                studentsTimeSet[s]['busyTimes'] = studentsTimeSet[s]['busyTimes'].union(tSet)
                    

# find conflic free coures
def major(stGroup):
    if stGroup not in {'CSE','EEE','ECE'}:
        return stGroup
    if stGroup == 'EEE':
        return 'EED'
    if stGroup == 'ECE':
        return 'EED'
    if stGroup == 'CSE':
        return 'CSD'

                
for s in sorted(studentsTimeSet):
    studentsTimeSet[s]['conflictFreeCourses'] = set()
    studentsTimeSet[s]['conflictFreeUWECourses'] = set()
    sTime = studentsTimeSet[s]['busyTimes']
    for c in cLTP:
        if not sTime.intersection(getTimingsSet(c)):
            cCode = c[0:6]
            studentsTimeSet[s]['conflictFreeCourses'].add(cCode)
            if 'Yes' in courseList[cCode]['openAsUWE']:
                if cCode[0:3] != major(s[0:3]):
                    studentsTimeSet[s]['conflictFreeUWECourses'].add(cCode)
                
            


coursesPickle = open('courses.pickle','rb')
courseList = pickle.load(coursesPickle) 
# write in excel



workbook = xlsxwriter.Workbook('stillAvailableCourses.xlsx') 
worksheet = workbook.add_worksheet()

row = 0

# header row
worksheet.write(row, 0, 'student group')
worksheet.write(row, 1, 'num of non conflicting couress')
worksheet.write(row, 2, 'non conflicting coures')
worksheet.write(row, 3, 'num non conflicting UWE')
worksheet.write(row, 4, 'courses')




for s in sorted(studentsTimeSet):
    row  = row +1
    worksheet.write(row,0,s)
    worksheet.write(row,1,len(studentsTimeSet[s]['conflictFreeCourses']))
    cString = ''
    for c in sorted(studentsTimeSet[s]['conflictFreeCourses']):
        cString = cString + c+','
    cString = cString[:-1]
    worksheet.write(row,2,cString)
    worksheet.write(row,3,len(studentsTimeSet[s]['conflictFreeUWECourses']))
    cString = ''
    for c in sorted(studentsTimeSet[s]['conflictFreeUWECourses']):
        cString = cString + c+','
    cString = cString[:-1]
    worksheet.write(row,4,cString)
    
    
workbook.close()
    
    
    
         
#save the instructor set for creating their non available slots
with open('roomsAvailability.pickle', 'wb') as f:
    pickle.dump(rooms, f)

        
    
