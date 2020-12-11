from tinydb import TinyDB, Query
import pandas as pd

db = TinyDB('db.json')

csv = pd.read_csv('data.csv', header=0)

for date, sIso, sHos, fIso, fHos, ts in csv.itertuples(index=False):
    db.insert({'date': date, 
    'studentIsolation': sIso,
    'studentHospitalization': sHos,
    'facStaffIsolation': fIso,
    'facStaffHospitalization': fHos,
    'timestampRetrieved': ts
    })