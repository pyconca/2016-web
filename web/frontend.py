from flask import Blueprint, render_template, g

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return render_template('pages/index.html')


@frontend.route('/code-of-conduct')
@frontend.route('/code-de-conduite')
def code_of_conduct():
    if g.lang_code == 'fr':
        return render_template('pages/code-of-conduct_fr.html')
    else:
        return render_template('pages/code-of-conduct.html')
