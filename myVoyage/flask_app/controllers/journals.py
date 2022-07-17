from flask import render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.journal import Journal
from flask_app import app
from flask import flash
from flask_app.models.user import User
from flask_app.models.trip import Trip


@app.route('/journal/<int:id>')
def journal(id):
    trip = User.get_user_with_trip_activities(id)
    if session.get("user_id") != trip.id:
        return redirect('/trip-inspiration')
    return render_template("trip_journal.html", trip = trip) 


@app.route('/add_entry',  methods=['POST'])
def addEntry():
    trip_id = request.form['trip_id']
    if not Journal.validate_entry(request.form):
        return redirect(f'/journal/{trip_id}')
    data = {
        "entry": request.form['entry'],
        "picture": request.form['picture'],
        "activity_id": request.form['activity'],
    }
    Journal.saveJournal(data)
    return redirect(f'/journal/{trip_id}')


@app.route('/edit-journal/<int:id>')
def editEntry(id):
    if session.get("user_id") == None:
        return redirect('/')
    trip = Trip.get_trip_with_entries_activities(id)
    return render_template("edit_journal.html", trip=trip)

@app.route('/submit_edit_journal/<int:id>',  methods=['POST'])
def submitEditEntry(id):
    if not Journal.validate_update_entry(request.form):
        return redirect(f'/edit-journal/{id}')
    trip_id = request.form['trip_id']
    data = {
        "entry": request.form['entry'],
        "picture": request.form['picture'],
        "activity_id": request.form['activity_id']
    }
    Journal.updateJournal(data, id)
    return redirect(f'/journal/{trip_id}')