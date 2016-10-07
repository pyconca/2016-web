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
    bold = workbook.add_format({'bold': 1})

    worksheet.write('A1', 'ID*', bold)
    worksheet.write('B1', 'Topic*', bold)
    worksheet.write('C1', 'Description*', bold)
    worksheet.write('D1', 'Track', bold)
    worksheet.write('E1', 'Date (yyyy-mm-dd)*', bold)
    worksheet.write('F1', 'Start Time (hh:mm)*', bold)
    worksheet.write('G1', 'End Time (hh:mm)*', bold)
    worksheet.write('H1', 'Location', bold)
    worksheet.write('I1', 'Speakers', bold)
    worksheet.write('J1', 'Attendees', bold)
    for row, item in enumerate(data, start=1):
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


def speakers_to_xlsx(data):
    output = StringIO.StringIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})

    worksheet.write('A1', 'ID*', bold)
    worksheet.write('B1', 'Name*', bold)
    worksheet.write('C1', 'Title*', bold)
    worksheet.write('D1', 'Company Name', bold)
    worksheet.write('E1', 'Description', bold)
    worksheet.write('F1', 'Email', bold)
    worksheet.write('G1', 'Website', bold)
    worksheet.write('H1', 'Facebook', bold)
    worksheet.write('I1', 'Twitter', bold)
    worksheet.write('J1', 'LinkedIn', bold)
    worksheet.write('K1', 'Picture', bold)
    worksheet.write('L1', 'Self Edit Link', bold)
    for row, item in enumerate(data, start=1):
        worksheet.write(row, 0, item['id'])
        worksheet.write(row, 1, item['name'])
        worksheet.write(row, 2, item['title'])
        worksheet.write(row, 3, item['company_name'])
        worksheet.write(row, 4, item['description'])
        worksheet.write(row, 5, item['email'])
        worksheet.write(row, 6, item['website'])
        worksheet.write(row, 7, item['facebook'])
        worksheet.write(row, 8, item['twitter'])
        worksheet.write(row, 9, item['linkedin'])
        worksheet.write(row, 10, item['picture'])
        worksheet.write(row, 11, item['self_edit_link'])
    workbook.close()

    output.seek(0)
    return output
