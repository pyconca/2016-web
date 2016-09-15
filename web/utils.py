import os
import json
import codecs

import yaml
import markdown

from flask import current_app


def get_data_file(filename):
    """
    Get the contents of a data file.
    """

    filepath = os.path.join(current_app.config['APP_PATH'], 'data', filename)

    with open(filepath, 'r') as f:
        if filename.endswith('.json'):
            return json.loads(f.read())

        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            return yaml.load(f.read())


def get_markdown_file(name, lang='en'):
    """
    Get the contents of a markdown file.
    """

    filename_temp = "{0}_{1}.markdown"

    md_dir = os.path.join(current_app.config['APP_PATH'], 'markdown')

    filepath = os.path.join(md_dir, filename_temp.format(name, lang))

    if not os.path.isfile(filepath) and lang == 'fr':
        filepath = os.path.join(md_dir, filename_temp.format(name, 'en'))

    if not os.path.isfile(filepath):
        return None

    with codecs.open(filepath, mode='r', encoding="utf-8") as f:
        return markdown.markdown(f.read())
