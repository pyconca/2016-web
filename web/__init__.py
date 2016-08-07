from flask import Flask, g, abort

from flask_babel import Babel

from .frontend import frontend


def create_app(configfile=None):
    app = Flask(__name__)

    app.config.from_object('web.config.Config')

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
