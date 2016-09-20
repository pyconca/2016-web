import os

from fabric import api
from fabric import utils
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project

# Deploy Config
api.env.user = 'deploy'
api.env.hosts = ['portland.pynorth.org']
api.env.use_ssh_config = True

# Git
api.env.repo = 'git://github.com/pyconca/2016-web.git'
api.env.remote = 'origin'

# Local
api.env.local_root_dir = os.path.dirname(os.path.abspath(__file__))
api.env.local_build_dir = os.path.join(api.env.local_root_dir, 'build/')
# The above needs to end with `/` or else rsync get's mad.


@api.task
def stag():
    api.env.environment = 'staging'

    # Directories
    api.env.root_dir = '/srv/www/pycon.ca/staging.2016/'
    api.env.html_dir = os.path.join(api.env.root_dir, 'html')
    api.env.venv_dir = os.path.join(api.env.root_dir, 'venv')
    api.env.app_dir = os.path.join(api.env.root_dir, 'app')

    # Python Helpers
    api.env.venv_python = os.path.join(api.env.venv_dir, 'bin/python')
    api.env.venv_pip = os.path.join(api.env.venv_dir, 'bin/pip')

    # Git
    api.env.branch = 'develop'


@api.task
def prod():
    api.env.environment = 'production'

    # Directories
    api.env.root_dir = '/srv/www/pycon.ca/2016/'
    api.env.html_dir = os.path.join(api.env.root_dir, 'html')
    api.env.venv_dir = os.path.join(api.env.root_dir, 'venv')
    api.env.app_dir = os.path.join(api.env.root_dir, 'app')

    # Python Helpers
    api.env.venv_python = os.path.join(api.env.venv_dir, 'bin/python')
    api.env.venv_pip = os.path.join(api.env.venv_dir, 'bin/pip')

    # Git
    api.env.branch = 'master'


@api.task
def deploy():
    api.require('environment')

    # Check to make sure that there isn't any unchecked files
    git_status = api.local('git status --porcelain', capture=True)

    if git_status:
        utils.abort('There are unchecked files.')

    # Push the repo to the remote
    api.local('git push {0} {1}'.format(api.env.remote, api.env.branch))

    # Build the static website.
    api.local('python manage.py freeze')

    # rsync the website to the server.
    rsync_project(remote_dir=api.env.html_dir,
                  local_dir=api.env.local_build_dir,
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


@api.task
def git_auto_deploy():
    with api.lcd(api.env.app_dir):
        # Install some dependencies
        api.local('{} install -U -r requirements.txt'.format(api.env.venv_pip))
        api.local('bower install --upgrade')

        # Generate the website
        api.local('{} manage.py freeze'.format(api.env.venv_python))

        # Copy the generated website
        api.local('rsync --delete --exclude "static/scss/" --exclude '
                  '"static/bower/" --exclude "static/.webassets-cache/" '
                  '-pthrvz {0} {1}'.format(os.path.join(api.env.app_dir,
                                                        'build/'),
                                           api.env.html_dir))
