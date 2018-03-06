#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 12:50:43 2018

@author: shubham
"""


import re
from itertools import combinations
import name_parser

def initial_initial(name):
    """
    Input: Name
    Output: First Name in Abbrevated form
    """
    pre,fp,lp,suff = name_parser.split(name)
    
    if fp:
        fp = fp[0]
    return " ".join([p for p in [pre, fp, lp, suff] if p])


def middle_initials(name):
    """
    Input: Name
    Output: Middle Name in Abbrevated form
    """
    parts = name.split(' ')
    name = parts[0]
    
    for part in parts[1:-1]:
        name+=" "+part[0]
    if len(parts)>1:
        name+=" "+parts[-1]
    return name

def last_only(name):
    """
    Input: Name
    Output: Last Name
    """
    return name_parser.split(name)[2]

def first_first(name):
    """
    Input: Name
    Output: First name appears first and last name appears last
    """
    parts = name_parser.split(name)
    return " ".join([p for p in parts if p])

def last_first(name):
    """
    Input: Name
    Output: Last name appears first and first name appears last
    """
    pre, fp, lp, suf = name_parser.split(name)
    if lp:
        lp += ", "
    return lp + " ".join([p for p in [pre, fp, suf] if p])

_funcs = {(lambda s: s.lower()): 0.01,
          (lambda s: s.replace('.', '')): 0.02,
          (lambda s: s.replace(',', '')): 0.02,
          initial_initial: 0.10,
          middle_initials: 0.10,
          name_parser.drop_prefix: 0.05,
          name_parser.drop_suffix: 0.05,
          first_first: 0.02,
          last_first: 0.02,
          last_only: 0.20}

_combinations = []
for n in range(0, len(_funcs)):
    _combinations.extend(combinations(_funcs.items(), n))
    

def similarity(name1,name2):
    """
    Input: two strings name1 and name2
    Output: a floating point number between 0.0 and 1.0 which is the similarity score
    """
    
    # If name are same return 1
    if name1==name2:
        return 1.0

    # If either of name is empty string
    if not name1.strip() or not name2.strip():
        return 0.0
    
    # Remove multiple spaces i.e reduces spaces to 1 example: "abc  def" => "abc def"
    name1 = re.sub('  +', ' ', name1)
    name1 = re.sub('  +', ' ', name1)

    s1 = set()
    s2 = set()

    for combo in _combinations:
        n1,n2 = name1,name2
        penalty = 0.0
        for (func,mod) in combo:
            n1 = func(n1)
            n2 = func(n2)
            penalty+=mod
        s1.add((n1,penalty))
        s2.add((n2,penalty))
        
    max = 0.0
    
    for p1 in s1:
        for p2 in s2:
            if p1[0]==p2[0]:
                score = 1.0 - p1[1] - p2[1]
                if score > max:
                    max = score
    
    return max

