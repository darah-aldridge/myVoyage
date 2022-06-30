import imp, re
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from datetime import time 

db ="myvoyage"

class Activity:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.activity_description = data['activity_description'] 
        self.activity_start_date = data['activity_start'].strftime("%Y-%m-%dT%H:%M")
        self.start_date_mmdd = data['activity_start'].strftime("%m/%d")
        self.activity_start_time = data['activity_start'].strftime("%I:%M%p")
        self.address_location = data['address_location'] 
    @staticmethod
    def validate_activity(form_data):
        is_valid = True
        if len(form_data['activity_name']) < 3:
            flash(u"Trip name must be at least 3 characters.", 'activity error')
            is_valid = False
        if not form_data['activity_name']:
            flash(u"You must include a trip name.", 'activity error')
            is_valid = False
        if len(form_data['description']) < 3:
            flash(u"Description must be at least 3 characters.", 'activity error')
            is_valid = False
        if not form_data['description']:
            flash(u"You must include a description.", 'activity error')
            is_valid = False
        if not form_data['address']:
            flash(u"You must include a address/location.", 'activity error')
            is_valid = False
        if len(form_data['address']) < 3:
            flash(u"Address/Location must be at least 3 characters.", 'activity error')
            is_valid = False
        if not form_data['activity_type']:
            flash(u"You must choose an activity type.", 'activity error')
            is_valid = False
        if not form_data['activity_start']:
            flash(u"You must include a start date.", 'activity error')
            is_valid = False
        return is_valid
    @staticmethod
    def validate_update_activty(form_data):
        is_valid = True
        if len(form_data['activity_name']) < 3:
            flash(u"Trip name must be at least 3 characters.", 'activity error')
            is_valid = False
        if not form_data['activity_name']:
            flash(u"You must include a trip name.", 'activity error')
            is_valid = False
        if len(form_data['description']) < 3:
            flash(u"Description must be at least 3 characters.", 'activity error')
            is_valid = False
        if not form_data['description']:
            flash(u"You must include a description.", 'activity error')
            is_valid = False
        if not form_data['address']:
            flash(u"You must include a address/location.", 'activity error')
            is_valid = False
        if len(form_data['address']) < 3:
            flash(u"Address/Location must be at least 3 characters.", 'activity error')
            is_valid = False
        if not form_data['activity_type']:
            flash(u"You must choose an activity type.", 'activity error')
            is_valid = False
        if not form_data['activity_start']:
            flash(u"You must include a start date.", 'activity error')
            is_valid = False
        return is_valid
    @classmethod
    def saveActivity(cls, data):
        query = f"INSERT INTO activities (name, type, activity_start, address_location, activity_description, trip_id) VALUES (%(name)s, %(type)s, %(activity_start)s, %(address_location)s, %(activity_description)s, %(trip_id)s);"
        return connectToMySQL(db).query_db( query, data )  
    
    @classmethod
    def updateActivity(cls, data, id):
        query  = f"UPDATE activities SET name = %(name)s, type = %(type)s, activity_start = %(activity_start)s, address_location =%(address_location)s activity_description =%(activity_description)s  WHERE id = {id};"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_activity(cls, id):
        query  = f"SELECT * FROM activities WHERE id = {id};"
        result = connectToMySQL(db).query_db(query)
        return cls(result[0])
