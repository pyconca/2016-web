from datetime import datetime

import pytz
from icalendar import Calendar, Event

from flask import Blueprint, render_template, jsonify, Response, url_for, g

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
                           meta=meta, slug=slug)


@schedule.route('/<string:slug>.json')
def talk_json(slug):
    description, content = get_markdown_file('talks/{}'.format(slug), 'en')
    content['description'] = description
    return jsonify(content)


@schedule.route('/<string:slug>.ics')
def talk_ics(slug):
    description, content = get_markdown_file('talks/{}'.format(slug), 'en')

    tz = pytz.timezone('Canada/Eastern')

    start_time = datetime.strptime('{0} {1}'.format(content['date'][0],
                                                    content['start_time'][0]),
                                   '%Y-%m-%d %H:%M:%S')

    end_time = datetime.strptime('{0} {1}'.format(content['date'][0],
                                                  content['end_time'][0]),
                                 '%Y-%m-%d %H:%M:%S')

    cal = Calendar()
    cal.add('prodid', '-//PyCon Canada 2016//2016.pycon.ca')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', u"{0} with {1}".format(content['title'][0],
                                                content['speakers'][0]))
    event.add('dtstart', tz.localize(start_time))
    event.add('dtend', tz.localize(end_time))
    event.add('dtstamp', tz.localize(start_time))

    event.add('uid', slug)

    tpl_url = 'https://2016.pycon.ca{0}'
    event.add('url', tpl_url.format(url_for('schedule.talk', slug=slug)))

    cal.add_component(event)

    headers = {
        'Content-Disposition': 'attachment;filename={0}.ics'.format(slug)
    }

    return Response(response=cal.to_ical(),
                    status=200,
                    mimetype='text/x-calendar',
                    headers=headers)
