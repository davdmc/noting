from PyQt5 import QtCore, QtGui, QtWidgets
from os import listdir, path
import json
from datetime import date
from note import Note 

class NotingModel(QtCore.QAbstractListModel):
    # TODO: Create enums for note status and session status: (saved/notSaved)
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
        """If there is a session with the same path open it. Otherwise, create a new one and populate it."""
        self.resetSession()

        if path.isfile(self._sessionPath):
            with open(self._sessionPath) as json_file:
                data = json.load(json_file)
                self._parseJson(data)
                return True
        else:
            self._createSession()

        self.isActiveSession = True

    def resetSession(self):
        """Reset the data of the session in case of a later init"""

        self.isActiveSession = False
        self.sessionInfo = {}

        self.currentNote = None
        self.currentIndex = None
        
        self.beginResetModel()
        self._notes = []
        self.endResetModel()

    def getNotes(self):
        return self._notes
        
    def _createSession(self):
        """Create a new session and populate it with its name and todays date."""
        with open(path.join(self._sessionPath), 'w') as json_file:
            self.sessionInfo['name'] = path.splitext(
                path.split(self._sessionPath)[-1])[0]
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
        colorDict = {'note': QtGui.QColor('#8BC34A'), 'question': QtGui.QColor(
            '#FF5722'), 'task': QtGui.QColor('#FFEB3B')}

        if role == QtCore.Qt.BackgroundRole:
            return QtGui.QBrush(colorDict[self._notes[index.row()].noteType])
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
        # Used this method as is the abstract model implementation.
        currentLen = self.rowCount(0)
        # This recieves: index of model, from and to.
        self.beginInsertRows(self.index(0), currentLen - 1, currentLen)
        self._notes.insert(currentLen, self.currentNote)
        self.endInsertRows()
        self.currentIndex = self.index(currentLen)
        # return self.currentIndex

    def swapNote(self, direction):
        """Move the note one up or down."""
        intIndex = self.currentIndex.row()
        if direction == 'up' and intIndex > 0:
            self.beginMoveRows(self.index(0), intIndex,
                               intIndex, self.index(0), intIndex - 1)
            self._notes[intIndex], self._notes[intIndex -
                                               1] = self._notes[intIndex - 1], self._notes[intIndex]
            self.endMoveRows()
            self.currentIndex = self.index(intIndex - 1)
        
        # This is counter intuitive due to a bug in moving the rows up in the list.
        elif direction == 'down' and intIndex < self.rowCount(0) - 1:
            
            self.beginMoveRows(self.index(0), intIndex + 1,
                               intIndex + 1, self.index(0), intIndex)
            self._notes[intIndex], self._notes[intIndex +
                                               1] = self._notes[intIndex + 1], self._notes[intIndex]
            
            self.endMoveRows()
            self.currentIndex = self.index(intIndex + 1)


    def saveNoteText(self, noteText):
        """Save the text on the current note."""
        self.currentNote.text = noteText
        self._notes[self.currentIndex.row()] = self.currentNote