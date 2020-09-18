import markdown
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from os import path
from note import Note
import markdown_katex


class PDFExporter:
    def __init__(self, appPath, exportPath, sessionInfo, notes):
        self.appPath = appPath
        self.exportPath = exportPath
        self.sessionInfo = sessionInfo
        self.notes = notes

        self.title = sessionInfo['name']
        self.date = sessionInfo['date']

        self.author = 'David Morilla Cabello'

    def extract(self, ordered):

        if ordered:
            text = self._unifyTextOrdered()
        else:
            text = self._unifyTextUnordered()

        first_page = '<h1 class="session-name">{}</h1>\n'.format(self.title) + '<p class="date">{}</p>\n'.format(
            self.date) + '<p class="author">{}</p>\n\n'.format(self.author)

        font_config = FontConfiguration()
        html = markdown.markdown(text, extensions=['markdown_katex', ], extension_configs={
            'markdown_katex': {
                'no_inline_svg': True,      # fix for WeasyPrint
                'insert_fonts_css': False,
            },
        })

        html = first_page + html
        css = CSS(filename=path.join(self.appPath, 'style.css'),
                  font_config=font_config)
        katexCss = CSS(filename=path.join(self.appPath,
                                          'katex.min.css'), font_config=font_config)
        HTML(string=html).write_pdf(
            self.exportPath, stylesheets=[katexCss, css], font_config=font_config)

    def _unifyTextUnordered(self):

        document = ''

        for note in self.notes:
            document = document + '## ' + note.name + '\n\nType: _' + \
                note.noteType.capitalize() + '_\n\n' + note.text + '\n\n'

        return document

    def _unifyTextOrdered(self):

        document = ''

        noteTypes = ['note', 'question', 'task']

        for noteType in noteTypes:
            for note in self.notes:
                if note.noteType == noteType:
                    document = document + '## ' + note.name + '\n\nType: _' + \
                        note.noteType.capitalize() + '_\n\n' + note.text + '\n\n'

        return document
