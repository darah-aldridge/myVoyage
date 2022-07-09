import imp, re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_app.models.activity import Activity
from datetime import datetime


db ="myvoyage"

class Trip:
    def __init__( self , data ):
        self.id = data['id']
        self.trip_name = data['trip_name']
        self.description = data['description']  
        self.start_date = data['start_date'].strftime("%Y-%m-%d")  
        self.end_date = data['end_date'].strftime("%Y-%m-%d")
        self.destinations = data['destinations'] 
        self.start_date_mmddyyyy = data['start_date'].strftime("%m/%d/%Y")
        self.end_date_mmddyyyy = data['end_date'].strftime("%m/%d/%Y")
        self.activity_list = []
        self.all_past_trips = []
        self.user_trip = []
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
        query = f"SELECT * FROM trips JOIN activities ON trips.id = activities.trip_id WHERE trips.id = {id} ORDER BY activity_start;"
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
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
                    "user_id": row['trip_id'],
                }
                trip.activity_list.append(Activity(data))
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
    def get_one_trip_with_activities(cls, id):
        query = f"SELECT * FROM trips LEFT JOIN activities ON trips.id = activities.trip_id WHERE trips.id = {id} ORDER BY activity_start;"
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
            one_trip_user = cls(results[0])
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
                    "trip_id": row['trip_id'],
                }
                one_trip_user.activity_list.append(Activity(activity))
        return one_trip_user