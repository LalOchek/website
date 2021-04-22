import datetime
import json
import os


def get_data_json(path):
    with open(path, "r") as f:
        tutors = json.load(f)
    return tutors


def get_tutor(path, tutor_id):
    tutors = get_data_json(path)
    return [tutor for tutor in tutors if tutor["id"] == tutor_id][0]


def get_tutors_by_goal(path, goal):
    tutors = get_data_json(path)
    return [tutor for tutor in tutors if goal in tutor["goals"]]


def get_hour_and_day():
    weekdays = dict(zip(range(1, 8), ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]))
    now_hour = datetime.datetime.now().hour
    now_day = datetime.datetime.now().weekday()
    if now_hour % 2:
        now_hour += 1

    if now_hour == 24:
        now_hour = 0
        now_day += 1
        now_day = now_day % 7

    if now_hour < 8:
        now_hour = 0

    return f"{now_hour}:00", weekdays[now_day + 1]


def get_free_tutors(path):
    now_hour, now_day = get_hour_and_day()
    if now_hour == "0:00":
        return []
    tutors = get_data_json(path)
    return [tutor for tutor in tutors if tutor["free"][now_day][now_hour]]


def append_json(data_dict, path):
    if not os.path.isfile(path):
        with open(path, "w") as f:
            json.dump([data_dict], f)
    else:
        with open(path) as f:
            data = json.load(f)

        data.append(data_dict)

        with open(path, "w") as f:
            json.dump(data, f)
