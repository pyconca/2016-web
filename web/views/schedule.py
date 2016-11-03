from datetime import datetime

import pytz
from icalendar import Calendar, Event

from flask import Blueprint, render_template, jsonify, Response, url_for, abort

from web.utils import get_data_file, get_markdown_file

schedule = Blueprint('schedule', __name__)

tz = pytz.timezone('Canada/Eastern')


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

    if slug == 'schedule':
        content = get_data_file('schedule.json')
    else:
        description, content = get_markdown_file('talks/{}'.format(slug), 'en')

        # The Markdown Meta extension gives us everything in lists.
        # So this is a simple converter.
        for k, v in content.items():
            content[k] = v[0]

        content['description'] = description

    return jsonify(content)


def event_ics(slug):
    description, content = get_markdown_file('talks/{}'.format(slug), 'en')

    if not content:
        abort(404)

    for k, v in content.items():
        content[k] = v[0]

    start_time = datetime.strptime('{0} {1}'.format(content['date'],
                                                    content['start_time']),
                                   '%Y-%m-%d %H:%M:%S')

    end_time = datetime.strptime('{0} {1}'.format(content['date'],
                                                  content['end_time']),
                                 '%Y-%m-%d %H:%M:%S')

    event = Event()

    if content.get('speakers'):
        event.add('summary', u"{0} with {1}".format(content['title'],
                                                    content['speakers']))
    else:
        event.add('summary', u"{}".format(content['title']))

    event.add('dtstart', tz.localize(start_time))
    event.add('dtend', tz.localize(end_time))
    event.add('dtstamp', tz.localize(start_time))

    event.add('location', 'Room {}'.format(content['rooms']))

    event.add('uid', slug)

    tpl_url = 'https://2016.pycon.ca{0}'
    event.add('url', tpl_url.format(url_for('schedule.talk', slug=slug)))

    return event


@schedule.route('/<string:slug>.ics')
def talk_ics(slug):
    cal = Calendar()
    cal.add('prodid', '-//PyCon Canada 2016//2016.pycon.ca')
    cal.add('version', '2.0')

    if slug == 'schedule':
        schedule = get_data_file('schedule.json')

        # TODO: This should be refactored because it's really ugly.
        for day in schedule.get('days'):
            for slot in day.get('entries'):
                if slot.get('link'):
                    cal.add_component(event_ics(slot.get('link')))

                elif slot.get('talks'):
                    for room, talk in slot.get('talks').iteritems():
                        if talk:
                            cal.add_component(event_ics(talk))
                else:
                    start_time_str = '{0} {1}'.format(day['date'],
                                                      slot['start_time'])
                    start_time = datetime.strptime(start_time_str,
                                                   '%Y-%m-%d %H:%M:%S')

                    end_time_str = '{0} {1}'.format(day['date'],
                                                    slot['end_time'])
                    end_time = datetime.strptime(end_time_str,
                                                 '%Y-%m-%d %H:%M:%S')

                    event = Event()
                    event.add('summary', slot['title'])

                    event.add('dtstart', tz.localize(start_time))
                    event.add('dtend', tz.localize(end_time))
                    event.add('dtstamp', tz.localize(start_time))

                    cal.add_component(event)
    else:
        cal.add_component(event_ics(slug))

    headers = {
        'Content-Disposition': 'attachment;filename={0}.ics'.format(slug)
    }

    return Response(response=cal.to_ical(),
                    status=200,
                    mimetype='text/calendar',
                    headers=headers)
