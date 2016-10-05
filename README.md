# PyCon Canada 2016 Website

The source code for [PyCon Canada's 2016 conference website](https://2016.pycon.ca/).

## Objectives

* Have a concise and helpful website to help promote the conference and give attendees the best possible experience
* Regularly updated with relevant content
* Highlight all the volunteers, speakers, and sponsors who make this event possible
* Be easy for organizers to maintain

## Updating the Website Contents

* Page content files (i.e. About, Venue, Code of Conduct, Volunteer, etc.) are located in [./web/markdown/](./web/markdown)
* Page data (i.e. Sponsors, Organizers, etc.) are located in [./web/data/](./web/data)
* The French translation is in [./web/translations/fr/LC_MESSAGES/messages.po](./web/translations/fr/LC_MESSAGES/messages.po)

## Stages

### Stage One ([Open Issues](https://github.com/pyconca/2016-web/issues?q=is%3Aopen+is%3Aissue+milestone%3A%22Stage+One%22))

* Get a basic two page website built.

### Stage Two ([Open Issues](https://github.com/pyconca/2016-web/issues?q=is%3Aopen+is%3Aissue+milestone%3A%22Stage+Two%22))

* Design
* Develop a basic CMS for multiple pages.

### Stage Three ([Open Issues](https://github.com/pyconca/2016-web/issues?q=is%3Aopen+is%3Aissue+milestone%3A%22Stage+Three%22))

* Website should magically build when a change is made on the [GitHub](https://github.com/pyconca/2016-web) repo or the [PyConCA CfP](https://cfp.pycon.ca/)

### Stage Four ([Open Issues](https://github.com/pyconca/2016-web/issues?q=is%3Aopen+is%3Aissue+milestone%3A%22Stage+Four%22))

* Schedule and individual talk pages.

### Stage Five ([Open Issues](https://github.com/pyconca/2016-web/issues?q=is%3Aopen+is%3Aissue+milestone%3A%22Stage+Five%22))

* Task that need to be completed before the conference starts.

### Stage Six ([Open Issues](https://github.com/pyconca/2016-web/issues?q=is%3Aopen+is%3Aissue+milestone%3A%22Stage+Six%22))

* Individual talk pages should have links to the YouTube Videos.

## Development Environment Setup

You will need the following:

* Python 2.7
* pip
* virtualenvwrapper
* sass - `sudo gem install sass`
* bower - `sudo npm install -g bower`
* [git-lfs](https://git-lfs.github.com/) (this is used to store the large image files).

Start by cloning the repository:

```
$ git clone git@github.com:pyconca/2016-web.git
$ cd ~/2016-web
```

Install the static asset dependencies:

```
~/2016-web $ bower install
```

Create a python virtual environment:

```
~/2016-web $ mkvirtualenv pycon_web
(pycon_web) ~/2016-web $
```

The `(pycon_web)` prefix indicates that a virtual environment called "pycon_web" is being used. Next, check that you have the correct version of Python:

```
(pycon_web) ~/2016-web $ python --version
Python 2.7.12
(pycon_web) ~/2016-web $ pip --version
pip 8.0.2 from /Users/.../site-packages (python 2.7)
```

Install the project requirements:

```
(pycon_web) ~/2016-web $ pip install --upgrade -r requirements.txt
```

Run the project:

```
(pycon_web) ~/2016-web $ python manage.py runserver
```

This should start a webserver @ [127.0.0.1:5000](http://127.0.0.1:5000/en/).

The root directory will return a 404 error. You have to specify a language code (e.x. [127.0.0.1:5000/en/](http://127.0.0.1:5000/en/) or [127.0.0.1:5000/fr/](http://127.0.0.1:5000/fr/)).

## Deployment

```
fab <environment> deploy
```

Environments:

* `stag`
* `prod`
