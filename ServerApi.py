from flask import Flask
from flask_restful import Resource, Api

class ServerApi:

    def __init__(self, app):
        self.app = app

        self.api = Api(self.app)

        self.api.add_resource(root, '/')

class root(Resource):
    def get(self):
        return {"message": "BJU COVID API"}