import os.path
import csv

path = 'data.db'

check_file = os.path.isfile(path)

 
# opening the CSV file
with open('images_data/data.csv', mode ='r') as file:   
        
       # reading the CSV file
       csvFile = csv.DictReader(file)
 
       # displaying the contents of the CSV file
       for lines in csvFile:
            print(lines)