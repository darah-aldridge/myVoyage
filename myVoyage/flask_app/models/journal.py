import imp, re
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app


db ="myvoyage"

class Journal:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']  