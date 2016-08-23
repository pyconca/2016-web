from flask import Blueprint, render_template, g

from web.utils import get_json_file, get_markdown_file

pages = Blueprint('pages', __name__)


@pages.route('/')
def index():
    return render_template('pages/index.html')


@pages.route('/code-of-conduct/')
def code_of_conduct():
    content = get_markdown_file('code-of-conduct', g.lang_code)

    return render_template('pages/code-of-conduct.html', content=content)


@pages.route('/sponsors/')
def sponsors():
    data = get_json_file('sponsors.json')
    content = content = get_markdown_file('sponsors', g.lang_code)

    return render_template('pages/sponsors.html', content=content,
                           sponsors=data)


@pages.route('/venue/')
def venue():
    content = {
        'location': get_markdown_file('venue-location', g.lang_code),
        'travel': get_markdown_file('venue-travel', g.lang_code),
        'hotel': get_markdown_file('venue-hotel', g.lang_code),
        'public_transit': get_markdown_file('venue-public-transit',
                                            g.lang_code),
        'toronto': get_markdown_file('venue-toronto', g.lang_code)
    }

    return render_template('pages/venue.html', content=content)


@pages.route('/about/')
def about():
    content = get_markdown_file('about', g.lang_code)
    team = get_json_file('team.json')
    sponsors = get_json_file('sponsors.json')

    return render_template('pages/about.html', content=content, team=team,
                           sponsors=sponsors)


@pages.route('/volunteer/')
def volunteer():
    content = get_markdown_file('volunteer', g.lang_code)

    return render_template('pages/volunteer.html', content=content)


@pages.route('/guide/')
def guide():
    guide = get_json_file('guide.json')

    return render_template('pages/guide.html', guide=guide)
