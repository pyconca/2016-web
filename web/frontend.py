from flask import Blueprint, render_template, g, current_app

from .utils import get_json_file, get_markdown_file

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return render_template('pages/index.html')


@frontend.route('/code-of-conduct/')
@frontend.route('/code-de-conduite/', alias=True)
def code_of_conduct():
    if g.lang_code == 'fr':
        content = get_markdown_file('code-of-conduct_fr.markdown')
    else:
        content = get_markdown_file('code-of-conduct_en.markdown')

    return render_template('pages/code-of-conduct.html', content=content)


@frontend.route('/sponsors/')
def sponsors():
    data = get_json_file('sponsors.json')

    return render_template('pages/sponsors.html', sponsors=data)


@frontend.route('/venue/')
def venue():
    if g.lang_code == 'fr':
        content = get_markdown_file('venue_fr.markdown')
    else:
        content = get_markdown_file('venue_en.markdown')

    return render_template('pages/venue.html', content=content)


@frontend.route('/about/')
def about():
    if g.lang_code == 'fr':
        content = get_markdown_file('about_fr.markdown')
    else:
        content = get_markdown_file('about_en.markdown')

    return render_template('pages/about.html', content=content)


@frontend.route('/volunteer/')
def volunteer():
    if g.lang_code == 'fr':
        content = get_markdown_file('volunteer_fr.markdown')
    else:
        content = get_markdown_file('volunteer_en.markdown')

    return render_template('pages/volunteer.html', content=content)