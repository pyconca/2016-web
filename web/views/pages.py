from flask import Blueprint, render_template, g

from web.utils import get_json_file, get_markdown_file

pages = Blueprint('pages', __name__)


@pages.route('/')
def index():
    return render_template('pages/index.html')


@pages.route('/code-of-conduct/')
def code_of_conduct():
    if g.lang_code == 'fr':
        content = get_markdown_file('code-of-conduct', 'fr')
    else:
        content = get_markdown_file('code-of-conduct', 'en')

    return render_template('pages/code-of-conduct.html', content=content)


@pages.route('/sponsors/')
def sponsors():
    data = get_json_file('sponsors.json')

    return render_template('pages/sponsors.html', sponsors=data)


@pages.route('/venue/')
def venue():
    if g.lang_code == 'fr':
        content = {
            'location': get_markdown_file('venue-location', 'fr'),
            'travel': get_markdown_file('venue-travel', 'fr'),
            'hotel': get_markdown_file('venue-hotel', 'fr'),
            'public_transit': get_markdown_file('venue-public-transit', 'fr'),
            'toronto': get_markdown_file('venue-toronto', 'fr')
        }
    else:
        content = {
            'location': get_markdown_file('venue-location'),
            'travel': get_markdown_file('venue-travel'),
            'hotel': get_markdown_file('venue-hotel'),
            'public_transit': get_markdown_file('venue-public-transit'),
            'toronto': get_markdown_file('venue-toronto')
        }

    return render_template('pages/venue.html', content=content)


@pages.route('/about/')
def about():
    if g.lang_code == 'fr':
        content = get_markdown_file('about', 'fr')
    else:
        content = get_markdown_file('about')

    team = get_json_file('team.json')
    sponsors = get_json_file('sponsors.json')

    return render_template('pages/about.html', content=content, team=team,
                           sponsors=sponsors)


@pages.route('/volunteer/')
def volunteer():
    if g.lang_code == 'fr':
        content = get_markdown_file('volunteer', 'fr')
    else:
        content = get_markdown_file('volunteer')

    return render_template('pages/volunteer.html', content=content)


@pages.route('/guide/')
def guide():
    guide = get_json_file('guide.json')

    return render_template('pages/guide.html', guide=guide)
