import os
import json

from flask import Blueprint, render_template, g, current_app

frontend = Blueprint('frontend', __name__)


def get_json_file(filename):
    filepath = os.path.join(current_app.config['APP_PATH'], 'data', filename)

    with open(filepath, 'r') as f:
        return json.loads(f.read())


@frontend.route('/')
def index():
    return render_template('pages/index.html')


@frontend.route('/code-of-conduct/')
@frontend.route('/code-de-conduite/', alias=True)
def code_of_conduct():
    if g.lang_code == 'fr':
        return render_template('pages/code-of-conduct_fr.html')
    else:
        return render_template('pages/code-of-conduct.html')


@frontend.route('/sponsors/')
def sponsors():
    data = get_json_file('sponsors.json')

    return render_template('pages/sponsors.html', sponsors=data)


@frontend.route('/venue/')
def venue():
    return render_template('pages/venue.html')
