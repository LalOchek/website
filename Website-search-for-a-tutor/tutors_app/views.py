import random

from flask import Flask, render_template, request

from tutors_app.utils import *

app = Flask(__name__)

tutors_path = "./tutors_app/data/tutors.json"
weekdays_path = "./tutors_app/data/weekdays.json"
goals_path = "./tutors_app/data/goals.json"
booking_path = "./tutors_app/data/booking.json"
request_path = "./tutors_app/data/request.json"


@app.route("/")
def render_index():
    tutors = get_free_tutors(tutors_path)
    free = True
    return render_template("index.html", tutors=tutors, free=free)


@app.route("/profiles/")
def render_profiles():
    tutors = get_data_json(tutors_path)
    return render_template("index.html", tutors=tutors)


@app.route("/goals/<goal>/")
def render_goals(goal):
    goals = get_data_json(goals_path)
    tutors = get_tutors_by_goal(tutors_path, goal)
    return render_template("goal.html", goal=goals[goal], tutors=tutors)


@app.route("/profiles/<tutor_id>/")
def render_profile(tutor_id):
    tutor = get_tutor(tutors_path, int(tutor_id))
    goals = get_data_json(goals_path)
    weekdays = get_data_json(weekdays_path)
    return render_template("profile.html", tutor=tutor, weekdays=weekdays, goals=goals)


@app.route("/request/")
def render_request():
    return render_template("request.html")


@app.route("/request_done/", methods=["GET", "POST"])
def render_request_done():
    goals = get_data_json(goals_path)
    request_form = {
        "goal": request.form["goal"],
        "time": request.form["time"],
        "student": request.form["clientName"],
        "phone": request.form["clientPhone"],
    }
    append_json(request_form, request_path)
    return render_template("request_done.html", request_form=request_form, goals=goals)


@app.route("/booking/<tutor_id>/<day>/<hour>/")
def render_booking(tutor_id, day, hour):
    tutor = get_tutor(tutors_path, int(tutor_id))
    weekdays = get_data_json(weekdays_path)
    return render_template(
        "booking.html", tutor=tutor, day=day, hour=hour, weekdays=weekdays
    )


@app.route("/booking_done/", methods=["GET", "POST"])
def render_booking_done():
    weekdays = get_data_json(weekdays_path)
    booking_form = {
        "day": request.form["clientWeekday"],
        "hour": request.form["clientTime"],
        "tutor_id": request.form["clientTeacher"],
        "student": request.form["clientName"],
        "phone": request.form["clientPhone"],
    }
    append_json(booking_form, booking_path)
    return render_template(
        "booking_done.html", booking_form=booking_form, weekdays=weekdays
    )
