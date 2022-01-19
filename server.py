# Imports
from flask import Flask, render_template
from flask_restful import Resource, Api, abort, reqparse
from tinydb import TinyDB, Query
from datetime import datetime

# Set up server and data storage
app = Flask(__name__)
db = TinyDB('data/db.json').table('stats', cache_size=0)

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

        # Read all records in database, sort them, and return the latest
        results = db.all()

        # https://wiki.python.org/moin/SortingListsOfDictionaries
        sort_on = "date"
        decorated = [(dict_[sort_on], dict_) for dict_ in results]
        decorated.sort(reverse=True)
        result = [dict_ for (key, dict_) in decorated][0]

        return result

class all(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        # Register possible request parameters
        parser.add_argument('sort', type=str, choices=('ascending', 'descending'), help='{error_msg}. Use \'ascending\' or \'descending\'')

        # Parse request parameters
        args = parser.parse_args()
        # Read all records in database and sort them
        results = db.all()

        # https://wiki.python.org/moin/SortingListsOfDictionaries
        sort_on = "date"
        decorated = [(dict_[sort_on], dict_) for dict_ in results]
        decorated.sort(reverse=(args['sort'] == 'descending'))
        return [dict_ for (key, dict_) in decorated]



api.add_resource(root, '/api/v1/')
api.add_resource(latest, '/api/v1/latest')
api.add_resource(entries, '/api/v1/entries')
api.add_resource(all, '/api/v1/entries/all')
api.add_resource(entry, '/api/v1/entries/<int:date>')

@app.route('/')
def index():
    results = db.all()

    # https://wiki.python.org/moin/SortingListsOfDictionaries
    sort_on = "date"
    decorated = [(dict_[sort_on], dict_) for dict_ in results]
    decorated.sort(reverse=True)
    result = [dict_ for (key, dict_) in decorated][0]

    # format for title
    date = datetime.strptime(str(result['date']), '%Y%m%d')
    date = datetime.strftime(date, '%A, %B %d, %Y')

    # data for dashboard
    isolations = result['studentIsolation'] + result['facStaffIsolation']
    sI = result['studentIsolation']
    fI = result['facStaffIsolation']

    hospitalizations = result['studentHospitalization'] + result['facStaffHospitalization']
    sH = result['studentHospitalization']
    fH = result['facStaffHospitalization']

    # Isolation rate with estimated campus population of 3000
    occurrence = 3000

    if isolations != 0:
        occurrence = round(3000 / isolations)

    return render_template('index.html.jinja', date=date, 
    isolations=isolations,
    hospitalizations=hospitalizations,
    occurrence=occurrence,
    sI=sI,
    sIG=("" if sI == 1 else "s"),
    fI=fI,
    sH=sH,
    sHG=("" if sH == 1 else "s"),
    fH=fH)

@app.route('/privacy/')
def privacy():
    return render_template('privacy.html.jinja')

@app.route('/api/')
def apiPage():
    return render_template('api.html.jinja')

if __name__ == '__main__':
    app.run(debug=True)
