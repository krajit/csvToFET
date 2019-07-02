#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 03:50:06 2019

@author: ajit
"""
import pickle
coursesPickle = open('courses.pickle','rb')
courses = pickle.load(coursesPickle) 

twoOverlappingTemplate = "<ConstraintActivitiesSameStartingTime> \n\
	<Weight_Percentage>100</Weight_Percentage> \n\
	<Number_of_Activities>2</Number_of_Activities> \n \
	<Activity_Id>item1</Activity_Id> \n\
	<Activity_Id>item2</Activity_Id>\n\
	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintActivitiesSameStartingTime>\n"



x1 =  "<ConstraintActivitiesSameStartingTime> \n\
	<Weight_Percentage>100</Weight_Percentage>\n"
x2 =  "<ConstraintActivitiesSameStartingTime> \n\
	<Weight_Percentage>100</Weight_Percentage>\n"
    
    
overlLappingActIds = []
for c in courses:
    if courses[c]['CourseType'] != 'CCC':
        continue
    if c == 'CCC510':
        continue
    lids = list(courses[c]['lecSections']['LEC1']['ids'])
    overlLappingActIds.append(lids)


x1 = x1 + '\t<Number_of_Activities>'+str(len(overlLappingActIds))+'</Number_of_Activities>\n'
x2 = x2 + '\t<Number_of_Activities>'+str(len(overlLappingActIds))+'</Number_of_Activities>\n'
    
for c in overlLappingActIds:
    x1 = x1 + '\t<Activity_Id>'+str(c[0])+'</Activity_Id>\n'
    x2 = x2 + '\t<Activity_Id>'+str(c[1])+'</Activity_Id>\n'


x1 = x1 + 	'\t<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintActivitiesSameStartingTime>\n'

x2 = x2 + 	'\t<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintActivitiesSameStartingTime>\n'
x = x1+x2


def overlapXML(c1,c2):    
    # make sure these two courses are overlappable
    lids1 = []
    lids2 = []
    tids1 = []
    tids2 = []
    pids1 = []
    pids2 = []
        
    if 'lecSections' in courses[c1]:
        lids1 = list(courses[c1]['lecSections']['LEC1']['ids'])
    if 'lecSections' in courses[c2]:
        lids2 = list(courses[c2]['lecSections']['LEC1']['ids'])
    if 'tutSections' in courses[c1]:
        tids1 = list(courses[c1]['tutSections']['TUT1']['ids'])
    if 'tutSections' in courses[c2]:
        tids2 = list(courses[c2]['tutSections']['TUT1']['ids'])
    if 'labSections' in courses[c1]:
        pids1 = list(courses[c1]['labSections']['PRAC1']['ids'])
    if 'labSections' in courses[c2]:
        pids2 = list(courses[c2]['labSections']['PRAC1']['ids'])
        
    if (len(lids1) != len(lids2)) or (len(tids1) != len(tids2)) or (len(tids1) != len(tids2)):
        print("can't overlap", c1, ' and ', c2)
        print(lids1,lids2, tids1,tids2,pids1,pids2)
        return ''
    
    out = ''
    
    for j in range(len(lids1)):
        outj = twoOverlappingTemplate
        outj = outj.replace('item1',str(lids1[j]))
        outj = outj.replace('item2',str(lids2[j]))
        out = out+outj
        
    for j in range(len(tids1)):
        outj = twoOverlappingTemplate
        outj = outj.replace('item1',str(tids1[j]))
        outj = outj.replace('item2',str(tids2[j]))
        out = out+outj
        
        
    for j in range(len(pids1)):
        outj = twoOverlappingTemplate
        outj = outj.replace('item1',str(pids1[j]))
        outj = outj.replace('item2',str(pids2[j]))
        out = out+outj
        
    return out

MAT494_overlaps_CSD310 = overlapXML('CSD310','MAT494')
MAT440overlapsMAT424 = overlapXML('MAT440', 'MAT424')
MAT494overlapsMAT399 = overlapXML('MAT494', 'MAT399')    
    




