import os
import json
import codecs

import markdown

from flask import current_app


def get_json_file(filename, lang='en'):
    filepath = os.path.join(current_app.config['APP_PATH'], 'data', filename)

    with open(filepath, 'r') as f:
        return json.loads(f.read())


def get_markdown_file(name, lang='en'):
    filename_temp = "{0}_{1}.markdown"

    md_dir = os.path.join(current_app.config['APP_PATH'], 'markdown')

    filepath = os.path.join(md_dir, filename_temp.format(name, lang))

    if not os.path.isfile(filepath) and lang == 'fr':
        filepath = os.path.join(md_dir, filename_temp.format(name, 'en'))

    if not os.path.isfile(filepath):
        return None

    with codecs.open(filepath, mode='r', encoding="utf-8") as f:
        return markdown.markdown(f.read())
