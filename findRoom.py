#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 02:24:33 2019

@author: ajit
"""


slots = [
        '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00',
         '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
         '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', 
         '18:00', '18:30', '19:00', '19:30','20:00'
         ]


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
    days = ['M', 'T', 'W', 'Th', 'F','S','Sun']
    for d in days:
        rooms[r]['slots'][d] = dict()
        for s in slots:
            rooms[r]['slots'][d][s] = 'available'


# read BMS course sheet
courses = dict()
roomFile = "SNU - Monsoon 2019.xlsx"
wb = xlrd.open_workbook(roomFile) 
sheet = wb.sheet_by_index(0) # get first sheet

## fill in the rooms booking
#for i in range(1,sheet.nrows):
#    cCode = sheet.cell_value(i,0)
#    ltp = sheet.cell_value(i,1)
#    currentRoom = sheet.cell_value(i,5)
#    cCapacity = sheet.cell_value(i,6)
#    
#    if 'PRAC' in ltp:
#        continue
#    timings =sheet.cell_value(i,2) 
#    if (',' in timings):
#        offPatternTimings.append()
#        
#        
#    timings = timingsToSlots(timings)
#    
    

import re

def timingsToSlots(timings):
    days = re.findall('[A-Z][a-z]*',timings.split(' ')[0])
    times = timings.split(' ')[1]
    tBegin = times.split('-')[0]
    tEnd = times.split('-')[-1]
    
    tBeginIndex = slots.index(tBegin)
    tEndIndex = slots.index(tEnd)
    cSlots = slots[tBeginIndex:tEndIndex]
    timeDict = dict()
    for d in days:
        timeDict[d] = cSlots
    return(timeDict)


def markRooms(dt,cCode,ltp,cRoom):
    if cRoom not in rooms:
        print(cCode,cRoom, 'not a regular classroom')
        return

    for d in dt:
        for t in dt[d]:
            availability =  rooms[cRoom]['slots'][d][t]
            if 'available' in availability:
                rooms[cRoom]['slots'][d][t] = set()
                rooms[cRoom]['slots'][d][t].add(cCode+ltp)
            else:
                print(cCode,cRoom, 'Double booked',d,t,availability)
                rooms[cRoom]['slots'][d][t].add(cCode+ltp)
                

departments = {'ADP','BDA','BIO','CHY','MAT','PHY','ART','CCC','CED','CHD',
               'CSD','DES','DOM','ECO','EED','ENG','FAC','HIS','INT','ISM',
               'MEC','MED','MGT','MKT','OHM','SOC','STM'}    
        
bBlockPrefs = {'ADP','BDA','BIO','CHY','MAT','PHY'}
dBlockPrefs = departments.difference(bBlockPrefs)    


def findRoom(tSet,cCode,capacity, biometric = False):
    availableRoomSet = set()
    for r in rooms:
        if rooms[r]['capacity'] < capacity:
            continue
        if (biometric == True) and (rooms[r]['isBiometric'] == False):
            continue
        roomAvailable = True
        for ds in tSet:
            d,s = ds
            if 'available' not in rooms[r]['slots'][d][s]:
                roomAvailable = False
                continue    
        if roomAvailable:
            availableRoomSet.add((r,rooms[r]['capacity']))
    
    if len(availableRoomSet) == 0:
        print(cCode, capacity, 'no room found')
        return 'TBA'

    # sort room 
    # increasing room capacity
    # and room preference
    if cCode[0:3] in bBlockPrefs:                    
        # sort room B block first
        availableRoomSet = sorted(sorted(availableRoomSet, key = lambda x : x[0], reverse = False), key = lambda x : x[1]) 
    else:
        # sort room D Block first
        availableRoomSet = sorted(sorted(availableRoomSet, key = lambda x : x[0], reverse = True), key = lambda x : x[1]) 
        
    print(availableRoomSet)
        
    return (availableRoomSet[0][0])   


# fill in the rooms booking
for i in range(1,sheet.nrows):
    cCode = sheet.cell_value(i,0)
    ltp = sheet.cell_value(i,1)
    currentRoom = sheet.cell_value(i,5)
    if 'PRAC' in ltp:
        continue
    timings =sheet.cell_value(i,2).split(', ') 
    cTimings = dict()
    for t in timings:
        dt = timingsToSlots(t)
        markRooms(dt,cCode,ltp,currentRoom)
        

def timeTotSet(timeString):
    tSet = set()
    timings =timeString.split(', ')  
    for t in timings:
        for d in timingsToSlots(t):
            for s in timingsToSlots(t)[d]:
                tSet.add((d,s))
    return(tSet)
    
        
        

# room availability function
def isRoomAvailable(room,timings):
    availability = True
    dt = timingsToSlots(timings)
    for d in dt:
        for t in dt[d]:
            if 'available' not in rooms[room]['slots'][d][t]:
                availability = False
                return(availability)
    return(availability)
    



#    
##sort rooms from small to big    
#roomsList = sorted(rooms.items(), key = lambda x: x[1]['capacity'], reverse=False)
## make it into dictionry again
#rooms = dict()
#for r in roomsList:
#    rooms[r[0]] = r[1]
#    
#def findRoom(capacity,timings):
#    for r in rooms:
#        if rooms[r]['capacity'] < capacity:
#            continue
#        if isRoomAvailable(r,timings):
#            return(r)
#    # no room found
#    print('no room available')
#    return ''
#    
    
    
##courses with consective lectures and tutorials    
    







