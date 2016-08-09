import os

from fabric.api import task, env, local, require
from fabric.contrib.project import rsync_project

from web.config import Config

env.user = 'deploy'
env.hosts = ['portland.pynorth.org']
env.use_ssh_config = True

env.build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'build/')


@task
def stag():
    env.environment = 'staging'
    env.html_dir = '/srv/www/pycon.ca/staging.2016/html/'


@task
def prod():
    env.environment = 'production'
    env.html_dir = '/srv/www/pycon.ca/2016/html/'


@task
def deploy():
    require('environment')

    # Build the static website.
    local('python manage.py freeze')

    # rsync the website to the server.
    rsync_project(remote_dir=env.html_dir,
                  local_dir=env.build_dir,
                  delete=True,
                  exclude=['static/scss/',
                           'static/bower/',
                           'static/.webassets-cache/'])
