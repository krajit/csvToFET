#!/usr/bin/env python3
# -*- coding: utf-8 -*-
studentsGroup = {
        'year1': {'BIO1', 'BMS1', 'CED1', 'CHD1', 'CHY1', 'CSE1', 'ECE1', 'ECO1', 
                  'EEE1', 'ENG1', 'HIS1', 'INT1', 'MAT1', 'MED1', 'PHY1', 'SOC1'},
        'year2': {'BIO2', 'BMS2', 'CED2', 'CHD2', 'CHY2', 'CSE2', 'ECE2', 'ECO2', 
                  'EEE2', 'ENG2', 'HIS2', 'INT2', 'MAT2', 'MED2', 'PHY2', 'SOC2'},
        'year3': {'BIO3', 'BMS3', 'CED3', 'CHD3', 'CHY3', 'CSE3', 'ECE3', 'ECO3', 
                  'EEE3', 'ENG3', 'HIS3', 'INT3', 'MAT3', 'MED3', 'PHY3', 'SOC3'},
        'year4': {'BIO4', 'BMS4', 'CED4', 'CHD4', 'CHY4', 'CSE4', 'ECE4', 'ECO4', 
                  'EEE4', 'ENG4', 'HIS4', 'INT4', 'MAT4', 'MED4', 'PHY4', 'SOC4'}}

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