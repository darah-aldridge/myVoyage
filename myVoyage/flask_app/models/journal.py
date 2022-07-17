import imp, re
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app


db ="myvoyage"

class Journal:
    def __init__( self , data ):
        self.id = data['id']
        self.activity_picture = data['picture']
        self.entry = data['entry']  
        self.activity_id = data['activity_id'] 

    @staticmethod
    def validate_entry(form_data):
        is_valid = True
        if len(form_data['entry']) < 3:
            flash(u"Entry name must be at least 3 characters.", 'entry error')
            is_valid = False
        if not form_data['entry']:
            flash(u"You must include a entry.", 'entry error')
            is_valid = False
        if not form_data['activity']:
            flash(u"You must choose an activity.", 'entry error')
            is_valid = False
        return is_valid
    @staticmethod
    def validate_update_entry(form_data):
        is_valid = True
        if len(form_data['entry']) < 3:
            flash(u"Entry name must be at least 3 characters.", 'entry error')
            is_valid = False
        if not form_data['entry']:
            flash(u"You must include a entry.", 'entry error')
            is_valid = False
        return is_valid
    @classmethod
    def saveJournal(cls, data):
        query = f"INSERT INTO journal_entries (picture, entry, activity_id) VALUES (%(picture)s, %(entry)s, %(activity_id)s);"
        return connectToMySQL(db).query_db( query, data )  
    
    @classmethod
    def updateJournal(cls, data, id):
        query  = f"UPDATE journal_entries SET picture = %(picture)s, entry = %(entry)s, activity_id = %(activity_id)s  WHERE id = {id};"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_entry(cls, id):
        query  = f"SELECT * FROM journal_entries WHERE id = {id};"
        result = connectToMySQL(db).query_db(query)
        return cls(result[0])

