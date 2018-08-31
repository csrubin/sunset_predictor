#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 20:40:39 2018

@author: csrubin
"""

import sqlite3

path = '/Users/csrubin/Documents/Python/sunset_predictor/database.db'

def create_table(table_name):
    '''Create a new table within existing behavior tracker database. Arguments
    include a string for the table name, a list of column names, and list of
    corresponding SQL data types.'''
    
    columns = []
    data_types = []
    while True:
        col = input('Column Name: ')
        typ = input('Column Type: ')
        if col == '':
            break
        else:
            columns.append(col)
            data_types.append(typ)
         
    db = sqlite3.connect() # Use config file later
    c = db.cursor()
    args = []   #Empty list to build string 
    
    # Build a string with list of column names and list of corresponding data 
    # types to pass to CREATE TABLE 
    for i in range(len(columns)):
        args.append(columns[i]+' '+data_types[i])
    arg = ', '.join(args)
    
    #Execute SQL command to create new table in defined database; Save changes
    c.execute('CREATE TABLE %s(id INTEGER PRIMARY KEY, %s )' % (table_name, arg))
    db.commit()
    db.close()
    

