#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:02:08 2019

@author: ajit
"""
import xlrd, random

import readCOSdata as COSdata
UWEs = COSdata.UWEs

wb = xlrd.open_workbook('studentDatabase/studentDatabase.xlsx') 
sheet = wb.sheet_by_index(0) # get first sheet
rollCol = 0; netIdCol = 1; nameCol = 2; groupCol = 3
students = dict()
for i in range(1,sheet.nrows):
    sRoll = str(int(sheet.cell_value(i,rollCol)))
    sNetId = sheet.cell_value(i,netIdCol)
    sName = sheet.cell_value(i,nameCol)
    sGroup = sheet.cell_value(i,groupCol)    
    students[sNetId] = {'name': sName, 'roll': sRoll, 'group': sGroup, 'email': sNetId+'@snu.edu.in'}
    
#create students group
studentsGroup = dict()
for si in students:
    s = students[si]
    sG = s['group']
    if sG in studentsGroup:
        studentsGroup[sG].add(si)
    else:
        studentsGroup[sG] = set()
        studentsGroup[sG].add(si)
        
studentsListXML = '<Students_List>\n'
for si in studentsGroup:
    studentsListXML = studentsListXML + '<Year>\n' 
    studentsListXML = studentsListXML + '\t<Name>'+si+'</Name>\n'
    studentsListXML = studentsListXML + '\t<Number_of_Students>'+str(len(studentsGroup[si]))+'</Number_of_Students>\n'
    studentsListXML = studentsListXML + '\t<Comments></Comments>\n' 
    
    for gr in studentsGroup[si]:
        studentsListXML = studentsListXML + '\t<Group>\n'
        studentsListXML = studentsListXML + '\t\t<Name>'+gr+'</Name>\n'
        studentsListXML = studentsListXML + '\t\t<Number_of_Students>1</Number_of_Students>\n'
        studentsListXML = studentsListXML + '\t\t<Comments></Comments>\n'
        studentsListXML = studentsListXML + '\t</Group>\n'
    studentsListXML = studentsListXML + '</Year>\n'
studentsListXML = studentsListXML + '</Students_List>\n'

        
# inflate student dictionary with the choices they have made in the course survey form
wb = xlrd.open_workbook('studentDatabase/SNU - Pre Registration for Monsoon 2019 (Responses).xlsx') 
sheet = wb.sheet_by_index(0)
idCol = 1; minorCol = 5
me1col = 6; me2col = 7; me3col = 8
uwe1col = 9; uwe2col = 10; uwe3col = 11


studentWhoSelectedMajorElectivesOutsideTheirMajor = set()
studentWhoSelectedNonElectivesForTheirMajor = set()
studentWhoSelectedUWEsFromTheirDept = set()
studentWhoSelectedNonUWEasUWE = set()



majorPool = dict()
majorPool['EEE'] = {'EED', 'ECE'}
majorPool['ENG'] = {'ENG'}
majorPool['CSE'] = {'CSD'}
majorPool['INT'] = {'INT'}
majorPool['HIS'] = {'HIS', 'ARC'}
majorPool['ECE'] = {'EED', 'ECE', 'EEE'}
majorPool['MED'] = {'MED'}
majorPool['ECO'] = {'ECO'}
majorPool['CED'] = {'CED'}
majorPool['MAT'] = {'MAT'}
majorPool['BMS'] = {'FAC', 'MGT', 'OHM', 'MKT', 'DOM'}
majorPool['PHY'] = {'PHY'}
majorPool['SOC'] = {'SOC'}
majorPool['CHD'] = {'CHD'}
majorPool['BIO'] = {'BIO'}
majorPool['CHY'] = {'CHY'}


studentWhoHaveNotFilledTheFormYet = set()
for s in students:
    studentWhoHaveNotFilledTheFormYet.add(s+'@snu.edu.in')



for i in range(1,sheet.nrows):
    studentEmail = sheet.cell_value(i,idCol)
    
    # replace some weird email ids by students
    if studentEmail == 'inferno@snu.edu.in':
        studentEmail = 'kd184@snu.edu.in'
        
    if studentEmail == 'sae.snu@snu.edu.in':
        studentEmail = 'sk652@snu.edu.in'
    
    studentId = studentEmail[0:5]
    
    studentWhoHaveNotFilledTheFormYet.remove(studentEmail)
    
    # make sure this student is there in the database
    if studentId not in students:
        print(studentEmail, 'Not found in the student database')
        # skip this student
        continue
    
    # get group of this student
    sGroup = students[studentId]['group']
    sMajor = sGroup[0:3]
    
    # get list of major electives / only from non-empty or non -None cells
    studentIdMajorElectives = []    
    for j in range(3):
        if (sheet.cell_type(i,me1col+j) != xlrd.XL_CELL_EMPTY):
            cellVal = sheet.cell_value(i,me1col+j)
            if 'None' not in cellVal:
                if (cellVal[0:3] not in majorPool[sMajor]):
                    studentWhoSelectedMajorElectivesOutsideTheirMajor.add(studentEmail)
                else:
                    if 'Major Elective' not in cellVal:
                        studentWhoSelectedNonElectivesForTheirMajor.add(studentEmail)
                    else:
                        studentIdMajorElectives.append(cellVal[0:6])
                        
    students[studentId]['majorElectivesPreferences'] = studentIdMajorElectives

    studentIdUWEs = []
    # uncomment to add UWEs
#    for j in range(3):
#        if (sheet.cell_type(i,uwe1col+j) != xlrd.XL_CELL_EMPTY):
#            cellVal = sheet.cell_value(i,uwe1col+j)
#            if 'None' not in cellVal:
#                if (cellVal[0:3] in majorPool[sMajor]):
#                    studentWhoSelectedUWEsFromTheirDept.add(studentEmail)
#                else:
#                    if 'Not a UWE' in cellVal:
#                        studentWhoSelectedNonUWEasUWE.add(studentEmail)
#                    else:
#                        studentIdUWEs.append(cellVal[0:6])
#                          
                        
    students[studentId]['UWEpreferences'] = studentIdUWEs
                    
print('About', round(len(studentWhoSelectedMajorElectivesOutsideTheirMajor)*100/sheet.nrows),'% of students selected major electives outside their majors.\n')            
print('About', round(len(studentWhoSelectedNonElectivesForTheirMajor)*100/sheet.nrows),'% of students selected major electives  those courses which are nor marked as major electives.\n')
print('About', round(len(studentWhoSelectedUWEsFromTheirDept)*100/sheet.nrows),'% of students selected UWEs from their departments.\n')
print('About', round(len(studentWhoSelectedNonUWEasUWE)*100/sheet.nrows),'% of students selected a non UWE as their UWE course.\n')
print('About', round(len(studentWhoHaveNotFilledTheFormYet)*100/len(students)),'% have NOT filled the form yet.')            
    
    
# removing over added courses
print('\n\nRemoving electives from students who have shown interest in more courses than they have to.......\n\n')
import readElectivesInfo as ei
numElectives = ei.electives
# convert year to semester
sem2year = {'1':'1', '2':'1', '3':'2', '4':'2', '5':'3', '6':'3', '7':'4', '8':'4'}

# year to sem (for monsoon)
year2Sem = {'1':'1', '2':'3', '3':'5', '4':'7'}

for sId in students:
    s = students[sId]
    sGroup = s['group']
    y = sGroup[-1]
    sMajor = sGroup[0:-1]
    sem = 'Sem'+year2Sem[y]
    numMajorElectives = numElectives[sMajor]['numMajorElectives'][sem] # required num, only this much to accomodated in timetable
    numUWE = numElectives[sMajor]['numUWE'][sem]                       # required num, only this much to accomodated in timetable
       
    if 'majorElectivesPreferences' in s:
        if (len(s['majorElectivesPreferences'])>numMajorElectives):
            s['majorElectivesPreferences'][numMajorElectives:] = []    # remove overly added items
                        
#    if 'UWEpreferences' in s:
#        if (len(s['UWEpreferences'])>numUWE):
#            s['UWEpreferences'][numUWE:] = []    # remove overly added items
           
    # ignore the UWE  chosen by students because they are just too random
    # add UWE from UWE pool for that students
    
    sUWEpoolSet = set()
    sd = numElectives[sMajor]['UWEpool'][0:2]
    for sdi in sd:
        sdiy = sdi+y
        sdiym1 = sdi+str(int(y)-1)
        if sdiy in UWEs:
            sUWEpoolSet = sUWEpoolSet.union(UWEs[sdiy])
            
        if sdiym1 in UWEs:
            sUWEpoolSet = sUWEpoolSet.union(UWEs[sdiym1])
            
    if (numUWE > len(sUWEpoolSet)):
        print(sMajor, 'problem', numUWE, sUWEpoolSet)
    s['UWEpreferences'] = list(random.sample(sUWEpoolSet,numUWE))
    
courses = dict()

# fill students in classes        
for sId in students:
    s = students[sId]
    sGroup = s['group']
    
    if 'majorElectivesPreferences' in s:
        for c in s['majorElectivesPreferences']:
            if c not in courses:
                courses[c] = dict()
                courses[c][sGroup] = set()
                courses[c][sGroup].add(sId)
            elif sGroup not in courses[c]:
                courses[c][sGroup] = set()
                courses[c][sGroup].add(sId)
            else:
                courses[c][sGroup].add(sId)
    

    if 'UWEpreferences' in s:
        for c in s['UWEpreferences']:
            if c not in courses:
                courses[c] = dict()
                courses[c][sGroup] = set()
                courses[c][sGroup].add(sId)
            elif sGroup not in courses[c]:
                courses[c][sGroup] = set()
                courses[c][sGroup].add(sId)
            else:
                courses[c][sGroup].add(sId)
    
    
# record popular choices
# import xlsxwriter module 
import xlsxwriter 
row = 0
workbook = xlsxwriter.Workbook('courseAudience.xlsx') 
worksheet = workbook.add_worksheet()
for ci in courses:
    column = 0
    cStudents =courses[ci]
    worksheet.write(row, column, ci)
    for sg in cStudents:
       column = column + 1 
       worksheet.write(row, column, sg+'('+str(len(cStudents[sg]))+')')
    row = row+1
workbook.close() 
    
    
# create a table shwoing where each group is taking its courses
groupCourses = dict()
for c in courses:
    courseStudents = courses[c]
    for sg in courseStudents:
        sgStudents = courseStudents[sg]
        
        if sg not in groupCourses:
           groupCourses[sg] = dict()
           groupCourses[sg][c] = sgStudents
        else:
           groupCourses[sg][c] = sgStudents
    
# write groupCourses info in an excel
row = 0
workbook = xlsxwriter.Workbook('groupPreferences.xlsx') 
worksheet = workbook.add_worksheet()
for group in groupCourses:
    column = 0
    worksheet.write(row, column, group)
    for c in groupCourses[group]:
        column = column+1
        worksheet.write(row, column, c + '('+str(len(groupCourses[group][c]))+')')
        
    row = row + 1
workbook.close() 

    

    
    