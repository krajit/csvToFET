#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:44:46 2019

@author: ajit
"""

import re, csv


# laod a starting template for .fet file readable by FET.
templatePath = 'basicTemplate.fet'
basicTemplate = open(templatePath,"r").read()



# one by one load data in the basicTemplate, and will write that in a new file 
formattedData = basicTemplate 

# add instute name
formattedData = re.sub(
        r"<Institution_Name>.*</Institution_Name>",
        '<Institution_Name>Shiv Nadar University</Institution_Name>',
        formattedData)


#days
timeTableDays = ['MWF','TTh']

# hours, written vertically aligned to easily comment out few slots
slots = [
         '08:00', 
         '08:30',
         '09:00',
         '09:30',
         '10:00',
         '10:30',
         '11:00',
         '11:30',
         '12:00',
         '12:30',
         '13:00',
         '13:30',
         '14:00',
         '14:30',
         '15:00',
         '15:30',
         '16:00',
         '16:30',
         '17:00',
         '17:30',
         '18:00',
         '18:30',
          '19:00',
          '19:30'
         ]

TThStartTimimgs = ['09:00','10:30', '14:00', '15:30', '17:00', '18:30']



# replace default days 
daysTag = "<Days_List>\n"
daysTag = daysTag + "<Number_of_Days>"+str(len(timeTableDays))+"</Number_of_Days>\n"

for day in timeTableDays:
    daysTag = daysTag + "<Day><Name>"+ day + "</Name></Day>\n" 

daysTag = daysTag + "</Days_List>\n"

formattedData = re.sub(
        r"<Days_List>(.*?)</Days_List>", daysTag,
        formattedData,flags=re.DOTALL)

# replace default hours
hoursTag = "<Hours_List>\n"
hoursTag = hoursTag + "<Number_of_Hours>"+str(len(slots))+"</Number_of_Hours>\n"

for h in slots:
    hoursTag = hoursTag + "<Hour><Name>"+ h + "</Name></Hour>\n" 

hoursTag = hoursTag + "</Hours_List>\n"

formattedData = re.sub(
        r"<Hours_List>(.*?)</Hours_List>", hoursTag,
        formattedData,flags=re.DOTALL)

# read subjectlist from a csv file and load
#tag = "<Subjects_List>\n"
#subjectList = [];
#with open('testData/subjects.csv', 'r') as ff:
#  reader = csv.reader(ff)
#  subjectList = list(reader)

#for s in subjectList[1:]:
#    tag = tag + "<Subject>\n\t <Name>"+s[0]+"</Name>\n\t<Comments></Comments>\n</Subject>\n"
#
#tag = tag + "</Subjects_List>\n"
#formattedData = re.sub(
#        r"<Subjects_List>(.*?)</Subjects_List>", tag,
#        formattedData,flags=re.DOTALL)


# read activity tags list from a csv file and load
#tag = "<Activity_Tags_List>\n"
#Activity_Tags_List = [];
#with open('testData/activity_tags.csv', 'r') as ff:
#  reader = csv.reader(ff)
#  Activity_Tags_List = list(reader)
#
#for s in Activity_Tags_List[1:]:
#    tag = tag + "<Activity_Tag>\n\t<Name>"+s[0]+\
#    "</Name>\n\t<Printable>true</Printable>\n\t	<Comments></Comments>\n</Activity_Tag>\n"
#
#tag = tag + "</Activity_Tags_List>\n"
#formattedData = re.sub(
#        r"<Activity_Tags_List>(.*?)</Activity_Tags_List>", tag,
#        formattedData,flags=re.DOTALL)
#

# add student groups

totalNumberOfStudents = 0
with open('testData/students.csv', 'r') as ff:
  reader = csv.reader(ff)
  studentGroupList = list(reader)

# remove header read from the file
studentGroupList = studentGroupList[1:]

for grItem in studentGroupList:
    totalNumberOfStudents = totalNumberOfStudents + int(grItem[1])

tag = '\
<Students_List> \n\
<Year> \n\
    <Name>SNU</Name> \n\
    <Number_of_Students>'+str(totalNumberOfStudents) +'</Number_of_Students>\n\
    <Comments></Comments> \n'
       
for grItem in studentGroupList:
    tag = tag +  '<Group> \n <Name>'+ grItem[0] + '</Name>\n \
    <Number_of_Students>'+grItem[1]+'</Number_of_Students>\n \
	<Comments></Comments>\n \
</Group> \n'
                   
       
tag = tag+'</Year>\n</Students_List>'

#update file
formattedData = re.sub(
        r"<Students_List>(.*?)</Students_List>", tag,
        formattedData,flags=re.DOTALL)      

#read roomsAndBuildingFile
with open('testData/rooms_and_buildings.csv', 'r') as ff:
  reader = csv.reader(ff)
  roomsAndBuilding = list(reader)

buildingSet = set('');
AroomSet = set('');
BroomSet = set('');
CDroomSet = set('');

labRoomCons = ''

tag = '<Rooms_List>\n'
for room in roomsAndBuilding[1:]:   # [1:] is for ignoring the first row
    
    buildingSet.add(room[2])
    if (room[2] == 'Lab'):
        labRoomCons = labRoomCons + '<ConstraintActivityTagPreferredRoom>\n \
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Activity_Tag>'+room[0]+'</Activity_Tag> \n \
	<Room>'+room[0]+'</Room> \n \
	<Active>true</Active> \n \
	<Comments></Comments> \n \
</ConstraintActivityTagPreferredRoom>\n'
    
    
    if (room[0][0] == 'A'):
        AroomSet.add(room[0])
    elif(room[0][0] == 'B'):
        BroomSet.add(room[0])
    else:
        CDroomSet.add(room[0])
                
    tag = tag + '<Room> \n\
	<Name>'+room[0]+'</Name>\n \
	<Building>'+room[2]+'</Building>\n \
	<Capacity>'+room[1]+'</Capacity>\n \
	<Comments></Comments>\n </Room>\n '
tag = tag+ '</Rooms_List>\n'
#update file
formattedData = re.sub(
        r"<Rooms_List>(.*?)</Rooms_List>", tag,
        formattedData,flags=re.DOTALL)      

allRoomSet = AroomSet.union(BroomSet).union(CDroomSet)


# add building list
tag = '<Buildings_List>\n'
for building in buildingSet:   # [1:] is for ignoring the first row
    tag = tag + '<Building>\n \
	<Name>'+building+'</Name> \n \
	<Comments></Comments> \n \
</Building>\n'
    
tag = tag+ '</Buildings_List>\n'
#update file
formattedData = re.sub(
        r"<Buildings_List>(.*?)</Buildings_List>", tag,
        formattedData,flags=re.DOTALL)      

# the activities.csv needs to loaded at the FET interface




#### time constraints ##############################################333

# basic compulsory time constraint
tag = '<Time_Constraints_List>\n\
<ConstraintBasicCompulsoryTime>\n\
	<Weight_Percentage>100</Weight_Percentage>\n\
	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintBasicCompulsoryTime>\n'

## create MFW and TTh constraints
#days = timeTableDays;
#for day in days:
#    
#    tag = tag+ '<ConstraintActivitiesPreferredTimeSlots> \n\
#    	<Weight_Percentage>100</Weight_Percentage> \n\
#    	<Teacher_Name></Teacher_Name> \n\
#    	<Students_Name></Students_Name> \n\
#    	<Subject_Name></Subject_Name> \n\
#    	<Activity_Tag_Name>'+day+'</Activity_Tag_Name> \n\
#    	<Duration></Duration> \n\
#    	<Number_of_Preferred_Time_Slots>'+str(len(slots))+'</Number_of_Preferred_Time_Slots>\n'
#        
#    for periods in slots:
#        tag = tag + '	<Preferred_Time_Slot> \n \
#		<Preferred_Day>'+day+'</Preferred_Day> \n \
#		<Preferred_Hour>'+periods+'</Preferred_Hour> \n \
#	</Preferred_Time_Slot>\n'
#    tag = tag + '	<Active>true</Active> \n \
#	<Comments></Comments> \n \
#</ConstraintActivitiesPreferredTimeSlots>\n'

# add TTh 12-2 break time
tag = tag + '<ConstraintBreakTimes> \n\
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Number_of_Break_Times>4</Number_of_Break_Times> \n \
	<Break_Time> \n \
		<Day>TTh</Day> \n \
		<Hour>12:00</Hour> \n \
	</Break_Time> \n \
	<Break_Time> \n \
		<Day>TTh</Day> \n \
		<Hour>12:30</Hour> \n \
	</Break_Time> \n \
	<Break_Time> \n \
		<Day>TTh</Day> \n \
		<Hour>13:00</Hour> \n \
	</Break_Time> \n \
	<Break_Time> \n \
		<Day>TTh</Day> \n \
		<Hour>13:30</Hour> \n \
	</Break_Time> \n \
	<Active>true</Active> \n \
	<Comments></Comments> \n \
</ConstraintBreakTimes>\n'

lunchConsTag = '<ConstraintActivitiesPreferredStartingTimes> \n \
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Teacher_Name></Teacher_Name> \n \
	<Students_Name></Students_Name> \n \
	<Subject_Name>Lunch</Subject_Name> \n \
	<Activity_Tag_Name></Activity_Tag_Name> \n \
	<Duration></Duration> \n \
	<Number_of_Preferred_Starting_Times>2</Number_of_Preferred_Starting_Times> \n \
	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>MWF</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>MWF</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>14:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
	<Comments></Comments> \n \
</ConstraintActivitiesPreferredStartingTimes>\n'

tag = tag + lunchConsTag

MWFlecStTimeCons = '<ConstraintActivitiesPreferredStartingTimes> \n \
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Teacher_Name></Teacher_Name> \n \
	<Students_Name></Students_Name> \n \
	<Subject_Name></Subject_Name>\n \
	<Activity_Tag_Name>MWF</Activity_Tag_Name> \n \
	<Duration></Duration> \n \
	<Number_of_Preferred_Starting_Times>'+str(int(len(slots)/2))+'</Number_of_Preferred_Starting_Times>\n'
    
for s in slots[::2]:
    MWFlecStTimeCons = MWFlecStTimeCons + '	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>MWF</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>'+s+'</Preferred_Starting_Hour>\n\
	</Preferred_Starting_Time>'

MWFlecStTimeCons = MWFlecStTimeCons + '	<Active>true</Active> \n \
	<Comments></Comments> \n \
</ConstraintActivitiesPreferredStartingTimes>\n'

tag = tag + MWFlecStTimeCons


TThlecStTimeCons = '<ConstraintActivitiesPreferredStartingTimes> \n \
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Teacher_Name></Teacher_Name> \n \
	<Students_Name></Students_Name> \n \
	<Subject_Name></Subject_Name>\n \
	<Activity_Tag_Name>TTh</Activity_Tag_Name> \n \
	<Duration></Duration> \n \
	<Number_of_Preferred_Starting_Times>'+str(len(TThStartTimimgs))+'</Number_of_Preferred_Starting_Times>\n'
    
for s in TThStartTimimgs:
    TThlecStTimeCons = TThlecStTimeCons + '	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>TTh</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>'+s+'</Preferred_Starting_Hour>\n\
	</Preferred_Starting_Time>'

TThlecStTimeCons = TThlecStTimeCons + '	<Active>true</Active> \n \
	<Comments></Comments> \n \
</ConstraintActivitiesPreferredStartingTimes>\n'

tag = tag + TThlecStTimeCons

# minimal gap time constraint
tag = tag + '<ConstraintStudentsMaxGapsPerWeek> \n \
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Max_Gaps>0</Max_Gaps> \n \
	<Active>true</Active> \n \
	<Comments></Comments>\n\
</ConstraintStudentsMaxGapsPerWeek>\n\
<ConstraintTeachersMaxGapsPerWeek>\n\
	<Weight_Percentage>100</Weight_Percentage>\n\
	<Max_Gaps>0</Max_Gaps>\n\
	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintTeachersMaxGapsPerWeek>\n'

tag = tag + '</Time_Constraints_List>\n'

##  end time constraints

# write your content in n new file
formattedData = re.sub(
        r"<Time_Constraints_List>(.*?)</Time_Constraints_List>",tag ,
        formattedData,flags=re.DOTALL)      
###############################################33333


## space constaints

# basic compulsory constraint
spaceCons = '<Space_Constraints_List> \n \
<ConstraintBasicCompulsorySpace> \n \
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Active>true</Active> \n \
	<Comments></Comments> \n \
</ConstraintBasicCompulsorySpace>\n'

# all room - tag roomAny
spaceCons = spaceCons + '<ConstraintActivityTagPreferredRooms> \n \
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Activity_Tag>roomAny</Activity_Tag> \n \
	<Number_of_Preferred_Rooms>'+str(len(allRoomSet))+'</Number_of_Preferred_Rooms> \n'

for room in allRoomSet:
    spaceCons = spaceCons + '<Preferred_Room>'+room+'</Preferred_Room>\n'
    
spaceCons = spaceCons + '<Active>true</Active> \n \
	<Comments></Comments> \n \
</ConstraintActivityTagPreferredRooms>\n'


# add lab room constraints
spaceCons = spaceCons + labRoomCons

spaceCons = spaceCons + '</Space_Constraints_List>\n'
    
#update file
formattedData = re.sub(
        r"<Space_Constraints_List>(.*?)</Space_Constraints_List>", spaceCons,
        formattedData,flags=re.DOTALL)      
    




## write file

dataFile = 'loadedData.fet'
f = open(dataFile,'w+')
f.write(formattedData)
f.close





dayFile = 'trash.xml'
g = open(dayFile,'w')
g.write("trash")
g.close
