from datetime import date

from flask import Blueprint, jsonify, url_for

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
        },
        'routes': [
            url_for('schedule.talk_json', slug='schedule.json', lang='en'),
            url_for('schedule.talk_json', slug='schedule.json', lang='fr'),
            '/en/schedule/<talk-slug>.json',
            '/fr/schedule/<talk-slug>.json',
        ]
    })
