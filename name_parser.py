#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 08:15:16 2018

@author: shubham
"""

import re

# List of suffixes, prefixes and compound prefixes used to match pattern 
with open("prefixes.txt", 'r') as f:
    _prefixes = [line.rstrip('\n') for line in f]

with open("suffixes.txt", 'r') as f:
    _suffixes = [line.rstrip('\n') for line in f]

with open("compound_prefixes.txt", 'r') as f:
  _compound_prefixes = [line.rstrip('\n') for line in f]

_suffix_pattern = [r"\.?".join(suffix) for suffix in _suffixes]
_suffix_pattern = r'\W*,?(\W+(%s)\.?,?)+\W*$' % r"|".join(_suffix_pattern)
_suffix_pattern = re.compile(_suffix_pattern, re.IGNORECASE)

_prefix_pattern = r'^\W*((%s)\.?(\W+|$))+' % r"|".join(_prefixes)
_prefix_pattern = re.compile(_prefix_pattern, re.IGNORECASE)


_compound_pattern = re.compile(r'\b(%s)\b.+$' % r'|'.join(_compound_prefixes),
                               re.IGNORECASE)

def get_prefix(name):
    """
    Input: Name 
    Output: Prefix,Name without prefix
    Check if pattern any prefix from the list of prefixes is available or not
    """
    name = name.lstrip()
    match = _prefix_pattern.match(name)
    
    # If prefix is present separate prefix and rest of the name
    if match:
        return(match.group(0).strip(),name[match.end():len(name)].lstrip())
        
    return('',name)
    
def drop_prefix(name):
    """
    Input: Name
    Output: Name without prefix
    """
    return(get_prefix(name)[1])
    
def get_suffix(name):
    """
    Input: Name 
    Output: Name without suffix,Suffix
    Search if any of the suffix pattern from the list of suffixes is present or not
    """
    name = name.rstrip()
    match = _suffix_pattern.search(name)
    
    # If suffix is present separate suffix and rest of the name
    if match:
        return(name[0:match.start()].rstrip(),match.group().lstrip('., \t\r\n'))
        
    return(name,'')
    
    
def drop_suffix(name):
    """
    Input: Name
    Output: Name without suffix
    """
    return(get_suffix(name)[0])
    
def split(name):
    """
    Splits a string containing a name into a tuple of 4 strings,
    (prefixes, first_part, last_part, suffixes), any of which may be empty
    if the name does not include a corresponding part.

      * prefixes is the part of the name consisting of titles that precede
        a name in typical speech ('Mr.', 'Dr.', 'President')
      * first_part corresponds to included given name(s), first initial(s),
        middle name(s) and/or middle initial(s) (e.g. 'Fred', 'F. Scott',
        'Barack Hussein')
      * last_part corresponds to a last name (e.g. 'Smith', 'van Dyke')
      * suffixes corresponds to generational suffixes ('Jr.', 'III', etc.),
        academic suffixes ('Ph.D.', 'M.A.', etc.) and other titles that
        typically follow a name
    """
    name_ws,suffixes = get_suffix(name)
    i = name_ws.find(', ')
    
    # If last name separted by comma
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

        # We check that first and last are not empty, and that
        # last is not just prefixes (in which case we probably
        # misinterpreted a prefix with a comma for a last name),
        # skipping on to the other name splitting algorithm
        # if true.
        if last_part and first_part and get_prefix(last_part)[1]:
            return (prefixes, first_part, last_part, suffixes)
        

    # Look for compound last name
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

    # Sometimes a last name looks like a prefix. If we found
    # prefixes but no last name, the last prefix is probably
    # actually the last name
    if prefixes and not last_part:
        pre_words = prefixes.split()
        last_part = pre_words[-1]
        prefixes = ' '.join(pre_words[0:-1])

    return(prefixes,first_part,last_part,suffixes)
    
    