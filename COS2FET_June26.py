#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 17:00:47 2019

@author: ajit
"""

import re, csv
import random, xlrd

# some preparotory instructions
print('\nWarning: File downloaded from COS contains Ziaur Rehman. It is a dummy instructor name. Make sure to replace it with unique name for each activity.\n')
print('\nWarning: Large courses with multiple tutorials generally have instructor names in the tutorials section. Make sure to replace that with course code + TAi to get accurate time table.\n')


#--------------------------------------------------------
# laod a starting template for .fet file readable by FET.
templatePath = 'basicTemplate.fet'
basicTemplate = open(templatePath,"r").read()
formattedData = basicTemplate 
fetFileName = 'snu-timetable.fet'

# hours, written vertically aligned to easily comment out few slots
slots = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00',
         '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
         '15:00', '15:30', 
         '16:00', 
         '16:30', 
         '17:00', 
         '17:30', 
#         '18:00',
#         '18:30', 
#         '19:00', 
#         '19:30',
         ]


# prepare student groups
studentGroups = {
        'year1': {'BIO1', 'BMS1', 'CED1', 'CHD1', 'CHY1', 'CSE1', 'ECE1', 'ECO1', 
                  'EEE1', 'ENG1', 'HIS1', 'INT1', 'MAT1', 'MED1', 'PHY1', 'SOC1'},
        'year2': {'BIO2', 'BMS2', 'CED2', 'CHD2', 'CHY2', 'CSE2', 'ECE2', 'ECO2', 
                  'EEE2', 'ENG2', 'HIS2', 'INT2', 'MAT2', 'MED2', 'PHY2', 'SOC2'},
        'year3': {'BIO3', 'BMS3', 'CED3', 'CHD3', 'CHY3', 'CSE3', 'ECE3', 'ECO3', 
                  'EEE3', 'ENG3', 'HIS3', 'INT3', 'MAT3', 'MED3', 'PHY3', 'SOC3'},
        'year4': {'BIO4', 'BMS4', 'CED4', 'CHD4', 'CHY4', 'CSE4', 'ECE4', 'ECO4', 
                  'EEE4', 'ENG4', 'HIS4', 'INT4', 'MAT4', 'MED4', 'PHY4', 'SOC4'}}

studentsListXML = '<Students_List>\n'
for si in studentGroups:
    studentsListXML = studentsListXML + '<Year>\n' 
    studentsListXML = studentsListXML + '\t<Name>'+si+'</Name>\n'
    studentsListXML = studentsListXML + '\t<Number_of_Students>'+str(len(studentGroups[si]))+'</Number_of_Students>\n'
    studentsListXML = studentsListXML + '\t<Comments></Comments>\n' 
    
    for gr in studentGroups[si]:
        studentsListXML = studentsListXML + '\t<Group>\n'
        studentsListXML = studentsListXML + '\t\t<Name>'+gr+'</Name>\n'
        studentsListXML = studentsListXML + '\t\t<Number_of_Students>1</Number_of_Students>\n'
        studentsListXML = studentsListXML + '\t\t<Comments></Comments>\n'
        studentsListXML = studentsListXML + '\t</Group>\n'
    studentsListXML = studentsListXML + '</Year>\n'
studentsListXML = studentsListXML + '</Students_List>\n'

# read course offering data
import readCOSdata as COS
courseList = COS.courseList # a dictionary containing details of each course read from COS excel file
CCCcourses = COS.CCCcourses

# minorElectives = COS.minorElectives
# UWEnotInMinors = COS.UWEnotInMinors

maxMajorElectives = 3
numMajorElectives = dict()
for y in studentGroups:
    for s in studentGroups[y]:
        numMajorElectives[s] = maxMajorElectives



# add students to complusory courses
# loop over courses and add the set of major studetns to it
print('Adding major students in their compulsory courses ......')
for ci in courseList:
    c = courseList[ci]
    c['studentsSet'] = set()
    
    if (c['CourseType'] == 'Major') :
        for m in c['programs']:
            c['studentsSet'].add(m)
            
            
    if (c['CourseType'] == 'Major Elective') :
        for m in c['programs']:
            if numMajorElectives[m] > 0:
                c['studentsSet'].add(m)
                numMajorElectives[m] = numMajorElectives[m] -1 
            else:
                print('Student group', m, 'not added in ', ci, 'because too many major electives')
            
            
#add UWE students preferences given by instructors
import readUWEInstructorsPreference as up
UWEcourses = up.UWEcourses
for c in UWEcourses:
    if 'pref1' in UWEcourses[c]:
        courseList[c]['studentsSet'].add(UWEcourses[c]['pref1'])
       

## add year1, year2, year3 in on one randomly selected CCC
# Then manually make sure all CCC overlaps
courseList['CCC510']['studentsSet'].add('year1')

courseList['CCC515']['studentsSet'].add('year1')
courseList['CCC515']['studentsSet'].add('year2')
courseList['CCC515']['studentsSet'].add('year3')

            
# replace 'programs' dictionary with 'studentsSet' dictionary in each course
# because the pragram is designed to distribute 'programs' dictionary among sections
for ci in courseList:
    c = courseList[ci]
    c['programs'] = c['studentsSet']
   
            
            
# filling lecture sections, tutorial sections, lab sections with students subgroups               
for cIndex, c in courseList.items():    
    
    # fill lecture dictionary with students
    if 'lecSections' in c:
        numSections = len(c['lecSections'])
        # start picking programs and putting them in lecSEcSTudents
        j = 0 # section index
        for s in c['programs']:
            courseList[cIndex]['lecSections']['LEC'+str(j+1)]['students'].add(s)
            j = (j +1) % numSections              # cycle over sections 
            
    # fill tutorials with students
    if 'tutSections' in c:
        numSections = len(c['tutSections'])
        # start picking programs and putting them in tut
        j = 0 # section index
        for s in c['programs']:
            courseList[cIndex]['tutSections']['TUT'+str(j+1)]['students'].add(s)
            j = (j +1) % numSections              # cycle over sections 
            
                        
    # fill practicals sections with students
    if 'labSections' in c:
        numSections = len(c['labSections'])
        # start picking programs and putting them in tut
        j = 0 # section index
        for s in c['programs']:
            courseList[cIndex]['labSections']['PRAC'+str(j+1)]['students'].add(s)
            j = (j +1) % numSections              # cycle over sections 
               
               
## map courses to activities
tutDurationSet = set()
activityTagSet= set()
activityString = "Students Sets,Subject,Teachers,Activity Tags,Total Duration,Split Duration,Min Days,Weight,Consecutive\n"

def splitLec(totalDuration, lecDuration = '2'):
    if (totalDuration == '2'):
        return '2'
    elif (totalDuration == '3'):
        return '3'
    elif (totalDuration == '4'):
        return '2+2'
    elif (totalDuration == '6'):
        if (lecDuration == '3'):
            return '3+3'
        else:
            return '2+2+2'
    elif (totalDuration == '8'):
        return '4+4'
    elif (totalDuration == '10'):
        return '5+5'
    else:
        return ''
      
        
activityListXML = '<Activities_List>\n'
activityId = 0
activityGroupId = 0
for cIndex, c in courseList.items():
    if 'lecSections' in c:
        for lIndex, l in c['lecSections'].items():
            activityXML = '<Activity>\n'
            activityXML = activityXML + '\t<Subject>'+cIndex+'</Subject>\n'
            for s in l['students']:
                activityXML = activityXML + '\t<Students>'+s+'</Students>\n'
            teachers = ''
            for i in l['instructors']:
                activityXML = activityXML + '\t<Teacher>'+i+'</Teacher>\n'
            activityTag = lIndex #'LEC+AnyRoom+'+lIndex
            activityTagSet.add(activityTag)
            activityXML = activityXML + '\t<Activity_Tag>'+activityTag+'</Activity_Tag>\n'
            
            if (cIndex[0:3] == 'CCC'):
                activityTag = 'CCC'
                activityTagSet.add(activityTag)
                activityXML = activityXML + '\t<Activity_Tag>'+activityTag+'</Activity_Tag>\n'

            totalDuration = str(c['LectureHoursPerWeek'])
            if (int(totalDuration) >= 12):
                print(cIndex + " abnormally high lecture hours. Skipping")
                continue
            lecDuration = str(c['LectureDuration'])
            if (cIndex[0:3] == 'CCC'):
                lecDuration = '3'            
            
            splitDuration = splitLec(totalDuration,lecDuration)
            activityXML = activityXML + '\t<Duration>'+splitDuration[0]+'</Duration>\n'
            activityXML = activityXML + '\t<Total_Duration>'+totalDuration+'</Total_Duration>\n'
                
            # add an acitivtyID for each contact session
            # needed for forcing lectures on diff days to to on same time 
            activityIdSet = set()
            for i in range(0,len(splitDuration),2):
                activityId = activityId + 1
                activityIdSet.add(activityId)
                # get first lecture id in week
                if (i == 0):
                    activityGroupId = activityId
                activityXMLi = activityXML
                activityXMLi = activityXMLi + '\t<Id>'+str(activityId)+'</Id>\n'
                activityXMLi = activityXMLi + '\t<Activity_Group_Id>'+str(activityGroupId)+'</Activity_Group_Id>\n'
                activityXMLi = activityXMLi + '\t<Active>true</Active>\n'
                activityXMLi = activityXMLi + '\t<Comments></Comments>\n'
                activityXMLi = activityXMLi + '</Activity>\n'
                activityListXML = activityListXML + activityXMLi
            courseList[cIndex]['lecSections'][lIndex]['ids']=activityIdSet

    if 'tutSections' in c:
        for lIndex, l in c['tutSections'].items():
            activityXML = '<Activity>\n'
            activityXML = activityXML + '\t<Subject>'+cIndex+'</Subject>\n'
            for s in l['students']:
                activityXML = activityXML + '\t<Students>'+s+'</Students>\n'
            for i in l['instructors']:
                activityXML = activityXML + '\t<Teacher>'+i+'</Teacher>\n'
            activityTag = lIndex #'TUT+AnyRoom+'+lIndex
            activityTagSet.add(activityTag)
            activityXML = activityXML + '\t<Activity_Tag>'+activityTag+'</Activity_Tag>\n'

            if (cIndex[0:3] == 'CCC'):
                activityTag = 'CCC'
                activityTagSet.add(activityTag)
                activityXML = activityXML + '\t<Activity_Tag>'+activityTag+'</Activity_Tag>\n'
            
            totalDuration = str(c['TutorialHoursPerWeek'])
            if (int(totalDuration) >= 12):
                print(cIndex + " abnormally high tutorials hours. Skipping")
                continue
            splitDuration = splitLec(totalDuration,'3')
            activityXML = activityXML + '\t<Duration>'+splitDuration[0]+'</Duration>\n'
            activityXML = activityXML + '\t<Total_Duration>'+totalDuration+'</Total_Duration>\n'

            # add an acitivtyID for each contact session
            # needed for forcing lectures on diff days to to on same time 
            activityIdSet = set()
            for i in range(0,len(splitDuration),2):
                activityId = activityId + 1
                activityIdSet.add(activityId)
                # get first lecture id in week
                if (i == 0):
                    activityGroupId = activityId
                activityXMLi = activityXML
                activityXMLi = activityXMLi + '\t<Id>'+str(activityId)+'</Id>\n'
                activityXMLi = activityXMLi + '\t<Activity_Group_Id>'+str(activityGroupId)+'</Activity_Group_Id>\n'
                activityXMLi = activityXMLi + '\t<Active>true</Active>\n'
                activityXMLi = activityXMLi + '\t<Comments></Comments>\n'
                activityXMLi = activityXMLi + '</Activity>\n'
                activityListXML = activityListXML + activityXMLi
            courseList[cIndex]['tutSections'][lIndex]['ids']=activityIdSet
    if 'labSections' in c:
        for lIndex, l in c['labSections'].items():
            activityXML = '<Activity>\n'
            activityXML = activityXML + '\t<Subject>'+cIndex+'</Subject>\n'
            for s in l['students']:
                activityXML = activityXML + '\t<Students>'+s+'</Students>\n'
            for i in l['instructors']:
                activityXML = activityXML + '\t<Teacher>'+i+'</Teacher>\n'
            activityTag = lIndex #'LAB' +'+'+ l['room'][0:4]+'+'+lIndex
            activityTagSet.add(activityTag)
            activityXML = activityXML + '\t<Activity_Tag>'+activityTag+'</Activity_Tag>\n'

            if (cIndex[0:3] == 'CCC'):
                activityTag = 'CCC'
                activityTagSet.add(activityTag)
                activityXML = activityXML + '\t<Activity_Tag>'+activityTag+'</Activity_Tag>\n'

            
            
            totalDuration = str(c['PracticalHoursPerWeek'])
            if (int(totalDuration) >= 12):
                print(cIndex + " abnormally high practical hours. Skipping")
                continue
            splitDuration = totalDuration # no splitting of lab hours
            activityXML = activityXML + '\t<Duration>'+splitDuration[0]+'</Duration>\n'
            activityXML = activityXML + '\t<Total_Duration>'+totalDuration+'</Total_Duration>\n'
            # add an acitivtyID for each contact session
            # needed for forcing lectures on diff days to to on same time 
            activityIdSet = set()
            for i in range(0,len(splitDuration),2):
                activityId = activityId + 1
                activityIdSet.add(activityId)
                # get first lecture id in week
                if (i == 0):
                    activityGroupId = activityId
                activityXMLi = activityXML
                activityXMLi = activityXMLi + '\t<Id>'+str(activityId)+'</Id>\n'
                activityXMLi = activityXMLi + '\t<Activity_Group_Id>'+str(activityGroupId)+'</Activity_Group_Id>\n'
                activityXMLi = activityXMLi + '\t<Active>true</Active>\n'
                activityXMLi = activityXMLi + '\t<Comments></Comments>\n'
                activityXMLi = activityXMLi + '</Activity>\n'
                activityListXML = activityListXML + activityXMLi
            courseList[cIndex]['labSections'][lIndex]['ids']=activityIdSet

##-------------------------------------------------------------------------
# TODO add Lunch activity and dummy lunch intstructor Set
##-------------------------------------------------------------------------
# add Lunch activity and dummy lunch intstructor Set
instructorSet = set()

# add lunch activity for each subgroup
lunchActivityIdSet = set()
lunchId = activityId+1
lunchInFourDaysXML = ''

for sg in studentGroups:
    
    for s in studentGroups[sg]:
        lunchInFourDaysXML = lunchInFourDaysXML + '<ConstraintMinDaysBetweenActivities>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Weight_Percentage>100</Weight_Percentage>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Consecutive_If_Same_Day>true</Consecutive_If_Same_Day>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Number_of_Activities>4</Number_of_Activities>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Activity_Id>'+str(lunchId)+'</Activity_Id>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Activity_Id>'+str(lunchId+1)+'</Activity_Id>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Activity_Id>'+str(lunchId+2)+'</Activity_Id>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Activity_Id>'+str(lunchId+3)+'</Activity_Id>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<MinDays>1</MinDays>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Active>true</Active>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '\t<Comments></Comments>\n'
        lunchInFourDaysXML = lunchInFourDaysXML + '</ConstraintMinDaysBetweenActivities>\n'
    
        lXML = '<Activity>\n'
        dummyInstructor = 'Lunch'+s
        instructorSet.add(dummyInstructor)
        
        lXML = lXML + '\t<Teacher>'+dummyInstructor+'</Teacher>\n'
        lXML = lXML + '\t<Subject>Lunch</Subject>\n'
        lXML = lXML + '\t<Activity_Tag></Activity_Tag>\n'
        lXML = lXML + '\t<Students>'+s+'</Students>\n'
        lXML = lXML + '\t<Duration>2</Duration>\n'
        lXML = lXML + '\t<Total_Duration>8</Total_Duration>\n'
        
        for i in range(4): # four activity for lunch on M, T, W, Fri. The lunch on Thursday is automatically in break hours
            if (i == 0):
                lunchGroupId = lunchId
            lXMLi = lXML # each lunch period is a new actvity
            lXMLi = lXMLi + '\t<Id>'+str(lunchId)+'</Id>\n'
            lXMLi = lXMLi + '\t<Activity_Group_Id>'+str(lunchGroupId)+'</Activity_Group_Id>\n'
            lXMLi = lXMLi + '\t<Active>true</Active>\n'
            lXMLi = lXMLi + '\t<Comments></Comments>\n'
            lXMLi = lXMLi + '</Activity>\n'
            
            activityListXML = activityListXML + lXMLi
            lunchId = lunchId  + 1

activityListXML = activityListXML+ '<!-- SPACE FOR MORE ACTIVITIES -->\n'
activityListXML = activityListXML+ '</Activities_List>\n'

formattedData = re.sub(
        r"<Activities_List>(.*?)</Activities_List>", activityListXML,
        formattedData,flags=re.DOTALL)

subjectListXML = '<Subjects_List>\n'
for cIndex in courseList:
    subjectListXML = subjectListXML + '<Subject>\n'
    subjectListXML = subjectListXML + '\t<Name>'+cIndex+'</Name>\n'
    subjectListXML = subjectListXML + '\t<Comments></Comments>\n'
    subjectListXML = subjectListXML + '</Subject>\n'
    
# add lunch subject
subjectListXML = subjectListXML + '<Subject>\n'
subjectListXML = subjectListXML + '\t<Name>Lunch</Name>\n'
subjectListXML = subjectListXML + '\t<Comments></Comments>\n'
subjectListXML = subjectListXML + '</Subject>\n'

subjectListXML = subjectListXML + '</Subjects_List>\n'
formattedData = re.sub(
        r"<Subjects_List>(.*?)</Subjects_List>", subjectListXML,
        formattedData,flags=re.DOTALL)

# add instute name
formattedData = re.sub(
        r"<Institution_Name>.*</Institution_Name>",
        '<Institution_Name>Shiv Nadar University</Institution_Name>',
        formattedData)

# add instute name
formattedData = re.sub(
        r"<Institution_Name>.*</Institution_Name>",
        '<Institution_Name>Shiv Nadar University</Institution_Name>',
        formattedData)

#days
timeTableDays = ['M','T','W','Th','F']

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


# fill in students list
formattedData = re.sub(
        r"<Students_List>(.*?)</Students_List>", studentsListXML,
        formattedData,flags=re.DOTALL)      

##----------------------------------------
#read roomsAndBuildingFile
with open('testData/rooms_and_buildings.csv', 'r') as ff:
  reader = csv.reader(ff)
  roomsAndBuilding = list(reader)

buildingSet = set('');
lectureRoomSetInA = set('');
lectureRoomSetInB = set('');
lectureRoomSetInCD = set('');

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
    
    
    if (room[0][0] == 'A') and (room[2] != 'Lab'):
        lectureRoomSetInA.add(room[0])
    if(room[0][0] == 'B') and (room[2] != 'Lab'):
        lectureRoomSetInB.add(room[0])
    if ((room[0][0] == 'C') or (room[0][0] == 'D'))  and (room[2] != 'Lab'):
        lectureRoomSetInCD.add(room[0])


                
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

allRoomSet = lectureRoomSetInA.union(lectureRoomSetInB).union(lectureRoomSetInCD)


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
#-------------------------------------------------------------

##--space constraint------------------------------------------

# basic compulsory constraint
spaceCons = '<Space_Constraints_List> \n \
<ConstraintBasicCompulsorySpace> \n \
    <Weight_Percentage>100</Weight_Percentage> \n \
    <Active>true</Active> \n \
    <Comments></Comments> \n \
</ConstraintBasicCompulsorySpace>\n'

roomArray = []
for s in allRoomSet:
    roomArray.append(s)
j = 0
# add a specific room preference for each lecture room
# so that each lecture happens in the same room
for cIndex, c in courseList.items():
    if 'lecSections' in c:
        for lIndex, l in c['lecSections'].items():
            if 'ids' in l:    
                for i in l['ids']:
                    spaceCons = spaceCons + '<ConstraintActivityPreferredRoom>\n'
                    spaceCons = spaceCons + '\t<Weight_Percentage>100</Weight_Percentage>\n'
                    spaceCons = spaceCons + '\t<Activity_Id>'+str(i)+'</Activity_Id>\n'
                    spaceCons = spaceCons + '\t<Room>'+roomArray[j]+'</Room>\n'
                    spaceCons = spaceCons + '\t<Permanently_Locked>false</Permanently_Locked>\n'
                    spaceCons = spaceCons + '\t<Active>true</Active>\n'
                    spaceCons = spaceCons + '\t<Comments></Comments>\n'
                    spaceCons = spaceCons + '\t</ConstraintActivityPreferredRoom>\n'
                j = (j+1) % len(allRoomSet)


# add lab room constraints
spaceCons = spaceCons + labRoomCons

spaceCons = spaceCons + '</Space_Constraints_List>\n'
    
#update file
formattedData = re.sub(
        r"<Space_Constraints_List>(.*?)</Space_Constraints_List>", spaceCons,
        formattedData,flags=re.DOTALL)      
    


######################################################
## -- end of space constratint



#### time constraints ##############################################333

# basic compulsory time constraint
tag = '<Time_Constraints_List>\n\
<ConstraintBasicCompulsoryTime>\n\
    <Weight_Percentage>100</Weight_Percentage>\n\
    <Active>true</Active>\n\
    <Comments></Comments>\n\
</ConstraintBasicCompulsoryTime>\n'

# add Th 12-2 break time
tag = tag + '<ConstraintBreakTimes> \n\
	<Weight_Percentage>100</Weight_Percentage> \n \
	<Number_of_Break_Times>4</Number_of_Break_Times> \n \
	<Break_Time> \n \
		<Day>Th</Day> \n \
		<Hour>12:00</Hour> \n \
	</Break_Time> \n \
	<Break_Time> \n \
		<Day>Th</Day> \n \
		<Hour>12:30</Hour> \n \
	</Break_Time> \n \
	<Break_Time> \n \
		<Day>Th</Day> \n \
		<Hour>13:00</Hour> \n \
	</Break_Time> \n \
	<Break_Time> \n \
		<Day>Th</Day> \n \
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
	<Number_of_Preferred_Starting_Times>16</Number_of_Preferred_Starting_Times> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>M</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>12:30</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>M</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>M</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:30</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>M</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>14:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
        	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>T</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>12:30</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>T</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>T</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:30</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>T</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>14:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
        	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>W</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>12:30</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>W</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>W</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:30</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>W</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>14:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
        	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>F</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>12:30</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>F</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>F</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>13:30</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
    	<Preferred_Starting_Time> \n \
		<Preferred_Starting_Day>F</Preferred_Starting_Day> \n \
		<Preferred_Starting_Hour>14:00</Preferred_Starting_Hour> \n \
	</Preferred_Starting_Time> \n \
	<Active>true</Active> \n \
	<Comments></Comments> \n \
</ConstraintActivitiesPreferredStartingTimes>\n'

tag = tag + lunchConsTag

# adding constraint of same lectures on diff days to be on same time
for cIndex, c in courseList.items():
    if 'lecSections' in c:
        for lIndex, l in c['lecSections'].items():
            
            # same lecture on diff days should have same time slots
            if 'ids' in l:
                tag = tag + '<ConstraintActivitiesSameStartingHour>\n'
                tag = tag + '\t<Weight_Percentage>100</Weight_Percentage>\n'
                tag = tag + '\t<Number_of_Activities>'+str(len(l['ids']))+'</Number_of_Activities>\n'
                
                for id in l['ids']:
                    tag = tag+ '\t\t<Activity_Id>'+str(id)+'</Activity_Id>\n'
                tag = tag + '\t<Active>true</Active>\n'
                tag = tag + '\t<Comments></Comments>\n'
                tag = tag + '</ConstraintActivitiesSameStartingHour>\n'
                
                
            # slots in FET are of half hours. 1 hour class is 2 consecutive slot and 
            # a 1.5 hours class  is consecutive 3 slots.
            if 'ids' in l:
                tag = tag + '<ConstraintMinDaysBetweenActivities> \n'
                tag = tag + '\t<Weight_Percentage>100</Weight_Percentage>\n'
                tag = tag + '\t<Consecutive_If_Same_Day>true</Consecutive_If_Same_Day>\n'
                tag = tag + '\t<Number_of_Activities>'+str(len(l['ids']))+'</Number_of_Activities>\n'
                                
                for id in l['ids']:
                    tag = tag+ '\t\t<Activity_Id>'+str(id)+'</Activity_Id>\n'
                    
                tag = tag + '\t<MinDays>2</MinDays>\n'
                tag = tag + '\t<Active>true</Active>\n'
                tag = tag + '\t<Comments></Comments>\n'
                tag = tag + '</ConstraintMinDaysBetweenActivities>\n'
            
        
            
tag = tag+ lunchInFourDaysXML

# add CCC overlapping constratint
import overlappingCCCstring as overlappCCC
tag = tag+overlappCCC.x

tag = tag+ '</Time_Constraints_List>\n'




##  end time constraints

# write your content in n new file
formattedData = re.sub(
        r"<Time_Constraints_List>(.*?)</Time_Constraints_List>",tag ,
        formattedData,flags=re.DOTALL)      
###############################################



#####################################################
# the activities.csv needs to loaded at the FET interface



# read instructos set
for cIndex, c in courseList.items():
    if 'lecSections' in c:
        for sId,s in c['lecSections'].items():
            instructorSet = instructorSet.union(set(s['instructors']))
            
    if 'tutSections' in c:
        for sId,s in c['tutSections'].items():
            instructorSet = instructorSet.union(set(s['instructors']))
            
    if 'labSections' in c:
        for sId,s in c['labSections'].items():
            instructorSet = instructorSet.union(set(s['instructors']))
            

teachersXML = '<Teachers_List>\n'
for i in instructorSet:
    teachersXML = teachersXML + '<Teacher>\n'
    teachersXML = teachersXML + '\t<Name>'+i+'</Name>\n'
    teachersXML = teachersXML + '\t<Target_Number_of_Hours>0</Target_Number_of_Hours>\n'
    teachersXML = teachersXML + '\t<Qualified_Subjects></Qualified_Subjects>\n'
    teachersXML = teachersXML + '\t<Comments></Comments>\n'
    teachersXML = teachersXML + '</Teacher>\n'

teachersXML = teachersXML + '</Teachers_List>\n'
# write your content in n new file
formattedData = re.sub(
        r"<Teachers_List>(.*?)</Teachers_List>",teachersXML ,
        formattedData,flags=re.DOTALL)      


# write activity tags in fet
activityTagListXML = '<Activity_Tags_List>\n'

for a in activityTagSet:
    activityTagListXML = activityTagListXML + '<Activity_Tag>\n'
    activityTagListXML = activityTagListXML + '\t<Name>'+a+'</Name>\n'
    activityTagListXML = activityTagListXML + '\t<Printable>true</Printable>\n'
    activityTagListXML = activityTagListXML + '\t<Comments></Comments>\n'
    activityTagListXML = activityTagListXML + '</Activity_Tag>\n'

activityTagListXML = activityTagListXML + '</Activity_Tags_List>\n'    
formattedData = re.sub(
        r"<Activity_Tags_List>(.*?)</Activity_Tags_List>",activityTagListXML,
        formattedData,flags=re.DOTALL)      

## write file

f = open(fetFileName,'w+')
f.write(formattedData)
f.close





dayFile = 'trash.xml'
g = open(dayFile,'w')
g.write("trash")
g.close
