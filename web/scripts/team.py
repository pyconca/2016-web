import json
from collections import OrderedDict

from flask_script import Command


class AlphabetizeTeam(Command):
    """
    Alphabetize the team.json file.
    """

    def name_last_first_sortkey(self, v):
        full_name = v['name'].split()
        first = full_name[0]
        last = full_name[-1]
        middle = ' '.join(full_name[1:-1])
        return (last, first, middle)

    def run(self):
        with open('web/data/team.json', 'r') as fobj:
            data = json.loads(fobj.read(), object_pairs_hook=OrderedDict)

        for k in ['organisers', 'volunteers']:
            data[k].sort(key=self.name_last_first_sortkey)

        with open('web/data/team.json', 'w') as fobj:
            json.dump(data, fobj, indent=4)
            fobj.write('\n')
