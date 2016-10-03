from datetime import datetime

from icalendar import Calendar, Event

from flask import Blueprint, render_template, jsonify, g

from web.utils import get_data_file, get_markdown_file

schedule = Blueprint('schedule', __name__)


@schedule.route('/')
def index():
    """
    Schedule index page.
    """
    schedule = get_data_file('schedule.json')

    return render_template('pages/schedule/index.html', schedule=schedule)


@schedule.route('/<string:slug>/')
def talk(slug):
    """
    Talk details page.
    """
    content, meta = get_markdown_file('talks/{}'.format(slug), 'en')

    return render_template('pages/schedule/talk.html', content=content,
                           meta=meta)


@schedule.route('/<string:slug>/json/')
def talk_json(slug):
    description, content = get_markdown_file('talks/{}'.format(slug), 'en')
    content['description'] = description
    return jsonify(content)


@schedule.route('/<string:slug>/ics/')
def talk_ics(slug):
    description, content = get_markdown_file('talks/{}'.format(slug), 'en')

    cal = Calendar()
    cal.add('prodid', '-//PyCon Canada 2016//2016.pycon.ca')