from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean

from flask_frozen import Freezer

from web.scripts import *
from web.app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def freeze():
    freezer = Freezer(app)

    @freezer.register_generator
    def page_list():
        for lang_code in ['en', 'fr']:
            yield 'pages.index', {'lang_code': lang_code}
            yield 'pages.guide', {'lang_code': lang_code}
            yield 'schedule.index', {'lang_code': lang_code}
            yield '/{}/schedule/schedule.json'.format(lang_code)
            yield '/{}/schedule/schedule.ics'.format(lang_code)

    freezer.freeze()


manager.add_command('tr-init', InitTranslation())
manager.add_command('tr-update', UpdateTranslations())
manager.add_command('tr-compile', CompileTranslations())

manager.add_command('alphabetize-team', AlphabetizeTeam())

manager.add_command('runserver', Server())
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
