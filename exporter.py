from pdfExporter import PDFExporter
from note import Note
from pathlib import Path
from os import path

class Exporter:

    def export_pdf(self, appPath, path, sessionInfo, notes, ordered=False):

        exp = PDFExporter(appPath, path, sessionInfo, notes)
        
        exp.extract(ordered)

if __name__ == "__main__":
    note = Note('Note 1', 'note', 'This is the example note. \n\n# Title \n\n Prepare to write a lot.')
    exp = Exporter()
    exp.export_pdf('.', {'name':'Session1','date':'10-9-2020'}, [note])

