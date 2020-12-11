# Imports
from flask import Flask
from flask_restful import Resource, Api
from tinydb import TinyDB, Query

# Set up server and data storage
app = Flask(__name__)
db = TinyDB('data/db.json')

# Initialize API
api = Api(app)

class root(Resource):
    def get(self):
        return {"message": "BJU COVID API"}

class entry(Resource):
    def get(self, date):
        query = Query()

        result = db.search(query.date == int(date))

        if (len(result) > 0):
            return db.search(query.date == int(date))[0]
        else:
            return {}

api.add_resource(root, '/api/v1/')
api.add_resource(entry, '/api/v1/entries/<string:date>')

if __name__ == '__main__':
    app.run(debug=True)
