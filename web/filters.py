import datetime

from flask import url_for, g
from flask.ext import babel

from web.utils import get_markdown_file


def format_datetime(value, format='full'):
    if type(value) is str or type(value) is unicode:
        datetimeobj = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        return babel.format_datetime(datetimeobj, format)
    else:
        return babel.format_datetime(value, format)


def format_date(value, format='full'):
    if type(value) is str or type(value) is unicode:
        datetimeobj = datetime.datetime.strptime(value, '%Y-%m-%d')
        return babel.format_date(datetimeobj.date(), format)
    else:
        return babel.format_date(value, format)


def format_time(value, format='full'):
    if type(value) is str or type(value) is unicode:
        datetimeobj = datetime.datetime.strptime(value, '%H:%M:%S')
        return babel.format_date(datetimeobj.time(), format)
    else:
        return babel.format_time(value, format)


def get_talk(slug):
    content, meta = get_markdown_file('talks/{}'.format(slug), g.lang_code)

    if slug:
        meta['link'] = url_for('schedule.talk', slug=slug)
    else:
        meta['link'] = None

    return meta
