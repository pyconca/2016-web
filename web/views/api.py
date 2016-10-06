from datetime import date

from flask import Blueprint, jsonify, send_file

from web.utils import get_data_file, get_markdown_file, schedule_to_xlsx

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


class ScheduleParser(object):

    def __init__(self, schedule):
        self.schedule = schedule

    @staticmethod
    def _is_keynote_slot(slot):
        return 'title' in slot and 'keynote' in slot.get('title', '').lower() and 'content' in slot

    @staticmethod
    def _is_talks_slot(slot):
        return 'talks' in slot

    def _agenda_item(self, id, topic, description, tracks, date, start_time, end_time, location, speakers='', attendees=''):

        return {
            'id': id,
            'topic': topic,
            'description': description,
            'tracks': tracks,
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
            'speakers': speakers,
            'attendees': attendees
        }

    def _get_talk(self, slug):
        return {
            'title': 'Talk title goes here'
        }

    @property
    def data(self):
        data = []

        for schedule_day in self.schedule['days']:
            date = schedule_day['date']
            for slot in schedule_day['entries']:
                start_time = slot['start_time']
                end_time = slot['end_time']
                if self._is_keynote_slot(slot):
                    agenda_item = self._agenda_item(
                        id=1,
                        topic=slot['title'],
                        description=slot['content'],
                        tracks='',
                        date=date,
                        start_time=start_time,
                        end_time=end_time,
                        location='',
                    )

                    data.append(agenda_item)
                elif self._is_talks_slot(slot):
                    for room, talk in slot['talks'].iteritems():
                        talk_details = self._get_talk(talk)

                        agenda_item = self._agenda_item(
                            id=1,
                            topic=talk_details['title'],
                            description='',
                            tracks='',
                            date=date,
                            start_time=start_time,
                            end_time=end_time,
                            location=room,
                        )

                        data.append(agenda_item)
                else:
                    agenda_item = self._agenda_item(
                        id=1,
                        topic=slot['title'],
                        description='',
                        tracks='',
                        date=date,
                        start_time=start_time,
                        end_time=end_time,
                        location='',
                    )

                    data.append(agenda_item)

        def key_sort(item):
            return (item['date'], item['start_time'])

        data = sorted(data, key=key_sort)

        def stringify(item):
            item['date'] = item['date'].strftime('%Y-%m-%d')
            item['start_time'] = item['start_time'].strftime('%H:%M')
            item['end_time'] = item['end_time'].strftime('%H:%M')
            return item

        data = [stringify(item) for item in data]

        return data


@api.route('/exports/agenda.json')
def agenda_json():
    schedule = get_data_file('schedule.json')
    # print(schedule)
    print(type(schedule))
    serializer = ScheduleParser(schedule)
    data = serializer.data
    print(data)

    return jsonify(data)


@api.route('/exports/agenda')  # for some mysterious reason 'agenda.xlsx' screws up the download and return empty file!
def agenda_xlsx():
    schedule = get_data_file('schedule.json')
    serializer = ScheduleParser(schedule)
    data = serializer.data
    xlsx_file = schedule_to_xlsx(data)

    return send_file(xlsx_file,
                     as_attachment=True,
                     attachment_filename='agenda.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                     )
