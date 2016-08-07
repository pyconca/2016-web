import os

class Config(object):
    APP_PATH = os.path.dirname(os.path.abspath(__file__))

    LANGUAGES = {
        'en': 'English',
        'fr': 'Francais'
    }

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    FREEZER_DESTINATION = os.path.join(APP_PATH, '../build/')
