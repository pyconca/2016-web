import os

class Config(object):
    DEBUG = True

    APP_PATH = os.path.dirname(os.path.abspath(__file__))

    LANGUAGES = {
        'en': 'English',
        'fr': 'Francais'
    }

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    SASS_LOAD_PATH = os.path.join(APP_PATH, '../bower_components')

    FREEZER_DESTINATION = os.path.join(APP_PATH, '../build/')

    MARKDOWN_EXTENSION_CONFIG = {}
