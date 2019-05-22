#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 2019

@author: ajit
"""


#TODO: Work on CCC  courses

#TODO: adding all majors and minors to all electives is overconstraining
#TOTO: add majors in elective with probilty 0.5
#TODO: add minors in minor electives with prabability 0.3 

# read major minor preferences
from readMajorMinorPreferences import *


# read excel file
# data stored as a dictionary in courseList
from readCourseOfferingFromExcel import *


# extract list of   instructors
instructors = set()
for cIndex, c in courseList.items():    
    # collect lecture instructos name
    if 'lecSections' in c:
        for insListIndex, insList in c['lecSections'].items():
           for i in insList:
               instructors.add(i)
               
    # collect tutorial instructos name
    if 'tutSections' in c:
       for insListIndex, insList in c['tutSections'].items():
           for i in insList:
               instructors.add(i)
               
    # collect lab instructos name
    if 'labSections' in c:
       for insListIndex, insList in c['labSections'].items():
           for i in insList['instructors']:
               instructors.add(i)
               
               
# add minor students in courseList['programs']
'''
for cIndex, c in courseList.items():
    if ('Elective' in c['PartofMinoras']) or ('Compulsory' in c['PartofMinoras']):
        y = cIndex[3] # course level
        d = cIndex[0:3]
        
        if (y == '5'): # hard resetting MAT522 for year 4 
            y = '4'
            
        # check if anyone one wants to do minor in d
        if d in minorSeeker:
            # add year y, y+1 subgroups of students doing minor in d as this course students
            yp1 = str(min(int(y)+1,4)) # yp1 = min(y+1, 4), don't want to go beyond fouth year, right?
            dMinorSeekers = minorSeeker[d]
            
            # adding year y
            for j in dMinorSeekers:
                minJd = j+y+d
                if minJd in studentsGroup[j+y]['subgroups']:
                    c['programs'][minJd] = studentsGroup[j+y]['subgroups'][minJd]
                    
            # adding year yp1
            for j in dMinorSeekers:
                minJd = j+yp1+d
                if minJd in studentsGroup[j+yp1]['subgroups']:
                    c['programs'][minJd] = studentsGroup[j+yp1]['subgroups'][minJd]
'''

        
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
            
        
               
               
               
# map courses to activities
tutDurationSet = set()
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
      
activityId = 0
    
for cIndex, c in courseList.items():
    if 'lecSections' in c:
        for lIndex, l in c['lecSections'].items():
            
            studentSet = ''
            for s in l['students']:
                studentSet = studentSet+'+'+s
            studentSet = studentSet[1:]
            subject = cIndex
            
            teachers = ''
            for i in l['instructors']:
                teachers = teachers +'+' + i
            teachers = teachers[1:]
            
            activityTag = 'LEC+AnyRoom+'+lIndex
            totalDuration = str(c['LectureHoursPerWeek'])
            if (int(totalDuration) >= 12):
                print(cIndex + " abnormally high lecture hours. Skipping")
                continue
            
            lecDuration = str(c['LectureDuration'])
            splitDuration = splitLec(totalDuration,lecDuration)
            minDays = ''
            weight = ''
            consecutive = ''
            if (len(splitDuration) >= 2):
                minDays = '1'
                weight = '95'
                consecutive = '1'
                
            # add an acitivtyID for each contact session
            # needed for forcing lectures on diff days to to on same time 
            activityIdSet = set()
            for i in range(0,len(splitDuration),2):
                activityId = activityId + 1
                activityIdSet.add(activityId)
                
            courseList[cIndex]['lecSections'][lIndex]['ids']=activityIdSet
            
            
            row = studentSet+','+subject+','+teachers+','+activityTag+','+totalDuration+','+splitDuration+','+minDays+','+weight+','+consecutive+'\n'
            activityString = activityString+row

    if 'tutSections' in c:
        for lIndex, l in c['tutSections'].items():
            
            studentSet = ''
            for s in l['students']:
                studentSet = studentSet+'+'+s
            studentSet = studentSet[1:]
            subject = cIndex
  
            teachers = ''
            for i in l['instructors']:
                teachers = teachers +'+' + i
            teachers = teachers[1:]
            
            activityTag = 'TUT+AnyRoom+'+lIndex
            totalDuration = str(c['TutorialHoursPerWeek'])
            if (int(totalDuration) >= 12):
                print(cIndex + " abnormally high lecture hours. Skipping")
                continue

            
            
            splitDuration = splitLec(totalDuration,'3')
            minDays = ''
            weight = ''
            consecutive = ''
            
            # add an acitivtyID for each contact session
            # needed for forcing lectures on diff days to to on same time 
            activityIdSet = set()
            for i in range(0,len(splitDuration),2):
                activityId = activityId + 1
                activityIdSet.add(activityId)
            courseList[cIndex]['tutSections'][lIndex]['ids']=activityIdSet

                
            row = studentSet+','+subject+','+teachers+','+activityTag+','+totalDuration+','+splitDuration+','+minDays+','+weight+','+consecutive+'\n'
            activityString = activityString+row

    if 'labSections' in c:
        for lIndex, l in c['labSections'].items():
            
            studentSet = ''
            for s in l['students']:
                studentSet = studentSet+'+'+s
            studentSet = studentSet[1:]
            
            subject = cIndex
            
            teachers = ''
            for i in l['instructors']:
                teachers = teachers +'+' + i
            teachers = teachers[1:]
            
            activityTag = 'LAB' +'+'+ l['room'][0:4]+'+'+lIndex
            
            totalDuration = str(c['PracticalHoursPerWeek'])
            if (int(totalDuration) >= 12):
                print(cIndex + " abnormally high lecture hours. Skipping")
                continue

            
            splitDuration = totalDuration # no splitting of lab hours
            minDays = ''
            weight = ''
            consecutive = ''
            
            # add an acitivtyID for each contact session
            # needed for forcing lectures on diff days to to on same time 
            activityIdSet = set()
            for i in range(0,len(splitDuration),2):
                activityId = activityId + 1
                activityIdSet.add(activityId)
                
            courseList[cIndex]['labSections'][lIndex]['ids']=activityIdSet

            row = studentSet+','+subject+','+teachers+','+activityTag+','+totalDuration+','+splitDuration+','+minDays+','+weight+','+consecutive+'\n'
            activityString = activityString+row
            
f = open("activityTest01.csv", "w")
f.write(activityString)
f.close()    
    
#--------------------------------------------------------
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
timeTableDays = ['M','T','W','Th','F']

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
#         '17:00',
#         '17:30',
#         '18:00',
#         '18:30',
#          '19:00',
#          '19:30',
#          '20:00',
#          '20:30'
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

## fill in student groups list
tag = '<Students_List> \n'
for sIndex, s in studentsGroup.items():
    tag = tag + '<Year> \n\
        <Name>'+sIndex+'</Name> \n\
        <Number_of_Students>'+str(s['number']) +'</Number_of_Students>\n\
        <Comments></Comments> \n'
    
        
    for sgIndex, sg in s['subgroups'].items():
            tag = tag +  '\t<Group> \n \t\t<Name>'+ sgIndex + '</Name>\n \t\t<Number_of_Students>'+str(sg)+'</Number_of_Students>\n \t\t<Comments></Comments>\n \t</Group> \n'
            
    tag = tag+'</Year>\n'

tag = tag+'\n</Students_List>'

#update file
formattedData = re.sub(
        r"<Students_List>(.*?)</Students_List>", tag,
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

# all room - tag AnyRoom
spaceCons = spaceCons + '<ConstraintActivityTagPreferredRooms> \n \
    <Weight_Percentage>100</Weight_Percentage> \n \
    <Activity_Tag>AnyRoom</Activity_Tag> \n \
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


# adding constraint of same lectures on diff days to be on same time
for cIndex, c in courseList.items():
    if 'lecSections' in c:
        for lIndex, l in c['lecSections'].items():
            if 'ids' in l:
                tag = tag + '<ConstraintActivitiesSameStartingHour>\n'
                tag = tag + '\t<Weight_Percentage>100</Weight_Percentage>\n'
                tag = tag + '\t<Number_of_Activities>'+str(len(l['ids']))+'</Number_of_Activities>\n'
                
                for id in l['ids']:
                    tag = tag+ '\t\t<Activity_Id>'+str(id)+'</Activity_Id>\n'
                tag = tag + '\t<Active>true</Active>\n'
                tag = tag + '\t<Comments></Comments>\n'
                tag = tag + '</ConstraintActivitiesSameStartingHour>\n'
            
tag = tag + '</Time_Constraints_List>\n'
##  end time constraints

# write your content in n new file
formattedData = re.sub(
        r"<Time_Constraints_List>(.*?)</Time_Constraints_List>",tag ,
        formattedData,flags=re.DOTALL)      
###############################################



#####################################################
# the activities.csv needs to loaded at the FET interface




## write file

dataFile = 'loadedData.fet'
f = open(dataFile,'w+')
f.write(formattedData)
f.close





dayFile = 'trash.xml'
g = open(dayFile,'w')
g.write("trash")
g.close

#<ConstraintActivitiesSameStartingHour>
#    <Weight_Percentage>100</Weight_Percentage>
#    <Number_of_Activities>3</Number_of_Activities>
#    <Activity_Id>1</Activity_Id>
#    <Activity_Id>2</Activity_Id>
#    <Activity_Id>3</Activity_Id>
#    <Active>true</Active>
#    <Comments></Comments>
#</ConstraintActivitiesSameStartingHour>

