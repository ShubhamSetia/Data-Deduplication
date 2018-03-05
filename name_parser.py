#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 08:15:16 2018

@author: shubham
"""

import re

_suffixes = ['Jr', 'Sr', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
            'PhD', 'MD', 'DD', 'JD', 'PharmD', 'PsyD', 'RN', 'EngD',
            'DPhil', 'MA', 'MF', 'MBA', 'MSc', 'MEd', 'EdD', 'DMin',
            'AB', 'BA', 'BFA', 'BSc', 'Esq', 'Esquire', 'MP', "MS",
            'USA', 'USAF', 'USMC', 'USCG', 'USN', 'Ret', r'\(Ret\)',
            'CPA', 'Junior', 'Senior']

_prefixes = ['Mr', 'Mister', 'Mrs', 'Ms', 'Miss', 'Dr', 'Doctora?',
             'Professor', 'The', 'Honou?rable', 'Chief', 'Justice',
             'His', 'Her', 'Honou?r', 'Mayor', 'Associate', 'Majesty',
             'Judge', 'Master', 'Sen', 'Senator', 'Rep', 'Deputy',
             'Representative', 'Congress(wo)?man', 'Sir', 'Dame',
             'Speaker', r'(Majority|Minority)\W+Leader',
             'Presidente?', 'Chair(wo)?man', 'Pres', 'Governor',
             'Gov', 'Assembly\W+Member', 'Highness', 'Hon',
             'Prime\W+Minister', r'P\.?M', 'Admiral', 'Adm',
             'Colonel', 'Col', 'General', 'Gen', 'Captain',
             'Capt', 'Corporal', 'CPL', 'PFC', 'Private',
             r'First\W+Class', 'Sergeant', 'Sgt', 'Commissioner',
             'Lieutenant', 'Lt', 'Lieut', 'Brigadier',
             'Major', 'Maj', 'Officer', 'Pilot',
             'Warrant', 'Officer', 'Cadet', 'Reverand',
             'Minister', 'Venerable', 'Father', 'Mother', 'Brother',
             'Sister', 'Rabbi', 'Fleet', 'Sr', 'Sra', 'Srta', 'Alcalde(sa)?',
             'Senadora?', 'Representante', 'Legisladora?', 'Gobernadora?',
             'Comisionado','Residente']

_compound_prefixes = ['vere', 'von', 'van', 'de', 'del', 'della', 'di', 'da',
                      'pietro', 'vanden', 'du', r'st\.', 'st', 'la', 'ter',
                      'bin']

_suffix_pattern = [r"\.?".join(suffix) for suffix in _suffixes]
_suffix_pattern = r'\W*,?(\W+(%s)\.?,?)+\W*$' % r"|".join(_suffix_pattern)
_suffix_pattern = re.compile(_suffix_pattern, re.IGNORECASE)

_prefix_pattern = r'^\W*((%s)\.?(\W+|$))+' % r"|".join(_prefixes)
_prefix_pattern = re.compile(_prefix_pattern, re.IGNORECASE)


_compound_pattern = re.compile(r'\b(%s)\b.+$' % r'|'.join(_compound_prefixes),
                               re.IGNORECASE)

def get_prefix(name):
    name = name.lstrip()
    match = _prefix_pattern.match(name)
    #print(match)
    if match:
        return(match.group(0).strip(),name[match.end():len(name)].lstrip())
        
    return('',name)
    
def drop_prefix(name):
    return(get_prefix(name)[1])
    
def get_suffix(name):
    name = name.rstrip()
    match = _suffix_pattern.search(name)
    
    if match:
        return(name[0:match.start()].rstrip(),match.group().lstrip('., \t\r\n'))
        
    return(name,'')
    
    
def drop_suffix(name):
    return(get_suffix(name)[0])
    
def split(name):
    name_ws,suffixes = get_suffix(name)
    i = name_ws.find(', ')
    
    if i!=-1:
        last_part,first_part = name_ws.split(', ',1)
        last_part,more_suffixes = get_suffix(last_part)
        if more_suffixes:
            if suffixes:
                suffixes +=" "
            suffixes+=more_suffixes
            
        prefixes,first_part=get_prefix(first_part)
        if prefixes and not first_part and ' ' not in prefixes:
            first_part = prefixes
            prefixes = ''
        first_part = first_part.strip()
        last_part = last_part.strip()
        
        if last_part and first_part and get_prefix(last_part)[1]:
            return (prefixes, first_part, last_part, suffixes)
        
    prefixes,name_wa = get_prefix(name_ws)
    match = _compound_pattern.search(name_wa)
    
    if match and match.start()!=0:
        first_part = name_wa[0:match.start()]
        last_part = match.group(0)
    else:
        words = name_wa.split()
        first_part = ' '.join(words[0:-1])
        if not words:
            last_part = ''
        else:
            last_part = words[-1]
    
    first_part = first_part.strip()
    last_part = last_part.strip()
    
    if prefixes and not first_part and ' ' not in prefixes:
        first_part = prefixes
        prefixes = ''
    
    if prefixes and not last_part:
        pre_words = prefixes.split()
        last_part = pre_words[-1]
        prefixes = ' '.join(pre_words[0:-1])

    return(prefixes,first_part,last_part,suffixes)
    
    