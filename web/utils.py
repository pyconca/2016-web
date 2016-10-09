import os
import json
import codecs
import StringIO
import zipfile
from collections import OrderedDict

import yaml
import markdown
import datetime
import xlsxwriter
from bs4 import BeautifulSoup
from markdown import markdown

from flask import current_app
from .config import Config


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


def markdown_to_text(markdown_text):
    html = markdown(markdown_text)
    text = ''.join(BeautifulSoup(html, "html.parser").findAll(text=True))

    return text


def clean_xlsx_value(value):
    if isinstance(value, (str, unicode)):
        # Excel uses '\n' for linebreaks. See https://github.com/jmcnamara/excel-writer-xlsx/issues/86
        value = "\n".join(value.splitlines())
    return value

AGENDA_FIELDS = OrderedDict([
    ('id', u'ID*'),
    ('topic', u'Topic*'),
    ('description', u'Description*'),
    ('tracks', u'Track'),
    ('date', u'Date (yyyy-mm-dd)*'),
    ('start_time', u'Start Time (hh:mm)*'),
    ('end_time', u'End Time (hh:mm)*'),
    ('location', u'Location'),
    ('speakers', u'Speakers'),
    ('attendees', u'Attendees')
])


def schedule_to_xlsx(data):
    output = StringIO.StringIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})

    for col, header in enumerate(AGENDA_FIELDS.values()):
        worksheet.write(0, col, header, bold)

    for row, item in enumerate(data, start=1):
        for col, field in enumerate(AGENDA_FIELDS.keys()):
            worksheet.write(row, col, clean_xlsx_value(item[field]))

    workbook.close()
    output.seek(0)

    return output

SPEAKER_FIELDS = OrderedDict([
    ('id', u'ID*'),
    ('name', u'Name*'),
    ('title', u'Title'),
    ('company_name', u'Company Name'),
    ('description', u'Description'),
    ('email', u'Email'),
    ('website', u'Website'),
    ('facebook', u'Facebook'),
    ('twitter', u'Twitter'),
    ('linkedin', u'LinkedIn'),
    ('picture', u'Picture'),
    ('self_edit_link', u'Self Edit Link'),
])


def speakers_to_xlsx(data):
    output = StringIO.StringIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})

    for col, header in enumerate(SPEAKER_FIELDS.values()):
        worksheet.write(0, col, header, bold)

    for row, item in enumerate(data, start=1):
        for col, field in enumerate(SPEAKER_FIELDS.keys()):
            worksheet.write(row, col, clean_xlsx_value(item[field]))

    workbook.close()
    output.seek(0)

    return output


def get_speaker_pictures_archive():
    output = StringIO.StringIO()

    def zipdir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

    zipf = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
    zipdir(Config.SPEAKER_IMG_DIR, zipf)
    zipf.close()
    output.seek(0)

    return output
