import argparse
import codecs
import json
import os
import pprint
import re

re_newline   = re.compile('\r?\n')
re_delimiter = re.compile('^(?P<key>[^:]+)\s*:\s*(?P<value>.+)$')

parser = argparse.ArgumentParser()
parser.add_argument('src_dir')

args    = parser.parse_args()
src_dir = args.src_dir

metadata_map = {}

for name in os.listdir(src_dir):
    if name[0] == '.':
        continue

    with codecs.open(os.path.join(src_dir, name), 'r', 'utf-8') as f:
        content = f.read().split('---')[1].strip()
        lines   = re_newline.split(content)
        alias   = name.split('.')[0]

        metadata_map[alias] = {}
        metadata            = metadata_map[alias]

        for line in lines:
            matches = re_delimiter.search(line).groupdict()
            key     = matches['key']
            value   = matches['value']

            metadata[key] = value

            if key == 'pk':
                metadata[key] = int(value)

with codecs.open('jsx/talks.json', 'w') as f:
    json.dump(metadata_map, f)
