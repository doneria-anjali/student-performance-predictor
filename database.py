#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 16:25:20 2018

@author: anjali
"""

from sqlalchemy import create_engine

"""
Before running this, open Anaconda Prompt and run:
conda install -c anaconda sqlalchemy
conda install -c anaconda pymysql
"""

def connect():
    """ Connect to MySQL database after filling out below parameters"""
    engine = create_engine('mysql+pymysql://anjali:spring2018@127.0.0.1:3306/edm?charset=utf8', encoding='utf-8')
    return engine