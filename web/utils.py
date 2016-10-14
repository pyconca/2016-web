import os
import json
import codecs
import datetime

import yaml
import markdown

from flask import current_app


class CustomJSONDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook,
                                  *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict):
            for key in obj:
                if key.endswith('time'):
                    obj[key] = datetime.datetime.strptime(obj[key],
                                                          '%H:%M:%S').time()

                if key.endswith('date'):
                    obj[key] = datetime.datetime.strptime(obj[key],
                                                          '%Y-%m-%d').date()

        return obj


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, datetime.time):
            return obj.isoformat()


def get_data_file(filename):
    """
    Get the contents of a data file.
    """

    filepath = os.path.join(current_app.config['APP_PATH'], 'data', filename)

    with open(filepath, 'r') as f:
        if filename.endswith('.json'):
            return json.loads(f.read(), cls=CustomJSONDecoder)

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
        return None, {}

    md = markdown.Markdown(['markdown.extensions.meta'])

    with codecs.open(filepath, mode='r', encoding="utf-8") as f:
        html = md.convert(f.read())

    md.Meta['github_link'] = ('https://github.com/pyconca/2016-web/blob/'
                              'master/web/markdown/{0}').format(filename_temp)

    return html, md.Meta
