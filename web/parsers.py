import re
import os
import urlparse
import shutil
from collections import namedtuple

import requests

from .config import Config
from .utils import markdown_to_text


class SymposionProposalsApi(object):
    URL = 'https://cfp.pycon.ca'
    RESOURCE = 'proposals'

    def __init__(self):
        self.token = os.environ.get('CFP_TOKEN', '')

    def get_url(self):
        return '{}/api/{}'.format(self.URL, self.RESOURCE)

    def get(self):
        r = requests.get(
            self.get_url(),
            headers={'Authorization': 'Token {}'.format(self.token)}
        )

        return r


class ProposalsInterface(object):

    def __init__(self):
        self.api_request = SymposionProposalsApi()
        self.data = None
        self.proposals = {}

    def _process_data(self):
        for proposal in self.data:
            self.proposals[proposal['id']] = proposal

    def fetch(self):
        self.data = self.api_request.get().json()
        self._process_data()

    def get_proposal_by_id(self, id):
        try:
            proposal = self.proposals[id]
        except KeyError:
            return None

        return proposal


class ScheduleInterface(object):
    KEYNOTE_ROOM = '1-067'

    _event_attrs = ['date', 'start_time', 'end_time']
    Talk = namedtuple('Talk', _event_attrs + ['talk_slug', 'room'])
    Keynote = namedtuple('Keynote', _event_attrs + ['title', 'content', 'room'])
    Event = namedtuple('Event', _event_attrs + ['title'])

    def __init__(self, schedule_json):
        self.schedule_json = schedule_json

        self.events = []
        self.rooms = {r['slug']: r['name'] for r in schedule_json['rooms']}

        for schedule_day in self.schedule_json['days']:
            date = schedule_day['date']
            for slot in schedule_day['entries']:
                if self._is_keynote_slot(slot):
                    keynote = self.Keynote(date=date,
                                           start_time=slot['start_time'],
                                           end_time=slot['end_time'],
                                           title=slot['title'],
                                           content=slot['content'],
                                           room=self.KEYNOTE_ROOM)
                    self.events.append(keynote)
                elif self._is_talks_slot(slot):
                    for room, talk_slug in slot['talks'].iteritems():
                        talk = self.Talk(date=date,
                                         start_time=slot['start_time'],
                                         end_time=slot['end_time'],
                                         talk_slug=talk_slug,
                                         room=room)
                        self.events.append(talk)
                else:
                    event = self.Event(date=date,
                                       start_time=slot['start_time'],
                                       end_time=slot['end_time'],
                                       title=slot['title'])
                    self.events.append(event)

        self.events = sorted(self.events, key=self._event_sort_key)

    @staticmethod
    def _event_sort_key(event):
        return event.date, event.start_time, event.end_time

    @staticmethod
    def _is_keynote_slot(slot):
        return 'title' in slot and 'keynote' in slot.get('title', '').lower() and 'content' in slot

    @staticmethod
    def _is_talks_slot(slot):
        return 'talks' in slot

    def get_agenda(self):
        return self.events

    def get_keynotes(self):
        events = [e for e in self.events if isinstance(e, self.Keynote)]

        return events

    def get_talks(self):
        events = [e for e in self.events if isinstance(e, self.Talk)]

        return events

    def get_miscellaneous(self):
        events = [e for e in self.events if isinstance(e, self.Event)]

        return events


