import os
import json
import codecs

import markdown

from flask import current_app

def get_json_file(filename):
    filepath = os.path.join(current_app.config['APP_PATH'], 'data', filename)

    with open(filepath, 'r') as f:
        return json.loads(f.read())


def get_markdown_file(filename):
    filepath = os.path.join(current_app.config['APP_PATH'], 'markdown',
                            filename)

    with codecs.open(filepath, mode='r', encoding="utf-8") as f:
        return markdown.markdown(f.read())
