from flask import url_for, g
from flask.ext import babel

from web.utils import get_markdown_file


def format_datetime(value, format='full'):
    return babel.format_datetime(value, format)


def format_date(value, format='full'):
    return babel.format_date(value, format)


def format_time(value, format='full'):
    return babel.format_time(value, format)


def get_talk(slug):
    content, meta = get_markdown_file('talks/{}'.format(slug), g.lang_code)

    if slug:
        meta['link'] = url_for('schedule.talk', slug=slug)
    else:
        meta['link'] = None

    return meta
