from datetime import date

from flask import Blueprint, jsonify, send_file

from web.utils import get_data_file, get_markdown_file, schedule_to_xlsx, speakers_to_xlsx
from web.parsers import ScheduleParser

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


@api.route('/exports/agenda.json')
def agenda_json():
    schedule = get_data_file('schedule.json')
    # print(schedule)
    print(type(schedule))
    serializer = ScheduleParser(schedule)
    data = serializer.agenda_data
    print(data)

    return jsonify(data)


@api.route('/exports/agenda')  # for some mysterious reason 'agenda.xlsx' screws up the download and return empty file!
def agenda_xlsx():
    schedule = get_data_file('schedule.json')
    serializer = ScheduleParser(schedule)
    data = serializer.agenda_data
    xlsx_file = schedule_to_xlsx(data)

    return send_file(xlsx_file,
                     as_attachment=True,
                     attachment_filename='agenda.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                     )



@api.route('/exports/speakers')  # for some mysterious reason 'agenda.xlsx' screws up the download and return empty file!
def speakers_xlsx():
    schedule = get_data_file('schedule.json')
    serializer = ScheduleParser(schedule)
    data = serializer.speaker_data
    xlsx_file = speakers_to_xlsx(data)

    return send_file(xlsx_file,
                     as_attachment=True,
                     attachment_filename='speakers.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                     )
