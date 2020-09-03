from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
from notingModel import Note
from pathlib import Path

class NotingCtrl:

    def __init__(self, model, view, defaultPath):

        self._view = view
        self._model = model
        self._path = defaultPath
        
        appPath = path.join(str(Path(__file__).parent.absolute()), "NotingLogo.ico")
        self._view.setWindowIcon(QtGui.QIcon(appPath))
        # Choose if you want to open or create a new session.
        method = self._view.selectSessionDialog()

        self._initSession(method)

        self._view.listNotes.setModel(self._model)
        self._connectSignals()

    def _initSession(self, method):
        """Function to initialize the session opening or creating a new one."""

        if method == "open":
            self._openSession()
        elif method == "new":
            self._newSession()

        self._model.setSessionPath(self.sessionPath)
        self._model.initSession()

        #Disables the textEdit and move buttons until a note is created or opened.
        self._view.textEdit.setDisabled(True)
        self._view.textEdit.clear()
        self._view.upButton.setDisabled(True)
        self._view.downButton.setDisabled(True)
        self._view.infoText.setText('Session name: {}\nNo openned note'.format(
            self._model.sessionInfo['name']))

    def _openSession(self):
        # Return the session path from a file selector.
        self.sessionPath = self._view.openSessionDialog()

    def _newSession(self):
        # Ask for the name of the session.
        sessionName = self._view.nameNewSessionForm()
        if not path.splitext(sessionName)[-1] == '.json':
            sessionName = sessionName + '.json'
        self.sessionPath = path.join(self._path, sessionName)
        
    def _connectSignals(self):
        """Manage the signal connection with controller methods."""
        
        # Data list 
        self._view.listNotes.doubleClicked.connect(self.openNote)
        self._view.returnKeyPressed.connect(self.openNote)

        # Up/down buttons
        self._view.upButton.clicked.connect(lambda: self.moveNote('up'))
        self._view.downButton.clicked.connect(lambda: self.moveNote('down'))

        # Create notes shortcuts
        self._view.createNoteShortcut.activated.connect(lambda: self.createNote('note'))
        self._view.createQuestionShortcut.activated.connect(lambda: self.createNote('question'))
        self._view.createTaskShortcut.activated.connect(lambda: self.createNote('task'))

        # Menu Bar connections
        self._view.newSession.triggered.connect(lambda: self._initSession("new"))
        self._view.openSession.triggered.connect(lambda: self._initSession("open"))
        self._view.saveSession.triggered.connect(self.saveSession)
        self._view.saveSession.setShortcut(self._view.saveSessionShortcut)
        
        # Management
        self._view.saveNoteShortcut.activated.connect(self.saveNoteText)
        self._view.focusListShortcut.activated.connect(self.focusList)

    def openNote(self, idx):
        """Open a note when it's clicked or the return key is used."""
        note = self._model.openNote(idx)
        self._updateNoteInfo(note)
        self._view.textEdit.setText(note.text)
        self._view.textEdit.setEnabled(True)
        self._view.upButton.setEnabled(True)
        self._view.downButton.setEnabled(True)
        self._view.textEdit.setFocus()

    def createNote(self, noteType):
        """Create a new note TODO: AND OPENS IT."""
        noteName = self._view.newNoteForm(noteType)
        if noteName == None:
            return
        self._view.textEdit.setText('')
        newNote = Note(noteName, noteType, '')
        self._model.addNote(newNote)
        self._updateNoteInfo(newNote)
        self._view.listNotes.setCurrentIndex(self._model.currentIndex)
        self._view.textEdit.setEnabled(True)
        self._view.upButton.setEnabled(True)
        self._view.downButton.setEnabled(True)
        self._view.textEdit.setFocus()

    def moveNote(self, direction):
        # TODO: Change to drag and drop at some point.
        self._model.swapNote(direction)
        self._view.listNotes.setCurrentIndex(self._model.currentIndex)

    def saveNoteText(self):
        """Save note text. TODO: Make available to rename note."""
        noteText = self._view.textEdit.toMarkdown()
        self._model.saveNoteText(noteText)

    def saveSession(self):
        """Parses the sesion to the JSON file."""
        self._model.saveSession()
        
    def _updateNoteInfo(self, note):
        """Update the note info in the infoText. TODO: Separate session and note info."""
        self._view.infoText.setText('Session name: {}\nName: {}\nType: {}\n'.format(
            self._model.sessionInfo['name'], note.name, note.noteType))

    def focusList(self):
        """Focus list when called."""
        self._view.listNotes.setFocus()
