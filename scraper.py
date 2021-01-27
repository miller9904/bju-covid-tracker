#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
import datetime
import datefinder
from tinydb import TinyDB, Query
import logging
import smtplib

smtpconfig = {
    'server': '',
    'port': 587,
    'username': '',
    'password': '',
    'sender': '',
    'recipient': ['']
}

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s", datefmt='%Y-%m-%d %I:%M:%S %p')

db = TinyDB('data/db.json').table('stats', cache_size=0)

document = ""

for line in sys.stdin:
    document += line

soup = BeautifulSoup(document, 'html.parser')

logging.debug('Finished loading document')

try:
    table = soup.table

    date = table.parent.p.em.text

    studentIsolation = table.find_all('tr')[1].find_all('strong')[0].text
    studentHospitalization = table.find_all('tr')[1].find_all('strong')[1].text

    facStaffIsolation = table.find_all('tr')[2].find_all('strong')[0].text
    facStaffHospitalization = table.find_all('tr')[2].find_all('strong')[1].text

    date = list(datefinder.find_dates(date))[0].strftime("%Y%m%d")
except:
    logging.error('Could not parse document - may be inaccessible or structure may have changed')
    sys.exit()

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
    logging.error('Invalid number - studentIsolation: ' + studentIsolation)
    sys.exit()

if studentHospitalization.isdigit():
    entry['studentHospitalization'] = int(studentHospitalization)
elif studentHospitalization == '—':
    pass
else:
    logging.error('Invalid number - studentHospitalization: '+ studentHospitalization)
    sys.exit()

if facStaffIsolation.isdigit():
    entry['facStaffIsolation'] = int(facStaffIsolation)
elif facStaffIsolation == '—':
    pass
else:
    logging.error('Invalid number - facStaffIsolation: ' + facStaffIsolation)
    sys.exit()

if facStaffHospitalization.isdigit():
    entry['facStaffHospitalization'] = int(facStaffHospitalization)
elif facStaffHospitalization == '—':
    pass
else:
    logging.error('Invalid number - facStaffHospitalization: ' + facStaffHospitalization)
    sys.exit()

# Search for records that already exist for the current data by date

query = Query()

if len(db.search(query.date == int(date))) == 0:
    db.insert(entry)
    logging.info('Updated to ' + date)

    message = """From: BJU COVID Dashboard <""" + smtpconfig['sender'] + """>
To: <""" + smtpconfig['recipient'][0] + """>
MIME-Version: 1.0
Content-type: text/html
Subject: Data Updated

<h2>BJU COVID Dashboard</h2>

<div>""" + str(entry['studentIsolation'] + entry['facStaffIsolation']) + """ Active cases - """ + str(entry['studentIsolation']) + """ students, """ + str(entry['facStaffIsolation']) + """ faculty / staff</div>

<div>""" + str(entry['studentHospitalization'] + entry['facStaffHospitalization']) + """ hospitalizations - """ + str(entry['studentHospitalization']) + """ students, """ + str(entry['facStaffHospitalization']) + """ faculty / staff</div>
"""

    try:
        logging.debug(message)
        logging.debug(smtpconfig['sender'])

        s = smtplib.SMTP(smtpconfig['server'], smtpconfig['port'])
        s.starttls()
        s.login(smtpconfig['username'], smtpconfig['password'])
        s.sendmail(smtpconfig['sender'], smtpconfig['recipient'], message)
        s.quit()

        logging.info('Email sent successfully')
    except Exception as e:
        logging.error('Unable to send email: ' + str(e))
else:
    logging.info("Up to date - " + date)