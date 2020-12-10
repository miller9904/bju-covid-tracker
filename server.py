# Imports
from flask import Flask
from ServerApi import ServerApi
app = Flask(__name__)

api = ServerApi(app)

if __name__ == '__main__':
    app.run(debug=True)