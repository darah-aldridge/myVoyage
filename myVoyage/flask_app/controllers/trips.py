from flask import render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.trip import Trip
from flask_app.models.user import User

from flask_app import app

@app.route('/plan-a-trip')
def planATrip():
    if session.get("user_id") == None:
        return redirect('/')
    return render_template("plan_trip.html")

@app.route('/submit-trip',  methods=['POST'])
def submitTrip():
    if not Trip.validate_trip(request.form):
        return redirect(f'/plan-a-trip/{trip_id}')
    end_date = request.form['end_date'] + ' 11:59:59'
    print(end_date)
    data = {
        "trip_name": request.form['trip_name'],
        "description": request.form['description'],
        "start_date": request.form['start_date'],
        "end_date": end_date,
        "destinations": request.form['destinations'],
        "user_id": session['user_id'],
    }
    
    trip_id = Trip.saveTrip(data)
    session['trip_id'] = trip_id
    return redirect(f'/plan-your-trip/{trip_id}')


@app.route('/plan-your-trip/<int:id>')
def planTrip(id):
    if session.get("user_id") == None:
        return redirect('/')
    trip = Trip.get_one_trip_with_activities(id)
    if trip == None:
        trip = Trip.get_one_trip(id)
    return render_template("trip_planner.html", trip=trip)

@app.route('/edit-your-trip/<int:id>')
def editYourTrip(id):
    if session.get("user_id") == None:
        return redirect('/')
    trip = Trip.get_one_trip(id)
    return render_template("edit_trip.html", trip=trip)

@app.route('/edit-trip/<int:id>',  methods=['POST'])
def editTrip(id):
    if not Trip.validate_update_trip(request.form):
        return redirect(f'/edit-your-trip/{id}')
    data = {
        "trip_name": request.form['trip_name'],
        "description": request.form['description'],
        "start_date": request.form['start_date'],
        "end_date": request.form['end_date'],
        "destinations": request.form['destinations'],
        "user_id": session['user_id'],
    }
    
    trip_id = Trip.updateTrip(data, id)
    session['trip_id'] = trip_id
    return redirect(f'/plan-your-trip/{id}')

@app.route('/past-trips')
def pastTrips():
    if session.get("user_id") == None:
        return redirect('/')
    return render_template("past_trips.html") 

@app.route('/trip-inspiration')
def tripInspiration():
    if session.get("user_id") == None:
        return redirect('/')
    return render_template("trip_inspiration.html") 

@app.route('/view/<int:id>')
def viewTrip(id):
    # if session.get("user_id") == None:
    #     trip = Trip.get_one_trip_with_user(id)
    #     return render_template("view_trip.html", trip = trip) 
    trip = Trip.get_one_trip_with_activities(id)
    return render_template("view_trip.html", trip = trip) 

