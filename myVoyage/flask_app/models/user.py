import email
import imp, re
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
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


