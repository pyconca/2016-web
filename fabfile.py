from fabric.api import task, env
from fabric.contrib.project import rsync_project

env.user = 'deploy'
env.hosts = ['portland.pynorth.org']
env.use_ssh_config = True

# Remote Directories
env.html_dir = '/srv/www/pycon.ca/2016/html/'

@task
def deploy_coming_soon():
    rsync_project(remote_dir=env.html_dir, local_dir='./comingsoon/')
