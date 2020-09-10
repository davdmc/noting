import markdown
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from os import path
from note import Note


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

        font_config = FontConfiguration()
        
        html = markdown.markdown(text)
        css = CSS(filename=path.join(self.appPath, 'style.css'), font_config=font_config)
        HTML(string=html).write_pdf(self.exportPath, stylesheets=[css], font_config=font_config)

    def _unifyTextUnordered(self):

        document = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="style.css"><title>Document</title></head><body>\n'
        document = document + '<h1 class="session-name">{}</h1>\n'.format(self.title) + '<p class="date">{}</p>\n'.format(
            self.date) + '<p class="author">{}</p>\n\n'.format(self.author)

        for note in self.notes:
            document = document + '## ' + note.name + '\n\nType: _' + \
                note.noteType.capitalize() + '_\n\n' + note.text + '\n\n'

        document = document + '</body></html>'
        return document

    def _unifyTextOrdered(self):

        document = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="style.css"><title>Document</title></head><body>\n'
        document = document + '<h1 class="webtitle">{}</h1>\n'.format(self.title) + '<p class="date">{}</p>\n'.format(
            self.date) + '<p class="author">{}</p>\n\n'.format(self.author)

        noteTypes = ['note', 'question', 'task']
        
        for noteType in noteTypes:
            for note in self.notes:
                if note.noteType == noteType:
                    document = document + '## ' + note.name + '\n\nType: _' + \
                    note.noteType.capitalize() + '_\n\n' + note.text + '\n\n'

        document = document + '</body></html>'
        return document
