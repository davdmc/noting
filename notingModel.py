from PyQt5 import QtCore, QtGui, QtWidgets
from os import listdir, path
import json
from datetime import date


class NotingModel(QtCore.QAbstractListModel):

    def __init__(self, *args, **kwargs):
        super(NotingModel, self).__init__(*args, **kwargs)
        self._sessionPath = ""
        self.isActiveSession = False
        self.sessionInfo = {}

        self.currentNote = None
        self.currentIndex = None

        self._notes = []

    def setSessionPath(self, sessionPath):
        self._sessionPath = sessionPath

    def initSession(self):
        if path.isfile(self._sessionPath):
            with open(self._sessionPath) as json_file:
                data = json.load(json_file)
                self._parseJson(data)
                return True
        else:
            self._createSession()

        self.isActiveSession = True

    def _createSession(self):
        """Create a new session and populate it with its name and todays date."""
        with open(path.join(self._sessionPath), 'w') as json_file:
            self.sessionInfo['name'] = path.splitext(path.split(self._sessionPath)[-1])[0]
            self.sessionInfo['date'] = date.today().strftime("%Y-%m-%d")
            initData = {'name': self.sessionInfo['name'],
                        'date': self.sessionInfo['date'], 'contents': []}
            json.dump(initData, json_file)

    def _parseJson(self, data):
        """Parse the data from the session JSON."""
        self.sessionInfo['name'] = data['name']
        self.sessionInfo['date'] = data['date']

        for content in data['contents']:
            name = content['name']
            noteType = content['noteType']
            text = content['text']
            note = Note(name, noteType, text)

            self._notes.append(note)

    def saveSession(self):
        """Save session in a JSON file."""
        with open(self._sessionPath, 'w') as f:
            json.dump(self._parseSession(), f)

    def _parseSession(self):
        """Parse the current data to a JSON file."""
        noteObject = [note.toObject() for note in self._notes]
        objectJson = {
            'name': self.sessionInfo['name'],
            'date': self.sessionInfo['date'],
            'contents': noteObject
        }
        return objectJson

    def rowCount(self, index):
        """Returns the number of rows under the given parent. 
        When the parent is valid it means that rowCount is 
        returning the number of children of parent."""
        return len(self._notes)

    def data(self, index, role):
        """Returns the data stored under the given role for 
        the item referred to by the index."""
        if role == QtCore.Qt.DisplayRole:
            return self._notes[index.row()].name

    def openNote(self, index):
        """Make the note under the given index the current note and returns it."""
        self.currentNote = self._notes[index.row()]
        self.currentIndex = index
        return self.currentNote

    def addNote(self, note):
        """Add a new note and make it current note."""
        self.currentNote = note
        index_tmp = self.index(self.rowCount(0) - 1)
        self.beginInsertRows(index_tmp, index_tmp.row(), index_tmp.row() + 1)
        self._notes.insert(index_tmp.row() + 1, self.currentNote)
        self.endInsertRows()
        self.currentIndex = self.index(self.rowCount(0) - 1)
        #return self.currentIndex

    def saveNoteText(self, noteText):
        """Save the text on the current note."""
        self.currentNote.text = noteText
        self._notes[self.currentIndex.row()] = self.currentNote


class Note:

    def __init__(self, name, noteType, text):

        self.name = name

        self.text = text

        self.noteType = noteType

        # self.creationDate

        # self.modifyDate

    def toObject(self):
        return {'name': self.name,
                'noteType': self.noteType,
                'text': self.text}
