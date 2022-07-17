import email
import imp, re
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_app.models.trip import Trip
from flask_app.models.activity import Activity
from flask_app.models.journal import Journal

import pprint

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


db ="myvoyage"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r"^[A-Za-z]+$") 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']  
        self.email = data['email']
        self.bio = data['bio']
        self.profile_picture = data['profile_picture']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_past_trips = []
        self.user_future_trips = []
        self.future_trip_activities = []
        self.trip_inspo = []
        self.trip_activities = []
        self.user_trip = []
        self.user_trips = []
        self.trips_activities = []
        self.journal_entries = []
    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if not EMAIL_REGEX.match(form_data['email']): 
            flash(u"Invalid email address!", 'register error')
            is_valid = False
        if len(form_data['first_name']) < 3:
            flash(u"First name must be at least 3 characters.", 'register error')
            is_valid = False
        if not form_data['first_name']:
            flash(u"You must include a first name.", 'register error')
            is_valid = False
        if not NAME_REGEX.match(form_data['first_name']):
            flash(u"You can only use letters for your first name.", 'register error')
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash(u"Last name must be at least 3 characters.", 'register error')
            is_valid = False
        if not form_data['last_name']:
            flash(u"You must include a last name.", 'register error')
            is_valid = False
        if not NAME_REGEX.match(form_data['last_name']):
            flash(u"You can only use letters for your last name.", 'register error')
            is_valid = False
        if not form_data['email']:
            flash(u"You must include an email.", 'register error')
            is_valid = False
        if not form_data['password']:
            flash(u"You must include an password.", 'register error')
            is_valid = False
        if User.get_by_email({'email': form_data['email']}):
            flash(u"Email address is already in use!", 'register error')
            is_valid=False
        if form_data['password'] != form_data['confirm_password']:
            flash(u"Passwords don't match!", 'register error')
            is_valid=False
        if len(form_data['password']) < 8:
            flash(u"Password must be at least 8 characters.", 'register error')
            is_valid = False
        return is_valid
    @staticmethod
    def validate_update(form_data):
        is_valid = True
        if not EMAIL_REGEX.match(form_data['email']): 
            flash(u"Invalid email address!", 'update error')
            is_valid = False
        if len(form_data['first_name']) < 3:
            flash(u"First name must be at least 3 characters.", 'update error')
            is_valid = False
        if not form_data['first_name']:
            flash(u"You must include a first name.", 'update error')
            is_valid = False
        if not NAME_REGEX.match(form_data['first_name']):
            flash(u"You can only use letters for your first name.", 'update error')
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash(u"Last name must be at least 3 characters.", 'update error')
            is_valid = False
        if not form_data['last_name']:
            flash(u"You must include a last name.", 'update error')
            is_valid = False
        if not NAME_REGEX.match(form_data['last_name']):
            flash(u"You can only use letters for your last name.", 'update error')
            is_valid = False
        if not form_data['email']:
            flash(u"You must include an email.", 'update error')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, bio, profile_picture, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(bio)s, %(profile_picture)s, %(password)s);"
        return connectToMySQL(db).query_db( query, data )  

    @classmethod
    def login(cls, data):
        query  = "SELECT * FROM users WHERE password = %(password)s && email = %(email)s;"
        results = connectToMySQL(db).query_db(query)
        if results:
            return cls(results[0])
        else:
            return False
        
    @classmethod
    def get_by_email(cls, email):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, email)
        if len(results) < 1:
            return False
        if results:
            return cls(results[0])
        else:
            return False

    @classmethod
    def get_one(cls, id):
        query  = f"SELECT * FROM users WHERE id = {id};"
        result = connectToMySQL(db).query_db(query)
        return cls(result[0])

    @classmethod
    def edit(cls, data, id):
        query  = f"UPDATE users SET first_name =%(first_name)s, last_name = %(last_name)s, email = %(email)s, bio =%(bio)s  WHERE id = {id};"
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_one_user_with_past_trips(cls, id):
        query = f"SELECT * FROM users LEFT JOIN trips ON users.id = trips.user_id WHERE users.id = {id} and trips.end_date < now() ORDER BY start_date;"
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
            past_trips = cls(results[0])
            for row in results:
                data = {
                    "id": row['trips.id'],
                    "trip_name": row['trip_name'],
                    "description": row['description'],  
                    "start_date": row['start_date'],  
                    "end_date": row['end_date'],  
                    "destinations": row['destinations'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "user_id": row['user_id'],
                }
                past_trips.user_past_trips.append(Trip(data))
        return past_trips

    @classmethod
    def get_one_user_with_future_trips(cls, id):
        query = f"SELECT * FROM users LEFT JOIN trips ON users.id = trips.user_id LEFT JOIN activities ON activities.trip_id = trips.id WHERE trips.end_date >= now() and users.id = {id} ORDER BY start_date, activity_start;"
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
            future_trips = cls(results[0])
            for row in results:
                trip = {
                    "id": row['trips.id'],
                    "trip_name": row['trip_name'],
                    "description": row['description'],  
                    "start_date": row['start_date'],  
                    "end_date": row['end_date'],  
                    "destinations": row['destinations'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "user_id": row['user_id'],
                }
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
                future_trips.user_future_trips.append(Trip(trip))
                future_trips.future_trip_activities.append(Activity(activity))
        return future_trips

    @classmethod
    def get_all_trips_with_users(cls):
        query = f"SELECT * FROM users JOIN trips ON users.id = trips.user_id ORDER BY trips.start_date;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for row in results:
            if len(users) == 0:
                users.append(cls(row))
            else:
                trip_inspo = users[len(users)-1]
                if trip_inspo.id != row['id']:
                    users.append(cls(row))
            trip_inspo = users[len(users)-1]
            trips = {
                "id": row['trips.id'],
                "trip_name": row['trip_name'],
                "description": row['description'],  
                "start_date": row['start_date'],  
                "end_date": row['end_date'],  
                "destinations": row['destinations'],  
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
                "user_id": row['user_id'],
            }
            trip_inspo.trip_inspo.append(Trip(trips))
        return users


    @classmethod
    def get_user_with_trip_activities(cls, id):
        query = f"SELECT * FROM users LEFT JOIN trips ON users.id = trips.user_id LEFT JOIN activities ON activities.trip_id = trips.id LEFT JOIN journal_entries ON journal_entries.activity_id = activities.id WHERE trips.id = {id} ORDER BY start_date, activity_start;"
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
            trip = cls(results[0])
            for row in results:
                trip_data = {
                    "id": row['trips.id'],
                    "trip_name": row['trip_name'],
                    "description": row['description'],  
                    "start_date": row['start_date'],  
                    "end_date": row['end_date'],  
                    "destinations": row['destinations'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "user_id": row['user_id'],
                }
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
                trip.user_trip.append(Trip(trip_data))
                trip.trip_activities.append(Activity(activity))
                trip.journal_entries.append(Journal(entry))
        return trip

    @classmethod
    def get_user_with_trips_activities(cls, id):
        query = f"SELECT * FROM users LEFT JOIN trips ON users.id = trips.user_id LEFT JOIN activities ON activities.trip_id = trips.id WHERE users.id = {id} ORDER BY start_date, activity_start;"
        results = connectToMySQL(db).query_db(query)
        if not results:
            return None
        else:
            trip = cls(results[0])
            for row in results:
                trip_data = {
                    "id": row['trips.id'],
                    "trip_name": row['trip_name'],
                    "description": row['description'],  
                    "start_date": row['start_date'],  
                    "end_date": row['end_date'],  
                    "destinations": row['destinations'],  
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at'],
                    "user_id": row['user_id'],
                }
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
                trip.user_trips.append(Trip(trip_data))
                trip.trips_activities.append(Activity(activity))
        return trip
