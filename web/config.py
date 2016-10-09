import os


class Config(object):
    DEBUG = True

    # Paths
    APP_PATH = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = os.path.join(APP_PATH, 'static')

    # i18n Config
    LANGUAGES = {
        'en': 'English',
        'fr': 'Francais'
    }

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    FREEZER_STATIC_IGNORE = ('*.scss', '*.scssc')
    # Destination of the build directory
    FREEZER_DESTINATION = os.path.join(APP_PATH, '../build/')

    MARKDOWN_EXTENSION_CONFIG = {}

    SPEAKER_IMG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'images')
