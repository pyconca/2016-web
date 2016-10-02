from flask import Blueprint, render_template, g

from web.utils import get_data_file, get_markdown_file

schedule = Blueprint('schedule', __name__)


@schedule.route('/')
def index():
    """
    Schedule index page.
    """
    schedule = get_data_file('schedule.json')

    return render_template('pages/schedule/index.html', schedule=schedule)


@schedule.route('/<slug>/')
def talk(slug):
    """
    Talk details page.
    """
    content, meta = get_markdown_file('talks/{}'.format(slug), 'en')

    return render_template('pages/schedule/talk.html', content=content,
                           meta=meta)
