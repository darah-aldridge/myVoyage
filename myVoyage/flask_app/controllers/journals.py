from flask import render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.journal import Journal
from flask_app import app
from flask import flash

@app.route('/trip-journal')
def journal():
        # if session.get("user_id") == None:
    #     return redirect('/')
    return render_template("trip_journal.html")
