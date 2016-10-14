from os import system, unlink

from flask_script import Command


class InitTranslation(Command):
    """
    Initializes a new language translation catalogue.

    From a Gist by iepathos: <https://gist.github.com/iepathos/6678261>
    """

    def run(self):
        system('pybabel extract -F web/babel.cfg -k lazy_gettext -o '
               'web/messages.pot web')
        system('pybabel init -i web/messages.pot -d web/translations -l fr')
        unlink('web/messages.pot')


class UpdateTranslations(Command):
    """
    Updates the translations with pybabel extract and update commands.

    From a Gist by iepathos: <https://gist.github.com/iepathos/6678261>
    """

    def run(self):
        system('pybabel extract -F web/babel.cfg -k lazy_gettext -o '
               'web/messages.pot web')
        system('pybabel update -i web/messages.pot -d web/translations')
        unlink('web/messages.pot')


class CompileTranslations(Command):
    """
    Compiles the translations with the pybabel compile command.

    From a Gist by iepathos: <https://gist.github.com/iepathos/6678261>
    """

    def run(self):
        system('pybabel compile -d web/translations')