class ScheduleParser(object):
    KEYNOTE_ROOM = '1-067'

    def __init__(self, schedule):
        self.schedule = schedule
        self.proposals = ProposalsInterface()
        self.proposals.fetch()

    @staticmethod
    def _is_keynote_slot(slot):
        return 'title' in slot and 'keynote' in slot.get('title', '').lower() and 'content' in slot

    @staticmethod
    def _is_talks_slot(slot):
        return 'talks' in slot

    @staticmethod
    def _agenda_item(id, topic, description, date, start_time, end_time, **optional_columns):

        return {
            'id': id,
            'topic': topic,
            'description': description,
            'tracks': optional_columns.get('tracks') or '',
            'date': date.strftime('%Y-%m-%d'),
            'start_time': start_time.strftime('%H:%M'),
            'end_time': end_time.strftime('%H:%M'),
            'location': optional_columns.get('location') or '',
            'speakers': optional_columns.get('speakers') or '',
            'attendees': optional_columns.get('attendees') or ''
        }

    def _get_talk(self, slug):
        try:
            talk_proposal_id = int(slug.split('-')[0])
        except (ValueError, KeyError):
            print("Proposal NOT found: ", slug)
            return None
        return self.proposals.get_proposal_by_id(talk_proposal_id)

    @property
    def agenda_data(self):
        data = []

        for e in self.schedule.get_agenda():
            if isinstance(e, self.schedule.Keynote):
                data.append(self._agenda_item(id="{:%d}-{:%H:%M}".format(e.date, e.start_time),
                                              topic=e.title,
                                              description=e.content,
                                              date=e.date,
                                              start_time=e.start_time,
                                              end_time=e.end_time,
                                              location=e.room))
            elif isinstance(e, self.schedule.Talk):
                talk_details = self._get_talk(e.talk_slug)
                if talk_details is None:
                    continue
                speakers = [talk_details['speaker']['id']]
                for additional_speaker in talk_details['additional_speakers']:
                    speakers.append(additional_speaker['id'])
                data.append(self._agenda_item(id=str(talk_details['id']),
                                              topic=talk_details['title'],
                                              description=talk_details['description'],
                                              date=e.date,
                                              start_time=e.start_time,
                                              end_time=e.end_time,
                                              location=e.room,
                                              speakers=','.join(map(str, speakers))))
            elif isinstance(e, self.schedule.Event):
                data.append(self._agenda_item(id="{:%d}-{:%H:%M}".format(e.date, e.start_time),
                                              topic=e.title,
                                              description=e.title,
                                              date=e.date,
                                              start_time=e.start_time,
                                              end_time=e.end_time))
            else:
                pass

        return data


class SpeakerPictureParser(object):
    IMG_DIR = Config.SPEAKER_IMG_DIR

    def __init__(self, speaker, no_cache=False):
        self.speaker = speaker
        url = speaker['photo']
        if not url:
            self.filename = ''
            return
        path = urlparse.urlparse(url).path
        ext = os.path.splitext(path)[1] or '.jpeg'  # assume it's a jpeg if no extension
        self.filename = '{}-{}{}'.format(speaker['id'],
                                          re.sub('[^\w]+', '-', speaker['name'].lower()),
                                          ext)
        file_path = os.path.join(self.IMG_DIR, self.filename)
        if not os.path.exists(self.IMG_DIR):
            os.makedirs(self.IMG_DIR)
        if os.path.isfile(file_path):
            if no_cache:
                os.remove(file_path)
            else:
                return
        image_file = requests.get(url, stream=True)
        with open(file_path, 'wb') as img_file:
            shutil.copyfileobj(image_file.raw, img_file)
        del image_file

    @property
    def name(self):
        return self.filename


class SpeakerParser(object):

    def __init__(self, schedule):
        self.schedule = schedule
        self.proposals = ProposalsInterface()
        self.proposals.fetch()

    @staticmethod
    def _twitter_url_from_username(uname):
        return 'https://twitter.com/{}'.format(uname) if uname else ''

    @staticmethod
    def _get_image(speaker):
        image_obj = SpeakerPictureParser(speaker)

        return image_obj.name

    def _speaker_item(self, speaker):

        return {
            'id': speaker['id'],
            'name': speaker['name'] or 'UNKNOWN',
            'title': '',
            'company_name': '',
            'description': markdown_to_text(speaker['biography']),
            'email': speaker['invite_email'] or speaker['email'],
            'website': '',
            'facebook': '',
            'twitter': self._twitter_url_from_username(speaker['twitter_username']),
            'linkedin': '',
            'picture': self._get_image(speaker),
            'self_edit_link': ''
        }

    def _get_talk(self, slug):
        try:
            talk_proposal_id = int(slug.split('-')[0])
        except (ValueError, KeyError):
            print("Proposal NOT found: ", slug)
            return None

        return self.proposals.get_proposal_by_id(talk_proposal_id)

    @staticmethod
    def _remove_duplicates(speakers):
        ids = set()
        unique_speakers = []
        for s in speakers:
            if s['id'] in ids:
                continue
            unique_speakers.append(s)
            ids.add(s['id'])

        return unique_speakers

    @property
    def speaker_data(self):
        talks = self.schedule.get_talks()
        talk_proposals = [self._get_talk(t.talk_slug) for t in talks]
        speakers = []
        for proposal in talk_proposals:
            if proposal is None:
                continue
            speakers.append(proposal['speaker'])
            for add_speaker in proposal.get('additional_speakers', []):
                speakers.append(add_speaker)

        speaker_items = [self._speaker_item(s) for s in speakers]
        speaker_items = self._remove_duplicates(speaker_items)

        return speaker_items
