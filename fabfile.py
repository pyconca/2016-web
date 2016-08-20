import os

from fabric import api
from fabric import utils
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project

from web.config import Config

# Deploy Config
api.env.user = 'deploy'
api.env.hosts = ['portland.pynorth.org']
api.env.use_ssh_config = True

# Git
api.env.repo = 'git://github.com/pyconca/2016-web.git'
api.env.remote = 'origin'
api.env.branch = 'master'

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


@api.task
def setup():
    """
    Setup the deploy server.
    """
    api.sudo('mkdir -p {0}'.format(' '.join([api.env.html_dir,
                                             api.env.venv_dir,
                                             api.env.app_dir])))

    # Make sure the directories are writeable by me.
    api.sudo('chown {0}:{0} {1}'.format(api.env.user,
                                        ' '.join([api.env.html_dir,
                                                  api.env.venv_dir,
                                                  api.env.app_dir])))

    if not exists(os.path.join(api.env.app_dir, '.git')):
        # Clone the GitHub Repo
        with api.cd(api.env.app_dir):
            api.run('git clone {0} .'.format(api.env.repo))

    # Createh virtual environment.
    if not exists(os.path.join(api.env.venv_dir, 'bin')):
        api.run('virtualenv {0}'.format(api.env.venv_dir))

    # Install the dependencies.
    pip_upgrade()


@api.task
def python_version():
    """
    Return the Python version on the server for testing.
    """
    with api.cd(api.env.app_dir):
        api.run("{0} -V".format(api.env.venv_python))


@api.task
def update_code():
    """
    Update to the latest version of the code.
    """
    with api.cd(api.env.app_dir):
        api.run('git reset --hard HEAD')
        api.run('git checkout {0}'.format(api.env.branch))
        api.run('git pull {0} {1}'.format(api.env.remote, api.env.branch))


@api.task
def pip_upgrade():
    """
    Upgrade the third party Python libraries.
    """
    with api.cd(api.env.app_dir):
        api.run('{0} install --upgrade -r '
                'requirements.txt'.format(api.env.venv_pip))


@api.task
def bower_upgrade():
    with api.cd(api.env.app_dir):
        api.run('bower install')


@api.task
def local_deploy():
    # Check to make sure that there isn't any unchecked files
    git_status = api.local('git status --porcelain', capture=True)
    
    if git_status:
        utils.abort('There are unchecked files.')
    
    # Push the repo to the remote
    api.local('git push {0} {1}'.format(api.env.remote, api.env.branch))

    # The deploy tasks
    update_code()
    pip_upgrade()
    bower_upgrade()

    # Make the build directory.
    build_dir = os.path.join(api.env.app_dir, 'build')

    # Build the static website.
    with api.cd(api.env.app_dir):
        api.run('{0} manage.py freeze'.format(api.env.venv_python))

    # Remove some of the auto generate folders
    remove_dir = [os.path.join(build_dir, 'static/scss/'),
                  os.path.join(build_dir, 'static/bower/'),
                  os.path.join(build_dir, 'static/.webassets-cache/')]

    api.run('rm -r {0}'.format(' '.join(remove_dir)))

    # Copy the files.
    api.run('cp -a {0}/. {1}/'.format(build_dir, api.env.html_dir))

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