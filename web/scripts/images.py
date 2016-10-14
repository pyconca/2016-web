from glob import glob
from os.path import join, basename

from flask import current_app, render_template

from flask_script import Command

from cairosvg import svg2png

from web.utils import get_markdown_file


class TalkCards(Command):

    def generate_svg(self, slug):
        content, meta = get_markdown_file('talks/{}'.format(slug), lang='en')

        svg = render_template('cards/talk.svg', meta=meta, content=content)

        filename = join(current_app.config['STATIC_PATH'], 'images', 'cards',
                        '{}.svg')

        with open(filename.format(slug), 'wb') as fobj:
            fobj.write(svg.encode('utf8'))

    def convert_svg_to_png(self):
        svg_files = glob(join(current_app.config['STATIC_PATH'], 'images',
                              'cards', '*.svg'))

        for svg_file in svg_files:
            png_file = svg_file.replace('.svg', '.png')
            svg2png(url=svg_file, write_to=png_file)

    def run(self):
        talk_files = glob(join(current_app.config['APP_PATH'], 'markdown',
                               'talks', '*.markdown'))

        for talk_file in talk_files:
            slug = basename(talk_file).split('_en.markdown')[0]
            self.generate_svg(slug)

        self.convert_svg_to_png()
