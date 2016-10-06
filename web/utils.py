import os
import json
import codecs
import StringIO

import yaml
import markdown
import datetime
import xlsxwriter

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

    return html, md.Meta


def schedule_to_xlsx(data):
    output = StringIO.StringIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    for row, item in enumerate(data):
        worksheet.write(row, 0, item['id'])
        worksheet.write(row, 1, item['topic'])
        worksheet.write(row, 2, item['description'])
        worksheet.write(row, 3, item['tracks'])
        worksheet.write(row, 4, item['date'])
        worksheet.write(row, 5, item['start_time'])
        worksheet.write(row, 6, item['end_time'])
        worksheet.write(row, 7, item['location'])
        worksheet.write(row, 8, item['speakers'])
        worksheet.write(row, 9, item['attendees'])
    workbook.close()

    output.seek(0)
    return output
