#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 00:24:16 2019

@author: ajit
"""
## INPUT
#----------------------------------------------------------------------
insList = {
        'ENG240AND342Instructor':{'weight':100, 'numHours':5},
        'J  Venkatramani[20500736]':{'weight':100, 'numHours':8},
        'Sathi Rajesh Reddy[20500731]':{'weight':100, 'numHours':8},
        'Shalini  Rankavat[20501010]':{'weight':100, 'numHours':8},
        'Anirban  Ghosh[20500908]':{'weight':100, 'numHours':5},
        }
#----------------------------------------------------------------------


maxContXMLtemplate = '<ConstraintTeacherMaxHoursContinuously>\n\
	<Weight_Percentage>CONSWEIGHT</Weight_Percentage>\n\
	<Teacher_Name>CONSINSTRUCTOR</Teacher_Name>\n\
	<Maximum_Hours_Continuously>NUMHOURS</Maximum_Hours_Continuously>\n\
	<Active>true</Active>\n\
	<Comments></Comments>\n\
</ConstraintTeacherMaxHoursContinuously>\n'



consList = ''
for i in insList:
    iCons = maxContXMLtemplate
    iCons = iCons.replace('CONSWEIGHT',str(insList[i]['weight']))
    iCons = iCons.replace('CONSINSTRUCTOR', i)
    iCons = iCons.replace('NUMHOURS', str(insList[i]['numHours']))
    
    consList = consList + iCons
    
    
