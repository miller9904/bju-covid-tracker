# Imports
from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
from tinydb import TinyDB, Query
from operator import attrgetter
from datetime import datetime

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

        # Search database for an entry with the correct date
        result = db.search(query.date == int(date))

        # Check to see if there are any results
        if (len(result) > 0):
            # Return the result
            return result[0]
        else:
            # No entries found; return an HTTP error
            abort(404, message="Entry does not exist")

class entries(Resource):
    def get(self):
        query = Query()
        parser = reqparse.RequestParser()

        # Register possible request parameters
        parser.add_argument('sort', type=str, choices=('ascending', 'descending'), help='{error_msg}. Use \'ascending\' or \'descending\'')
        parser.add_argument('begin', type=int, required=True)
        parser.add_argument('end', type=int, required=True)

        # Parse request parameters
        args = parser.parse_args()

        # Helper function for testing date ranges
        def query_test(date, begin, end):
            return int(begin) <= int(date) <= int(end)

        # Run query and return results
        result = db.search(query.date.test(query_test, args['begin'], args['end']))
        
        # https://wiki.python.org/moin/SortingListsOfDictionaries
        sort_on = "date"
        decorated = [(dict_[sort_on], dict_) for dict_ in result]
        decorated.sort(reverse=(args['sort'] == 'descending'))
        result = [dict_ for (key, dict_) in decorated]

        return result

class latest(Resource):
    def get(self):
        # now = datetime.now()
        # date = now.strftime('%Y%m%d')

        # Returns the latest record to be inserted.  This is assumed to be the latest information collected.  This also assumes that records are sequential in time and are never deleted.
        return db.get(doc_id=len(db))



api.add_resource(root, '/api/v1/')
api.add_resource(latest, '/api/v1/latest')
api.add_resource(entries, '/api/v1/entries')
api.add_resource(entry, '/api/v1/entries/<int:date>')

if __name__ == '__main__':
    app.run(debug=True)
