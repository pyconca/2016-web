#!/usr/bin/env python3

import json
from collections import OrderedDict

def name_last_first_sortkey(v):
    first, *middle, last = v['name'].split()
    return (last, first, middle)

if __name__ == '__main__':
    with open('team.json', 'r') as fobj:
        data = json.load(fobj, object_pairs_hook=OrderedDict)

    for k in [ 'organisers', 'volunteers' ]:
        data[k].sort(key=name_last_first_sortkey)

    with open('team.json', 'w') as fobj:
        json.dump(data, fobj, indent=4)
        fobj.write("\n")
