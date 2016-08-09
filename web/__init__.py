import os

from flask import Flask, g, abort

from flask_babel import Babel
import flask_assets as assets

from webassets.filter import get_filter

from .frontend import frontend


def create_app(configfile=None):
    app = Flask(__name__)

    app.config.from_object('web.config.Config')

    env = assets.Environment(app)

    static_path = os.path.join(app.config['APP_PATH'], 'static')

    env.load_path = [
        os.path.join(static_path, 'bower'),
        os.path.join(static_path, 'scss'),
        os.path.join(static_path, 'javascript')
    ]

    env.register('js_all',
        assets.Bundle(
            'jquery/dist/jquery.min.js',
            assets.Bundle(
                'app.js'
            ),
            output='app.js'
        )
    )

    sass = get_filter('scss')
    sass.load_paths = env.load_path

    env.register('css_all',
        assets.Bundle(
            'app.scss',
            filters=(sass,),
            depends=(os.path.join(static_path, 'scss/**/*.scss')),
            output='app.css'
        )
    )

    babel = Babel(app)

    @app.url_defaults
    def set_language_code(endpoint, values):
        if 'lang_code' in values or not g.get('lang_code', None):
            return
        if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
            values['lang_code'] = g.lang_code

    @app.url_value_preprocessor
    def get_lang_code(endpoint, values):
        if values is not None:
            g.lang_code = values.pop('lang_code', None)

    @app.before_request
    def ensure_lang_support():
        lang_code = g.get('lang_code', None)
        if lang_code and lang_code not in app.config['LANGUAGES'].keys():
            return abort(404)

    @babel.localeselector
    def get_locale():
        return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])

    @babel.timezoneselector
    def get_timezone():
        return app.config['BABEL_DEFAULT_TIMEZONE']

    app.register_blueprint(frontend, url_prefix='/<lang_code>')

    return app
