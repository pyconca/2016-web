import argparse
import codecs
import json
import os
import pprint
import re

def etl_md_to_json(src_dir, compiled_path):
    re_newline   = re.compile('\r?\n')
    re_delimiter = re.compile('^(?P<key>[^:]+)\s*:\s*(?P<value>.+)$')

    session_map = {}

    for name in os.listdir(src_dir):
        if name[0] == '.':
            continue

        with codecs.open(os.path.join(src_dir, name), 'r', 'utf-8') as f:
            sections = f.read().split('---')

            content = sections[1].strip()
            lines   = re_newline.split(content)
            alias   = name.split('.')[0]

            session_map[alias] = {}
            session            = session_map[alias]

            for line in lines:
                matches = re_delimiter.search(line).groupdict()
                key     = matches['key']
                value   = matches['value'].encode("ascii", "xmlcharrefreplace")

                session[key] = value

                if key == 'pk':
                    session[key] = int(value)

            session['md'] = sections[2].strip().encode("ascii", "xmlcharrefreplace")

    with codecs.open(compiled_path, 'w') as f:
        json.dump(session_map, f, indent = 2, sort_keys = True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src_dir')

    args    = parser.parse_args()
    src_dir = args.src_dir

    etl_md_to_json(src_dir, 'jsx/talks.json')
