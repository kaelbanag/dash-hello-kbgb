#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:39:43 2022

@author: kaleb
"""

import sqlite3

conn = sqlite3.connect('scenarios.sqlite') 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS scenarios
          (scenario_name VarChar NOT NULL,
           total_hits Int,
           conversion_rate Int,
           revenue_per_purchase Int,
           ntpcuy Int,
           total_sampling_cost Int,
           potential_revenue Int,
           PRIMARY KEY (scenario_name))
          ''')
                     
conn.commit()
#%%
import sqlite3

conn = sqlite3.connect('scenarios.sqlite') 
c = conn.cursor()

c.execute('''
          INSERT INTO scenarios
          (scenario_name, total_hits, conversion_rate, revenue_per_purchase, ntpcuy, total_sampling_cost, potential_revenue) 
          VALUES('Test1', 1000000, 60, 50, 2, 25000000, 50)
          ''')
                     
conn.commit()