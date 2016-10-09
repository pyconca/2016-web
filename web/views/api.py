from datetime import date

from flask import Blueprint, jsonify, send_file

from web.utils import get_data_file, get_markdown_file, schedule_to_xlsx, speakers_to_xlsx, get_speaker_pictures_archive
from web.parsers import ScheduleParser, ScheduleInterface, SpeakerParser

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
    schedule_json = get_data_file('schedule.json')
    interface = ScheduleInterface(schedule_json)
    serializer = ScheduleParser(interface)
    data = serializer.agenda_data

    return jsonify(data)


@api.route('/exports/agenda')  # for some mysterious reason 'agenda.xlsx' screws up the download and return empty file!
def agenda_xlsx():
    schedule_json = get_data_file('schedule.json')
    interface = ScheduleInterface(schedule_json)
    serializer = ScheduleParser(interface)
    data = serializer.agenda_data
    xlsx_file = schedule_to_xlsx(data)

    return send_file(xlsx_file,
                     as_attachment=True,
                     attachment_filename='agenda.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                     )


@api.route('/exports/speakers.json')
def speakers_json():
    schedule_json = get_data_file('schedule.json')
    interface = ScheduleInterface(schedule_json)
    serializer = SpeakerParser(interface)
    data = serializer.speaker_data

    return jsonify(data)


@api.route('/exports/speakers')
def speakers_xlsx():
    schedule_json = get_data_file('schedule.json')
    interface = ScheduleInterface(schedule_json)
    serializer = SpeakerParser(interface)
    data = serializer.speaker_data
    xlsx_file = speakers_to_xlsx(data)

    return send_file(xlsx_file,
                     as_attachment=True,
                     attachment_filename='speakers.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                     )


@api.route('/exports/speaker_pictures')
def speakers_pictures_zip():
    archive = get_speaker_pictures_archive()

    return send_file(archive,
                     as_attachment=True,
                     attachment_filename='speakers_pictures.zip',
                     mimetype='application/zip'
                     )
