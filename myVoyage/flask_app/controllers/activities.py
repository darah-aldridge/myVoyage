from flask import render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.activity import Activity
from flask_app import app

@app.route('/add_activity',  methods=['POST'])
def addActivity():
    trip_id = request.form['trip_id']
    if not Activity.validate_activity(request.form):
        return redirect(f'/plan-a-trip/{trip_id}')
    data = {
        "name": request.form['activity_name'],
        "type": request.form['activity_type'],
        "activity_start": request.form['activity_start'],
        "address_location": request.form['address'],
        "activity_description": request.form['description'],
        "trip_id": trip_id,
    }
    Activity.saveActivity(data)
    return redirect(f'/plan-your-trip/{trip_id}')


@app.route('/edit-activity/<int:id>')
def editActivity(id):
    if session.get("user_id") == None:
        return redirect('/')
    activity = Activity.get_one_activity(id)
    return render_template("edit_activity.html", activity=activity)

@app.route('/submit_edit_activity/<int:id>',  methods=['POST'])
def submitEditActivity(id, trip_id):
    if not Activity.validate_update_activty(request.form):
        return redirect(f'/edit-activity/{id}')
    data = {
        "name": request.form['activity_name'],
        "type": request.form['activity_type'],
        "activity_start": request.form['activity_start'],
        "address_location": request.form['address'],
        "activity_description": request.form['description'],
        "trip_id": trip_id,
    }
    Activity.updateActivity(data, id)
    return redirect(f'/plan-your-trip/{trip_id}')