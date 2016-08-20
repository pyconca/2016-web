import os

from fabric import api
from fabric import utils
from fabric.contrib.project import rsync_project

from web.config import Config

api.env.user = 'deploy'
api.env.hosts = ['portland.pynorth.org']
api.env.use_ssh_config = True

api.env.build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'build/')


@api.task
def stag():
    api.env.environment = 'staging'
    api.env.html_dir = '/srv/www/pycon.ca/staging.2016/html/'


@api.task
def prod():
    api.env.environment = 'production'
    api.env.html_dir = '/srv/www/pycon.ca/2016/html/'


@api.task
def deploy():
    api.require('environment')

    # Check to make sure that there isn't any unchecked files
    git_status = api.local('git status --porcelain', capture=True)

    if git_status:
        utils.abort('There are unchecked files.')

    # Build the static website.
    api.local('python manage.py freeze')

    # rsync the website to the server.
    rsync_project(remote_dir=api.env.html_dir,
                  local_dir=api.env.build_dir,
                  delete=True,
                  exclude=['static/scss/',
                           'static/bower/',
                           'static/.webassets-cache/'])

    # Draw a ship
    utils.puts("               |    |    |               ")
    utils.puts("              )_)  )_)  )_)              ")
    utils.puts("             )___))___))___)\            ")
    utils.puts("            )____)____)_____)\\          ")
    utils.puts("          _____|____|____|____\\\__      ")
    utils.puts(" ---------\                   /--------- ")
    utils.puts("   ^^^^^ ^^^^^^^^^^^^^^^^^^^^^           ")
    utils.puts("     ^^^^      ^^^^     ^^^    ^^        ")
    utils.puts("          ^^^^      ^^^                  ")