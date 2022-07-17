import imp, re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_app.models.activity import Activity
from flask_app.models.journal import Journal
import pprint

from datetime import datetime


db ="myvoyage"

class Trip:
    def __init__( self , data ):
        self.id = data['id']
        self.trip_name = data['trip_name']
        self.description = data['description']  
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.destinations = data['destinations'] 
        self.activity_list = []
        self.all_past_trips = []
        self.user_trip = []
        self.trip_activity = None
        self.one_trip_activity_list = []
        self.journal_activity = []
        self.journal_entry = []
    @staticmethod
    def validate_trip(form_data):
        is_valid = True
        if len(form_data['trip_name']) < 3:
            flash(u"Trip name must be at least 3 characters.", 'trip error')
            is_valid = False
        if not form_data['trip_name']:
            flash(u"You must include a trip name.", 'trip error')
            is_valid = False
        if len(form_data['description']) < 3:
            flash(u"Description must be at least 3 characters.", 'trip error')
            is_valid = False
        if not form_data['description']:
            flash(u"You must include a description.", 'trip error')
            is_valid = False
        if not form_data['destinations']:
            flash(u"You must include a destination.", 'trip error')
            is_valid = False
        if len(form_data['destinations']) < 3:
            flash(u"Destination must be at least 3 characters.", 'trip error')
            is_valid = False
        if not form_data['start_date']:
            flash(u"You must include a start date.", 'trip error')
            is_valid = False
        if not form_data['end_date']:
            flash(u"You must include an end date.", 'trip error')
            is_valid = False
        if form_data['end_date'] < form_data['start_date']:
            flash(u"End date must be after the start date!", 'trip error')
            is_valid=False
        return is_valid
    @staticmethod
    def validate_update_trip(form_data):
        is_valid = True
        if len(form_data['trip_name']) < 3:
            flash(u"Trip name must be at least 3 characters.", 'trip error')
            is_valid = False
        if not form_data['trip_name']:
            flash(u"You must include a trip name.", 'trip error')
            is_valid = False
        if len(form_data['description']) < 3:
            flash(u"Description must be at least 3 characters.", 'trip error')
            is_valid = False
        if not form_data['description']:
            flash(u"You must include a description.", 'trip error')
            is_valid = False
        if not form_data['destinations']:
            flash(u"You must include a destination.", 'trip error')
            is_valid = False
        if len(form_data['destinations']) < 3:
            flash(u"Destination must be at least 3 characters.", 'trip error')
            is_valid = False
        if not form_data['start_date']:
            flash(u"You must include a start date.", 'trip error')
            is_valid = False
        if not form_data['end_date']:
            flash(u"You must include an end date.", 'trip error')
            is_valid = False
        if form_data['end_date'] < form_data['start_date']:
            flash(u"End date must be after the start date!", 'trip error')
            is_valid=False
        return is_valid
    @classmethod
    def saveTrip(cls, data):
        query = "INSERT INTO trips (trip_name, description, start_date, end_date, destinations, user_id) VALUES (%(trip_name)s, %(description)s, %(start_date)s, %(end_date)s, %(destinations)s, %(user_id)s);"
        return connectToMySQL(db).query_db( query, data )  
    
    @classmethod
    def updateTrip(cls, data, id):
        query  = f"UPDATE trips SET trip_name =%(trip_name)s, description = %(description)s, start_date = %(start_date)s, end_date =%(end_date)s, destinations =%(destinations)s  WHERE id = {id};"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_trip(cls, id):
        query  = f"SELECT * FROM trips WHERE id = {id};"
        result = connectToMySQL(db).query_db(query)
        return cls(result[0])
        
    @classmethod
    def get_one_trip_with_activities(cls, id):
        query = f"SELECT * FROM trips LEFT JOIN activities ON trips.id = activities.trip_id WHERE trips.id = {id} ORDER BY activity_start;"
        results = connectToMySQL(db).query_db(query)
        trip = cls(results[0])
        for row in results:
            data = {
                    "id": row['activities.id'],
                    "name": row['name'],
                    "type": row['type'],  
                    "activity_start": row['activity_start'],  
                    "address_location": row['address_location'],  
                    "activity_description": row['activity_description'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "trip_id": row['trip_id'],
                }
            trip.one_trip_activity_list.append(Activity(data))
        return trip

    @classmethod
    def get_past_trips(cls):
        query  = f"SELECT * FROM trips LEFT JOIN users ON trips.user_id = users.id WHERE trips.end_date < now() ORDER BY activity_start;"
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
            trips = cls(results[0])
            for row in results:
                data = {
                    "id": row['activities.id'],
                    "name": row['name'],
                    "type": row['type'],  
                    "activity_start": row['activity_start'],  
                    "address_location": row['address_location'],  
                    "activity_description": row['activity_description'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "user_id": row['trip_id'],
                }
                trips.all_past_trips.append(Trip(data))
        return trips


    @classmethod
    def get_one_activity_with_trip(cls, id):
        query = f"SELECT * FROM trips LEFT JOIN activities ON trips.id = activities.trip_id WHERE activities.id = {id};"        
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
            one_activity = cls(results[0])
            for row in results:
                data = {
                    "id": row['activities.id'],
                    "name": row['name'],
                    "type": row['type'],  
                    "activity_start": row['activity_start'],  
                    "address_location": row['address_location'],  
                    "activity_description": row['activity_description'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "trip_id": row['id'],
                }
                one_activity.trip_activity = Activity(data)
        return one_activity

    @classmethod
    def get_trip_with_entries_activities(cls, id):
        query = f"SELECT * FROM trips LEFT JOIN activities ON activities.trip_id = trips.id LEFT JOIN journal_entries ON activities.id = journal_entries.activity_id WHERE journal_entries.id = {id};"
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
            journal = cls(results[0])
            for row in results:
                activity = {
                    "id": row['activities.id'],
                    "name": row['name'],
                    "type": row['type'],  
                    "activity_start": row['activity_start'],  
                    "address_location": row['address_location'],  
                    "activity_description": row['activity_description'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "user_id": row['trip_id'],
                }
                entry = {
                    "id": row['journal_entries.id'],
                    "entry": row['entry'],
                    "picture": row['picture'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "activity_id": row['activity_id'],
                }
                journal.journal_activity.append(Activity(activity))
                journal.journal_entry.append(Journal(entry))

        return journal
