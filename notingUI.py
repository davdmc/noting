from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class NotingUi(QtWidgets.QMainWindow):
    """Noting's view (GUI)."""

    # Signals
    returnKeyPressed = QtCore.pyqtSignal(QtCore.QModelIndex)

    def __init__(self):
        """View initializer."""
        super().__init__()

        # Main window
        self.resize(975, 867)
        self.setWindowTitle("Noting")

        # Central Widget & General Layout
        self._centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._centralwidget)

        self.generalLayout = QtWidgets.QGridLayout()
        self._centralwidget.setLayout(self.generalLayout)

        # Text edit
        self.textEdit = QtWidgets.QTextEdit(self._centralwidget)
        self.generalLayout.addWidget(self.textEdit, 0, 0, -1, 1)

        # Up/down buttons
        self.moveNoteButtonBar = QtWidgets.QFrame(self._centralwidget)
        self.generalLayout.addWidget(self.moveNoteButtonBar,0,1)

        self.moveNoteButtonBarLayout = QtWidgets.QGridLayout()

        self.moveNoteButtonBar.setLayout(self.moveNoteButtonBarLayout)

        self.upButton = QtWidgets.QPushButton(self.moveNoteButtonBar)
        self.upButton.setText('Up')
        self.moveNoteButtonBarLayout.addWidget(self.upButton,0,0)

        self.downButton = QtWidgets.QPushButton(self.moveNoteButtonBar)
        self.moveNoteButtonBarLayout.addWidget(self.downButton,0,1)
        self.downButton.setText('Down')

        # List dir
        self.listNotes = QtWidgets.QListView(self._centralwidget)
        self.listNotes.setObjectName("listNotes")
        ## Used to manage the return key to open the item.
        self.listNotes.installEventFilter(self)
        self.generalLayout.addWidget(self.listNotes, 1, 1)

        # Markdown preview
        self.previewText = QtWidgets.QTextEdit()
        self.previewText.setReadOnly(True)
        self.generalLayout.addWidget(self.previewText, 2, 1)
        ## Auto-update this widget with the text to preview markdown.
        self.textEdit.textChanged.connect(self._updateMarkdown)

        # Info text
        self.infoText = QtWidgets.QLabel()
        self.infoText.setAlignment(QtCore.Qt.AlignTop)
        self.generalLayout.addWidget(self.infoText, 3, 1)

        # Set stretches
        self.generalLayout.setColumnStretch(0,1)
        self.generalLayout.setRowStretch(0,0)
        self.generalLayout.setRowStretch(1,3)
        self.generalLayout.setRowStretch(2,3)

        # Menu bar
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setStyleSheet("QMenuBar {padding: 2px} QMenuBar::item {padding: 4px 12px; border-radius: 4px;} QMenuBar::item:selected { /* when selected using mouse or keyboard */background: #a8a8a8;}")
        self.fileMenu = self.menuBar.addMenu("File")
        self.newSession = self.fileMenu.addAction("New Session")
        self.openSession = self.fileMenu.addAction("Open Session")
        self.saveSession = self.fileMenu.addAction("Save Session")
        self.editSessionData = self.fileMenu.addAction("Session Data")
        self.exportMenu = self.menuBar.addMenu("Export")
        self.exportPDF = self.exportMenu.addAction("Export to PDF")
        self.setMenuBar(self.menuBar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # Shortcuts
        self.createNoteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+N"), self._centralwidget)
        self.createQuestionShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self._centralwidget)
        self.createTaskShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+T"), self._centralwidget)
        self.saveNoteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self._centralwidget)
        self.saveSessionShortcut = QtGui.QKeySequence("Ctrl+O")
        self.focusListShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+E"), self._centralwidget)

    def selectSessionDialog(self):
        """Session manager dialog."""
        item, ok = QtWidgets.QInputDialog.getItem(self._centralwidget, 'Open/New Session', 'Choose if you want to open a session or create a new one.', ["Open session", "New session"],editable=False)
        
        if ok:
            if item == "Open session":
                return "open"
            else:
                return "new"
        else:
            sys.exit()

    def openSessionDialog(self):
        """Interface to select the session file. TODO: Add filters and check the file format."""
        name, filter = QtWidgets.QFileDialog.getOpenFileName(self._centralwidget, "Select session")
        return name

    def nameNewSessionForm(self):
        """Form to name a new session that will be created in the current directory. TODO: Choose optional date."""
        name, ok = QtWidgets.QInputDialog.getText(self._centralwidget, 'New Session', 'Session name:')
        if ok:
            return name
        else:
            sys.exit()

    def newNoteForm(self, noteType):
        """Form to create a new note."""
        noteName, ok = QtWidgets.QInputDialog.getText(self._centralwidget, 'New {}'.format(noteType.capitalize()), '{} name:'.format(noteType.capitalize()))
        if ok:
            return noteName
        else:
            return None

    def selectExportOrderForm(self):
        """Export order dialog: List or Note Type"""
        item, ok = QtWidgets.QInputDialog.getItem(self._centralwidget, 'Exporting order', 'Choose the order for the exported document according to:', ["List", "Note type"],editable=False)
        
        if ok:
            if item == "List":
                # Unordered
                return False
            else:
                # Ordered
                return True
        else:
            sys.exit()

    def exportSessionDialog(self):
        """Interface to select the exported file."""
        name, filter = QtWidgets.QFileDialog.getSaveFileName(self._centralwidget, "Select output file.")
        return name

    def _updateMarkdown(self):
        """Updates the markdown of the text preview."""
        self.previewText.setMarkdown(self.textEdit.toMarkdown())

    def eventFilter(self, watched, event):
        """Event filter to manage custom events on the UI."""
        if event.type() == QtCore.QEvent.KeyPress and event.matches(QtGui.QKeySequence.InsertParagraphSeparator):
            idx = self.listNotes.currentIndex()
            self.returnKeyPressed.emit(idx)
        
            return True
    
        return False
            