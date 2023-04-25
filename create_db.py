import os.path
import csv
import sqlite3
import uuid
import random

db_path = 'data.db'

con2 = sqlite3.connect(db_path)
cur2 = con2.cursor()

s=cur2.execute('''
CREATE TABLE IF NOT EXISTS Images
( imgId int NOT NULL PRIMARY KEY, filepath varchar(64), fake_or_real varchar(64), emotion int);''')
print(s)

cur2.execute('''CREATE TABLE IF NOT EXISTS  user_evaluation( sno INTEGER PRIMARY KEY AUTOINCREMENT,uid varchar(64),imgId int,fake_or_real int,emotion int);
''')

cur2.execute('''
CREATE TABLE IF NOT EXISTS user(uid varchar(64) NOT NULL PRIMARY KEY,email varchar(64),name varchar(64), random_counter int, total_count int,total_skip int, total_pos int, total_real int);
''')


 
# opening the CSV file
with open('image_data/data.csv', mode ='r') as file:   
        
    csvFile = csv.DictReader(file)
    count=1
    for lines in csvFile:
        
        #change these according to csv
        emotion=len(str(lines['emotion']))%2
        type=len(lines['type'])%2
        
        generator=random.randint(0, 1) 
        
        q='''INSERT INTO Images(imgId,filepath,fake_or_real,emotion) 
        VALUES({},'{}','{}','{}');
        '''.format(count,lines['filename'],
                   ['fake','real'][random.randint(0, 1)],
                   random.randint(0, 1))
        con2.execute(q)
        count+=1

con2.commit()
print(count)
print('database generated')
con2.close()