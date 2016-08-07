from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean

from web import create_app

app = create_app()

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
