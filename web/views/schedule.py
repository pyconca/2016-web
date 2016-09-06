from flask import Blueprint, render_template

schedule = Blueprint('schedule', __name__)


@schedule.route('/')
def index():
    """
    Schedule index page.
    """
    return render_template('pages/schedule/index.html')


@schedule.route('/<path:slug>/')
def talk():
    """
    Talk details page.
    """
    return render_template('pages/schedule/talk.html')
