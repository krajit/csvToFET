#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 2019

@author: ajit
"""

import random, xlrd
from colorama import Fore, Back, Style

# some preparotory instructions
print(Fore.RED+ '\nWarning: File downloaded from COS contains Ziaur Rehman. It is a dummy instructor name. Make sure to replace it with unique name for each activity.\n')

print(Fore.RED+ '\nWarning: Large courses with multiple tutorials generally have instructor names in the tutorials section. Make sure to replace that with course code + TAi to get accurate time table.\n')
print(Style.RESET_ALL)

numCCC  = 0 # expteced number of CCC
maxNumOfAllowedUWE = 0
numMajorElectives = 0
activityCsvFileName =  "generatedActivities/activityTest01.csv"
fetFileName = 'generatedActivities/snu-timetable.fet'

# hours, written vertically aligned to easily comment out few slots
slots = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00',
         '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
         '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00',
         '18:30', '19:00', '19:30']


# read major minor preferences as filled by UG advisers
# create subgroup of students based on minor preferences
filePath = "testData/SNU - popular minors data survey (Responses).xlsx"
## NOTE: make sure to remove duplicate department rows manually

# excel files have rather long names, lets shorten them
sName = {
        'Chemical Engineering' : 'CHD',
        'Civil Engineering' : 'CED',
        'Computer Science and Engineering' : 'CSD',
        'Electrical Engineering' : 'EED',
        'Mechanical Engineering' : 'MED',
        'Art & Performing Art' : 'ADP',
        'Communication' : 'COM',
        'Design' : 'DES',
        'Economics' : 'ECO',
        'English' : 'ENG',
        'History' : 'HIS', 
        'International Relations and Governance Studies' : 'INT',
        'Sociology' : 'SOC',
        'Management': 'MGT',
        'Chemistry' : 'CHY',
        'Life Sciences' : 'BIO', 
        'Mathematics' : 'MAT',
        'Physics' : 'PHY',
        'Archaeology' : 'HIS', # TODO: check which dept offers history 
        'Biotechnology' : 'BIO',
        'Chemistry' : 'CHY',
        'Dance' : 'ADP',  # TODO: check which dept offers dance
        'Data Analytics': 'MGT', # TODO: check which dept offers data analytics
        'Electronics and Communication Engineering' : 'ECE',
        'International Relations and Public Affairs': 'INT',
        'Electrical and Electronics Engineering': 'EED',
        'International Relations': 'INT',
        'Art Design and Performing Arts': 'ADP',
        'Bachelor of Management Studies': 'MGT',
        'Under Graduate': 'UGG',
        'OHM': 'MGT',
        'General Management': 'MGT',
        'FAC': 'MGT',
        'STM': 'MGT',
        'DOM': 'MGT'         
        }



wb = xlrd.open_workbook(filePath) 
sheet = wb.sheet_by_index(0) # get first sheet
  
deptCol = 3
popularMinor = dict() # major(students) and minors(dept)

for i in range(1,sheet.nrows):
    dept = sheet.cell_value(i,deptCol) # read dept names
    dept = sName[dept]                 # get short name for dept
    popularMinor[dept] = []
    
    for j in range(deptCol+1,deptCol+6):
        if (sheet.cell_type(i,j) != xlrd.XL_CELL_EMPTY):
            if (sheet.cell_value(i,j) != 'None'):
                popularMinor[dept].append(sName[sheet.cell_value(i,j)])
    
minorSeeker = dict()
numMinor = 2 # only first two pref are accounted for now. 
             # Change this value to 5 to include all pref

for i,dep in popularMinor.items():
    k = min(len(dep), numMinor)
    
    for j in range(k):
        if dep[j] in minorSeeker:
            minorSeeker[dep[j]].add(i)
        else:
            minorSeeker[dep[j]] = set()
            minorSeeker[dep[j]].add(i)
            
            
#            
#studentSet = {'BIO1',  'BIO2',  'BIO3',  'BIO4',  'CED1',  'CED2',  'CED3',  'CED4',
# 'CHD1',  'CHD2',  'CHD3',  'CHD4',  'CHY1',  'CHY2',  'CHY3',  'CHY4',
# 'CSD1',  'CSD2',  'CSD3',  'CSD4',  'ECE1',  'ECE2',  'ECE3',  'ECE4',
# 'ECO1',  'ECO2',  'ECO3',  'ECO4',  'EED1',  'EED2',  'EED3',  'EED4',
# 'ENG1',  'ENG2',  'ENG3',  'ENG4',  'HIS1',  'HIS2',  'HIS3',  'HIS4',  'INT1', 'INT2',
# 'MAT1',  'MAT2',  'MAT3',  'MAT4',  'MED1',  'MED2',  'MED3',  'MED4',
# 'MGT1',  'MGT2',  'MGT3',  'MGT4',  'PHY1',  'PHY2',  'PHY3',  'PHY4',
# 'SOC1',  'SOC2',  'SOC3',  'SOC4',  'UG1'}
#            
#            


wb = xlrd.open_workbook('testData/studentsData.xlsx') 
sheet = wb.sheet_by_index(0) # get first sheet
   
studentsGroup = dict()
for i in range(1,sheet.nrows):
    s = sheet.cell_value(i,0)
    n = int(sheet.cell_value(i,1))
    
    studentsGroup[s] = dict()
    studentsGroup[s]['number'] = n
    studentsGroup[s]['subgroups'] = {s+'NoMinor': n}
    

# make subgroups in studentGroup
# only in 2nd to 4th year
for sIndex, s in studentsGroup.items():
    
    y = sIndex[-1] #year
    d = sIndex[:-1] # dept
    
    # pass over first year students
    # TODO: Work on grouping first year studetns
    if (y == '1'):
        continue
    
    if d in popularMinor:
        n = min(len(popularMinor[d]),numMinor) # number of subgroups
        # weights
        # w1 + w2 + ... wn = 1
        # wi = i*a
        a = 2.0/(n*(n+1))
        for i in reversed(range(n)):
            wi = (i+1)*a
            ni = round(wi*int(s['number']))
            si = sIndex+popularMinor[d][i]
            s['subgroups'][si] = ni
            s['subgroups'][sIndex+'NoMinor'] = s['subgroups'][sIndex+'NoMinor'] - ni 
# end grouping students

# write subgroups in csv
            
studentToCsv = 'Year,Number of Students per Year,Group, Number of Students per Group,Subgroup, Number of Students per Subgroup\n'

for sIndex, s in studentsGroup.items():
    for sgIndex, sg in s['subgroups'].items():
        rowi = sIndex+','+str(s['number'])+','+sgIndex+','+ str(sg)+' , ,\n'
        
        #try without any subgroup
        #rowi = sIndex+','+str(s['number'])+','+''+','+ ''+' , ,\n'
        studentToCsv = studentToCsv + rowi
        
f = open("studentsGroup.csv", "w")
f.write(studentToCsv)
f.close()    
    


# read excel file
# data stored as a dictionary in courseList
#---------------------------------------------
filePath = "testData/Offered_Course_List_spring2019.xlsx"
wb = xlrd.open_workbook(filePath) 
sheet = wb.sheet_by_index(0) # get first sheet
  
# column heading numbers
School	=	0
Department	=	1
CourseCode	=	2
CourseTitle	=	3
Credits	=	4
CourseType	=	5
OpenasUWE	=	6
PartofMinoras	=	7
Programs	=	[8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
CourseCapacity	=	18
LectureHoursPerWeek	=	19
TutorialHoursPerWeek	=	20
PracticalHoursPerWeek	=	21
LectureDuration	=	22
LectureSections	=	23
TutorialSections	=	24
PracticalSections	=	25
LectureInstructors	=	26
TutorialInstructors	=	27
PracticalInstructors	=	28
LabRoomNumber	=	29
LabCapacity	=	30
SpecialRequirement	=	31
LectureSlottedoutsideMonFriand95	=	32
TutorialSlottedoutsideMonFriand95	=	33
PracticalSlottedoutsideMonFriand95	=	34
LectureRemarks	=	35
TutorialRemarks	=	36
PracticalRemarks	=	37
CourseCoordinator	=	38
LectureCredits	=	39
TutorialCredits	=	40
PracticalCredits	=	41
AssessmentTypeWeightage	=	42
CrossListedwith	=	43
Prerequisite	=	44
Crosslistedcourseoffered	=	45
Lasttimeofferedsemester	=	46



courseList = dict()

for i in range(1,sheet.nrows):
    
    
    # loop over courseCode column, make a dictionary for each course
    # if a cell in this column is empty, that means that row has details of 
    # last defined course code
    
    # skip over empty cells 
    if (sheet.cell_type(i,CourseCode) == xlrd.XL_CELL_EMPTY):
        continue
        
    j = 0 # How many EXTRA rows for a particular course
    if ((i+j+1) < sheet.nrows):
        while (sheet.cell_type(i+j+1,CourseCode) == xlrd.XL_CELL_EMPTY):
            j = j+1
       
    cCode = sheet.cell_value(i,CourseCode)

    courseList[cCode] = dict()
    
    courseI = courseList[cCode]
    courseI['Credits'] = int(sheet.cell_value(i,Credits))
    courseI['Title'] = sheet.cell_value(i,CourseTitle)
    courseI['CourseType'] = sheet.cell_value(i,CourseType)
    
    if (courseI['CourseType'] != 'CCC'):
        courseI['level'] = cCode[-3]
    else:
        courseI['level'] = 0
    
    courseI['OpenasUWE'] = sheet.cell_value(i,OpenasUWE)
    courseI['PartofMinoras'] = sheet.cell_value(i,PartofMinoras)
    
    
    # read target audience of the course
    courseI['programs'] = dict()
    for p in Programs:
        if (sheet.cell_type(i,p) != xlrd.XL_CELL_EMPTY):
            cellVal = sheet.cell_value(i,p)
            cellVal = sName[cellVal[:-1]]+cellVal[-1]
            courseI['programs'][cellVal] = studentsGroup[cellVal]['number']
            
    # read number lecture hours    
    if (sheet.cell_type(i,LectureHoursPerWeek) == xlrd.XL_CELL_EMPTY):
        courseI['LectureHoursPerWeek']=0
    else:
        courseI['LectureHoursPerWeek']=int(2*float(sheet.cell_value(i,LectureHoursPerWeek)))
        courseI['LectureDuration']=int(2*float(sheet.cell_value(i,LectureDuration)))
        
        
        
    #read number of tutorials hours
    if (sheet.cell_type(i,TutorialHoursPerWeek) == xlrd.XL_CELL_EMPTY):
        courseI['TutorialHoursPerWeek']=0
    else:
        courseI['TutorialHoursPerWeek']=int(2*float(sheet.cell_value(i,TutorialHoursPerWeek)))
        
    #read number of lab hours
    if (sheet.cell_type(i,PracticalHoursPerWeek) == xlrd.XL_CELL_EMPTY):
        courseI['PracticalHoursPerWeek']=0
    else:
        courseI['PracticalHoursPerWeek']=int(2*float(sheet.cell_value(i,PracticalHoursPerWeek)))
        
    # read lecture sections and respective instructors
    if (courseI['LectureHoursPerWeek'] >= 1):
        
        courseI['lecSections'] = dict()
        if (j == 0):
            seci = 'LEC1'
            courseI['lecSections'][seci] = dict()
            courseI['lecSections'][seci]['instructors'] = sheet.cell_value(i,LectureInstructors).split(',\n')[:-1]
            
            
            courseI['lecSections'][seci]['students'] = set()
        else:
            for k in range(i,i+j+1):
                if (sheet.cell_type(k,LectureSections) != xlrd.XL_CELL_EMPTY):
                    seci = sheet.cell_value(k,LectureSections)
                    courseI['lecSections'][seci] = dict()
                    courseI['lecSections'][seci]['instructors'] = sheet.cell_value(k,LectureInstructors).split(',\n')[:-1]
                    courseI['lecSections'][seci]['students'] = set()
                   
         
            
    # read tut sections and respective instructors
    
    if (courseI['TutorialHoursPerWeek'] >= 1):
        courseI['tutSections'] = dict()
        
        if (j == 0) :
            seci = 'TUT1'
            courseI['tutSections'][seci] = dict()
            courseI['tutSections'][seci]['instructors'] = sheet.cell_value(i,TutorialInstructors).split(',\n')[:-1]
            courseI['tutSections'][seci]['students'] = set()
        else:
            for k in range(i,i+j+1):
                if (sheet.cell_type(k,TutorialSections) != xlrd.XL_CELL_EMPTY):
                    seci = sheet.cell_value(k,TutorialSections)
                    courseI['tutSections'][seci] = dict()
                    courseI['tutSections'][seci]['instructors'] = sheet.cell_value(k,TutorialInstructors).split(',\n')[:-1]
                    courseI['tutSections'][seci]['students'] = set()

            

    # read Lab sections, respective instructors, and lab room number
    if (courseI['PracticalHoursPerWeek'] >= 1):
       courseI['labSections'] = dict()
       if (j == 0):
           praci = 'PRAC1'
           courseI['labSections'][praci] = dict()
           courseI['labSections'][praci]['instructors'] =  sheet.cell_value(i,PracticalInstructors).split(',\n')[:-1]
           courseI['labSections'][praci]['students'] =  set()
           courseI['labSections'][praci]['room'] =  sheet.cell_value(i,LabRoomNumber) 
           courseI['labSections'][praci]['students'] = set()
            
       else:
           for k in range(i,i+j+1):
               if (sheet.cell_type(k,PracticalSections) != xlrd.XL_CELL_EMPTY):
                    praci = sheet.cell_value(k,PracticalSections)
                    courseI['labSections'][praci] = dict()
                    courseI['labSections'][praci]['instructors'] =  sheet.cell_value(k,PracticalInstructors).split(',\n')[:-1]
                    courseI['labSections'][praci]['room'] =  sheet.cell_value(k,LabRoomNumber)
                    courseI['labSections'][praci]['students'] = set()
       
   
# create a dictionary major electives, minor electives and UWEs
majorElectives = dict()
minorElectives = dict()
UWEnotInMinors = dict()


for cIndex, c in courseList.items():
    d = cIndex[0:3] # dept
    y = cIndex[3]   # year
        
    # combine many business school minor in one
    if (d == 'MKT') or (d == 'DOM') or (d == 'FAC') or (d == 'OHM') or (d == 'STM'):
        d = 'MGT'
        
    if (int(y) >= 4):
        y = '4'

    #combine year and dept again
    d = d+y
    
    # update the list of major electives
    if 'Major Elective' in c['CourseType']:
        if d in majorElectives:
            majorElectives[d].add(cIndex)
        else:
            majorElectives[d] = set()
            majorElectives[d].add(cIndex)

    # update list of minor electives
    # treat UWE which are not part of minors as minor electives
    #    for time-tabling purpose
    if 'Elective' in c['PartofMinoras']:
        if d in minorElectives:
            minorElectives[d].add(cIndex)
        else:
            minorElectives[d] = set()
            minorElectives[d].add(cIndex)

    if ('Not a part' in c['PartofMinoras']) and ('Yes' in c['OpenasUWE']):
        if d in UWEnotInMinors:
            UWEnotInMinors[d].add(cIndex)
        else:
            UWEnotInMinors[d] = set()
            UWEnotInMinors[d].add(cIndex)

        
    
# extract a list of CCC
CCCcourses = set()
for cIndex in courseList:
    if 'CCC' in cIndex:
        CCCcourses.add(cIndex)    

ni = int(len(CCCcourses)/4)
# make four groups of CCC courses
# group i will be open to all year-i students

CCC = dict()
CCC['year1'] = random.sample(CCCcourses,ni)
CCCcourses.difference_update(CCC['year1'])

CCC['year2'] = random.sample(CCCcourses,ni)
CCCcourses.difference_update(CCC['year2'])

CCC['year3'] = random.sample(CCCcourses,ni)
CCCcourses.difference_update(CCC['year3'])

CCC['year4'] = CCCcourses

###--------------------------------------------------------------------------


## helper function to decide is a course should removed from the offerning or not
#def removeWithProbability(prob):
#    x = random.uniform(0,1)
#    if (x < prob):
#        return True
#    else:
#        return False
#    
#
## remove a percentage of UWE for easing out the timetable
#p = 0.30 # prability of removal 
#outputFileName = 'SNU-p-'+str(p)+'.fet'   
#coursesTobeRemoved = set()
#    
#for mIndex, mi  in majorElectives.items():
#    for c in mi:
#        if removeWithProbability(p):
#            coursesTobeRemoved.add(c)
#    
#for mIndex, mi  in minorElectives.items():
#    for c in mi:
#        if removeWithProbability(p):
#            coursesTobeRemoved.add(c)
#            
#for mIndex, mi  in UWEnotInMinors.items():
#    for c in mi:
#        if removeWithProbability(p):
#            coursesTobeRemoved.add(c)
#            
#            
#for c in coursesTobeRemoved:
#    del courseList[c]
#    
#    for i in list(majorElectives):
#        if c in majorElectives[i]:
#            majorElectives[i].remove(c)
#            
#    for i in list(minorElectives):
#        if c in minorElectives[i]:
#            minorElectives[i].remove(c)
#            
#    for i in list(UWEnotInMinors):
#        if c in UWEnotInMinors[i]:
#            UWEnotInMinors[i].remove(c)
#    
#print('For testing purpose: '+str(int(len(coursesTobeRemoved)*100/len(courseList)))+'% elective courses removed')





################################################
# extract list of instructors
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

# clean up major elective course from the list given from COS
# The major electives are populated with all major students which is putting a lot of constraint on the time-tabling
for me in majorElectives:
    for c in majorElectives[me]:
        courseList[c]['programs'] = dict() # reset student list of major electives

# add each other than ****NonMinor subgroup in a maximum of 2 major electives

studentSubgroupSet = set()

for si in studentsGroup:
    s = studentsGroup[si]
    if (len(s['subgroups']) == 1):
        # this has no subgroups
        studentSubgroupSet.add(si)
    else:
        # has multiple subgroups
        for sgi in s['subgroups']:
            if (sgi[4:] != 'NoMinor'):
                studentSubgroupSet.add(sgi)
                
# iterate over this set, and add each subgroup in 2 randomly chosen electives from 
for s in studentSubgroupSet:
    sMajor = s[0:3]
    y         = s[3]
    ym1       = str(max(int(y) - 1, 1)) # ym1 = max(y-1, 1)
    yp1       = str(min(int(y) + 1, 4)) # yp1 = min(y+1, 1)    
    my = sMajor+y
    mym1 = sMajor + ym1
    myp1 = sMajor + yp1
    
    # majorElective choices for the group
    sMajorElectiveChoices = set()
    if mym1 in majorElectives:
        sMajorElectiveChoices = sMajorElectiveChoices.union(majorElectives[mym1])
    if my in majorElectives:
        sMajorElectiveChoices = sMajorElectiveChoices.union(majorElectives[my])
    if myp1 in majorElectives:
        sMajorElectiveChoices = sMajorElectiveChoices.union(majorElectives[myp1])

    
    # if the set is non empty
    if (len(sMajorElectiveChoices) > 0):
        k = min(len(sMajorElectiveChoices), numMajorElectives) # adjust number of major electives if there are only one choice
        
        # choose k items from sMajorElectiveChoicse
        sToBeAddedIn = random.sample(sMajorElectiveChoices, k)
        
        # add s in each of sToBeAddedIn
        for c in sToBeAddedIn:
            courseList[c]['programs'][s] = 10


# add student subgroups in courses as UWE (inlcuding minors). Max UWE per subgroup is 2
#######################################################################
# maintain a dictionary of how many minors or UWE each subgroup can enroll
            


allowedNumOfUWE = dict()
for sIndex, s in studentsGroup.items():
    for sgIndex, sg in s['subgroups'].items():
        
        if (sgIndex[-7:] != 'NoMinor'):  # only add minor subgroups       
            allowedNumOfUWE[sgIndex] = maxNumOfAllowedUWE
               
#######################################################################
               
# add minor students in courseList['programs']
# only if the couse is compulsory for minors
for cIndex, c in courseList.items():
    #if ('Elective' in c['PartofMinoras']) or ('Compulsory' in c['PartofMinoras']):
    if ('Compulsory' in c['PartofMinoras']):
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
                    allowedNumOfUWE[minJd] = allowedNumOfUWE[minJd] - 1 
                    
            # adding year yp1
            for j in dMinorSeekers:
                minJd = j+yp1+d
                if minJd in studentsGroup[j+yp1]['subgroups']:
                    c['programs'][minJd] = studentsGroup[j+yp1]['subgroups'][minJd]
                    allowedNumOfUWE[minJd] = allowedNumOfUWE[minJd] - 1


for sg in allowedNumOfUWE:
    # need to assign k number of UWE to each group
    minorIn = sg[4:]
    y = sg[3] # year
    ym1 = str(int(y) - 1)   # year -1
    
    minor1 = minorIn+y
    minor2 = minorIn+ym1

    # first choose UWE from minor electives
    if (allowedNumOfUWE[sg] > 0):
        minorElectiveCoursesForSG = set()
        if minor1 in minorElectives:
            minorElectiveCoursesForSG = minorElectiveCoursesForSG.union(minorElectives[minor1])

        if minor2 in minorElectives:
            minorElectiveCoursesForSG = minorElectiveCoursesForSG.union(minorElectives[minor2])
            
        n = len(minorElectiveCoursesForSG)

        # n might be smaller than k
        k = min(n,allowedNumOfUWE[sg])
        if (k > 0):
            minorCoursesAssignedToSG = random.sample(minorElectiveCoursesForSG,k)
            # add these  students group sg to these courses
            for c in minorCoursesAssignedToSG:
                courseList[c]['programs'][sg] = 10
        # ki number of UWE courses have been assigned from minor electives
        allowedNumOfUWE[sg] = allowedNumOfUWE[sg] - k 
        
        # if the group still needs to take more UWE, it can take from UWE from minor dept, 
        # which are not part of minors
        
    # choose UWE from minor dept courses but which are not part of minors
    if (allowedNumOfUWE[sg] > 0):
        UWEForSG = set()
        if minor1 in UWEnotInMinors:
            UWEForSG = UWEForSG.union(UWEnotInMinors[minor1])

        if minor2 in UWEnotInMinors:
            UWEForSG = UWEForSG.union(UWEnotInMinors[minor2])
            
        n = len(UWEForSG)

        # n might be smaller than k
        k = min(n,allowedNumOfUWE[sg])
        if (k > 0):
            UWEassignedForSG = random.sample(UWEForSG,k)
            # add these  students group sg to these courses
            for c in UWEassignedForSG:
                courseList[c]['programs'][sg] = 10
        # ki number of UWE courses have been assigned from minor electives
        allowedNumOfUWE[sg] = allowedNumOfUWE[sg] - k 

####---------------------------------------------------
#### Adding year groups in CCC couurses
#for s in studentsGroup:
#    y = s[-1]
#    yeari = 'year' + y
#    
#    # add this student group in all CCC courses of yeari
#    CCCi = CCC[yeari]
#      
#    
#    # add all first year student in all CCCi course
#    for c in CCCi:
#        courseList[c]['programs'][s] = 10 # TODO: 10 is a dummy number of students. Fix it  
#    
####---------------------------------------------------
        
###---------------------------------------------------

### Adding year groups in CCC couurses
for s in studentsGroup:
    
    y = sIndex[-1]
    yeari = 'year' + y
    #   add each year studnets randomly in two  CCCi course

    CCCi = random.sample(CCC[yeari], 1)
       
    for c in CCCi:
        courseList[c]['programs'][s] = 10 # TODO: 10 is a dummy number of students. Fix it  
    
###---------------------------------------------------


        
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
            
            activityTag = lIndex #'LEC+AnyRoom+'+lIndex
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
                minDays = '2'
                weight = '100'
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
            
            activityTag = lIndex #'TUT+AnyRoom+'+lIndex
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
            
            activityTag = lIndex #'LAB' +'+'+ l['room'][0:4]+'+'+lIndex
            
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
            
# add lunch activity for each subgroup
for sIndex, s in studentsGroup.items():
    for sgIndex, sg in s['subgroups'].items():
        row = sgIndex+',Lunch,'+'T'+sgIndex+', ,8,2+2+2+2,1,100,1\n'
        activityString = activityString+row

            
f = open(activityCsvFileName, "w")
f.write(activityString)
f.close()    

###################################################################    
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
                    spaceCons = spaceCons + '<ConstraintActivityPreferredRoom>\n\
                    <Weight_Percentage>100</Weight_Percentage>\n\
                    <Activity_Id>'+str(i)+'</Activity_Id>\n\
                    <Room>'+roomArray[j]+'</Room>\n\
                    <Permanently_Locked>false</Permanently_Locked>\n\
                    <Active>true</Active>\n\
                    <Comments></Comments>\n\
                    </ConstraintActivityPreferredRoom>'
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

f = open(fetFileName,'w+')
f.write(formattedData)
f.close





dayFile = 'trash.xml'
g = open(dayFile,'w')
g.write("trash")
g.close
