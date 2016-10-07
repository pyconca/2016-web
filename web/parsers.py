import requests


class SymposionPropsalsApi(object):
    URL = 'https://cfp.pycon.ca'
    RESOURCE = 'proposals'

    def __init__(self):
        self.token = ''

    def get_url(self):
        return '{}/api/{}'.format(self.URL, self.RESOURCE)

    def get(self):
        r = requests.get(
            self.get_url(),
            headers={'Authorization': 'Token {}'.format(self.token)}
        )

        return r


class ProposalParser(object):

    def __init__(self):
        self.api_request = SymposionPropsalsApi()
        self.data = None
        self.proposals = {}
        self.speakers = []

    def _process_data(self):
        for proposal in self.data:
            self.proposals[proposal['id']] = proposal

    def _add_speaker(self, speaker):
        self.speakers.append(speaker)  # TODO: remove duplicates

    def fetch(self):
        self.data = self.api_request.get().json()
        self._process_data()

    def get_proposal_by_id(self, id):
        try:
            proposal = self.proposals[id]
        except KeyError:
            return None
        self._add_speaker(proposal['speaker'])
        for additional_speaker in proposal['additional_speakers']:
            self._add_speaker(additional_speaker)

        return proposal

    def get_speakers(self):
        # IMPORTANT: api returns all the speakers, so don't be tempted to grab all of them (from `self.data`).
        # Only accepted speakers (and additional speakers) should be consumed.
        return list(self.speakers)


class ScheduleParser(object):
    KEYNOTE_ROOM = '1-067'

    def __init__(self, schedule):
        self.schedule = schedule
        self.proposals = ProposalParser()
        self.proposals.fetch()

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

    def _speaker_item(self, speaker):

        return {
            'id': speaker['id'],
            'name': speaker['name'],
            'title': '',
            'company_name': '',
            'description': speaker['biography'],
            'email': '',
            'website': '',
            'facebook': '',
            'twitter': speaker['twitter_username'],
            'linkedin': '',
            'picture': speaker['photo'],
            'self_edit_link': ''
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

        for schedule_day in self.schedule['days']:
            date = schedule_day['date']
            for slot in schedule_day['entries']:
                start_time = slot['start_time']
                end_time = slot['end_time']
                if self._is_keynote_slot(slot):
                    # TODO: figure out a way to grab info
                    agenda_item = self._agenda_item(
                        id=1,
                        topic=slot['title'],
                        description=slot['content'],
                        tracks='',
                        date=date,
                        start_time=start_time,
                        end_time=end_time,
                        location=self.KEYNOTE_ROOM,
                    )

                    data.append(agenda_item)
                elif self._is_talks_slot(slot):
                    for room, talk in slot['talks'].iteritems():
                        talk_details = self._get_talk(talk)
                        if talk_details is None:
                            continue
                        speakers = [talk_details['speaker']['id']]
                        for additional_speaker in talk_details['additional_speakers']:
                            speakers.append(additional_speaker['id'])

                        agenda_item = self._agenda_item(
                            id=str(talk_details['id']),
                            topic=talk_details['title'],
                            description=talk_details['description'],
                            tracks='',
                            date=date,
                            start_time=start_time,
                            end_time=end_time,
                            location=room,
                            speakers=','.join(map(str, speakers))
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

    @property
    def speaker_data(self):
        self.agenda_data
        speakers = self.proposals.get_speakers()

        return [self._speaker_item(s) for s in speakers]
