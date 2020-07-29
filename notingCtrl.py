from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
from notingModel import Note

class NotingCtrl:

    def __init__(self, model, view, path):
        
        self._view = view
        self._model = model
        self._path = path

        self._initSession()

        self._view.listDir.setModel(self._model)
        self._connectSignals()
    
    def _initSession(self):
        """Function to initialize the session opening or creating a new one."""

        # Choose if you want to open or create a new session.
        method = self._view.selectSessionDialog()

        if method == "open":
            # Return the session path from a file selector.
            self.sessionPath = self._view.openSessionDialog()
        else:
            # Ask for the name of the session.
            sessionName = self._view.nameNewSessionForm()
            self.sessionPath = path.join(self._path, sessionName)
        
        self._model.setSessionPath(self.sessionPath)
        self._model.initSession()
        
    def _connectSignals(self):
        self._view.listDir.doubleClicked.connect(self.openNote)
        self._view.createNoteShortcut.activated.connect(self.createNote)
        self._view.saveNoteShortcut.activated.connect(self.saveNoteText)

    def openNote(self, idx):
        note = self._model.openNote(idx)
        self._view.textEdit.setText(note.text)

    def createNote(self):
        print("Enters create")
        noteName = self._view.newNoteForm()
        noteType = 'note'
        self._view.textEdit.setText('')
        newNote = Note(noteName, noteType, '')
        currentIndex = self._model.addNote(newNote)

    def saveNoteText(self):
        print("Enters save")
        noteText = self._view.textEdit.toMarkdown()
        self._model.saveNoteText(noteText)

    def updateList(self, index):
        print('Enter')
        self._view.listDir.repaint()
        print(self._model._notes)


