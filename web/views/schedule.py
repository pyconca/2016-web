from flask import Blueprint, render_template, g

schedule = Blueprint('schedule', __name__)


@schedule.route('/')
def index():
    return render_template('pages/schedule/index.html')


@schedule.rote('/<path:slug>/')
def talk():
    return render_template('pages/schedule/talk.html')
