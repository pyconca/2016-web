from fabric.api import task, env, local
from fabric.contrib.project import rsync_project

from web.config import Config

env.user = 'deploy'
env.hosts = ['portland.pynorth.org']
env.use_ssh_config = True

# Remote Directories
env.html_dir = '/srv/www/pycon.ca/2016/html/'


@task
def deploy():
    rsync_project(remote_dir=env.html_dir, local_dir='./comingsoon/')


@task
def freeze():
    local('pip freeze > requirements.txt')

@task
def pybabel_extract():
    local('pybabel extract -F web/babel.cfg -o web/messages.pot web')

@task
def pybabel_init():
    local('pybabel init -i web/messages.pot -d web/translations -l fr')

@task
def pybabel_compile():
    local('pybabel compile -d web/translations')
