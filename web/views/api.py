from datetime import date

from flask import Blueprint, jsonify

from web.utils import get_data_file, get_markdown_file

api = Blueprint('api', __name__)


@api.route('/index.json')
def index():
    return jsonify({
        'name': 'PyCon Canada 2016',
        'conference': {
            'start_date': date(2016, 11, 12),
            'end_date': date(2016, 11, 13)
        },
        'sprints': {
            'start_date': date(2016, 11, 14),
            'end_date': date(2016, 11, 15)
        },
        'location': {
            'name': 'Ted Rogers School of Business',
            'address': {
                'street': '55 Dundas Street West',
                'city': 'Toronto',
                'province': 'Ontario',
                'country': 'Canada',
                'postal_code': 'M5G 2C3',
                'geo': {
                    'latitude': '43.65543',
                    'longitude': '-79.38310'
                }
            }
        }
    })


@api.route('/schedule.json')
def schedule():
    schedule = get_data_file('schedule.json')

    

    return jsonify(schedule)


@api.route('/schedule/<string:slug>.json')
def talk_json(slug):
    description, content = get_markdown_file('talks/{}'.format(slug), 'en')
    content['description'] = description
    return jsonify(content)
