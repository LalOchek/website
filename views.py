from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, logout_user, login_required

from data.users import User
from forms.user import RegisterForm, LoginForm
from utils import *
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

tutors_path = "data/tutors.json"
weekdays_path = "data/weekdays.json"
goals_path = "data/goals.json"
booking_path = "data/booking.json"
request_path = "data/request.json"


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()