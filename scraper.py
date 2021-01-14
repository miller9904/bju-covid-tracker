#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
import datetime
import datefinder
from tinydb import TinyDB, Query

db = TinyDB('data/db.json').table('stats', cache_size=0)

document = ""

for line in sys.stdin:
    document += line

soup = BeautifulSoup(document, 'html.parser')

table = soup.table

date = table.parent.p.em.text

studentIsolation = table.find_all('tr')[1].find_all('strong')[0].text
studentHospitalization = table.find_all('tr')[1].find_all('strong')[1].text

facStaffIsolation = table.find_all('tr')[2].find_all('strong')[0].text
facStaffHospitalization = table.find_all('tr')[2].find_all('strong')[1].text

date = list(datefinder.find_dates(date))[0].strftime("%Y%m%d")

entry = {
    'studentIsolation': 0,
    'studentHospitalization': 0,
    'facStaffIsolation': 0,
    'facStaffHospitalization': 0,
    'date': int(date),
    'timestampRetrieved': datetime.datetime.now().timestamp()
}

if studentIsolation.isdigit():
    entry['studentIsolation'] = int(studentIsolation)
elif studentIsolation == '—':
    pass
else:
    print('Invalid number - studentIsolation: ' + studentIsolation)

if studentHospitalization.isdigit():
    entry['studentHospitalization'] = int(studentHospitalization)
elif studentHospitalization == '—':
    pass
else:
    print('Invalid number - studentHospitalization: '+ studentHospitalization)

if facStaffIsolation.isdigit():
    entry['facStaffIsolation'] = int(facStaffIsolation)
elif facStaffIsolation == '—':
    pass
else:
    print('Invalid number - facStaffIsolation: ' + facStaffIsolation)

if facStaffHospitalization.isdigit():
    entry['facStaffHospitalization'] = int(facStaffHospitalization)
elif facStaffHospitalization == '—':
    pass
else:
    print('Invalid number - facStaffHospitalization: ' + facStaffHospitalization)

# Search for records that already exist for the current data by date

query = Query()

if len(db.search(query.date == int(date))) == 0:
    db.insert(entry)
    print(entry)