from flask import Blueprint, render_template, g

from web.utils import get_json_file, get_markdown_file

pages = Blueprint('pages', __name__)


@pages.route('/')
def index():
    """
    Landing page.
    """

    sponsors = get_json_file('sponsors.json')

    return render_template('pages/index.html', sponsors=sponsors)


@pages.route('/code-of-conduct/')
def code_of_conduct():
    """
    Code of Conduct page.
    """
    content, meta = get_markdown_file('code-of-conduct', g.lang_code)

    return render_template('pages/code-of-conduct.html', content=content,
                           meta=meta)


@pages.route('/sponsors/')
def sponsors():
    """
    Sponsors page.
    """
    data = get_json_file('sponsors.json')
    content, meta = get_markdown_file('sponsors', g.lang_code)

    return render_template('pages/sponsors.html', content=content, meta=meta,
                           sponsors=data)


@pages.route('/venue/')
def venue():
    """
    Venue page.
    """
    content = {
        'location': get_markdown_file('venue-location', g.lang_code)[0],
        'travel': get_markdown_file('venue-travel', g.lang_code)[0],
        'hotel': get_markdown_file('venue-hotel', g.lang_code)[0],
        'public_transit': get_markdown_file('venue-public-transit',
                                            g.lang_code)[0],
        'toronto': get_markdown_file('venue-toronto', g.lang_code)[0]
    }

    return render_template('pages/venue.html', content=content)


@pages.route('/about/')
def about():
    """
    About page.
    """
    team = get_json_file('team.json')
    sponsors = get_json_file('sponsors.json')
    content, meta = get_markdown_file('about', g.lang_code)

    return render_template('pages/about.html', content=content, meta=meta,
                           team=team, sponsors=sponsors)


@pages.route('/volunteer/')
def volunteer():
    """
    Volunteer at PyCon Canada page.
    """
    content, meta = get_markdown_file('volunteer', g.lang_code)

    return render_template('pages/volunteer.html', content=content, meta=meta)


@pages.route('/guide/')
def guide():
    """
    Guide to things around the venue area page.
    """
    guide = get_json_file('guide.json')

    return render_template('pages/guide.html', guide=guide)
