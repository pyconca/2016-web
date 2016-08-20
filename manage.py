import os

from flask_script import Manager, Server, Command
from flask_script.commands import ShowUrls, Clean

from flask_frozen import Freezer

from web.app import create_app

app = create_app()


class InitTranslation(Command):
    """
    Initializes a new language translation catalogue.

    From a Gist by iepathos: <https://gist.github.com/iepathos/6678261>
    """

    def run(self):
        os.system('pybabel extract -F web/babel.cfg -k lazy_gettext -o '
                  'web/messages.pot web')
        os.system('pybabel init -i web/messages.pot -d web/translations -l fr')
        os.unlink('web/messages.pot')


class UpdateTranslations(Command):
    """
    Updates the translations with pybabel extract and update commands.

    From a Gist by iepathos: <https://gist.github.com/iepathos/6678261>
    """

    def run(self):
        os.system('pybabel extract -F web/babel.cfg -k lazy_gettext -o '
                  'web/messages.pot web')
        os.system('pybabel update -i web/messages.pot -d web/translations')
        os.unlink('web/messages.pot')


class CompileTranslations(Command):
    """
    Compiles the translations with the pybabel compile command.

    From a Gist by iepathos: <https://gist.github.com/iepathos/6678261>
    """

    def run(self):
        os.system('pybabel compile -d web/translations')


manager = Manager(app)


@manager.command
def freeze():
    freezer = Freezer(app)

    @freezer.register_generator
    def page_list():
        for lang_code in ['en', 'fr']:
            yield 'pages.index', {'lang_code': lang_code}
            yield 'pages.guide', {'lang_code': lang_code}

    freezer.freeze()


manager.add_command('tr-init', InitTranslation())
manager.add_command('tr-update', UpdateTranslations())
manager.add_command('tr-compile', CompileTranslations())

manager.add_command('runserver', Server())
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
