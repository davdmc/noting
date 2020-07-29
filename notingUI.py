from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class NotingUi(QtWidgets.QMainWindow):
    """Noting's view (GUI)."""
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Main window
        self.resize(975, 867)
        self.setWindowTitle("Noting")

        # Central Widget & General Layout
        self._centralwidget = QtWidgets.QWidget(self)
        self.generalLayout = QtWidgets.QGridLayout()
        self.setCentralWidget(self._centralwidget)
        self._centralwidget.setLayout(self.generalLayout)

        # Text edit
        self.textEdit = QtWidgets.QTextEdit(self._centralwidget)
        self.generalLayout.addWidget(self.textEdit, 0, 0, -1, 1)

        # List dir
        self.listDir = QtWidgets.QListView(self._centralwidget)
        self.listDir.setObjectName("listDir")
        self.generalLayout.addWidget(self.listDir, 0, 1)

        # Info text
        self.infoText = QtWidgets.QLabel()
        self.infoText.setAlignment(QtCore.Qt.AlignTop)
        self.generalLayout.addWidget(self.infoText, 1, 1)

        # Set stretches
        self.generalLayout.setColumnStretch(0,1)
        self.generalLayout.setRowStretch(0,1)
        self.generalLayout.setRowStretch(1,1)

        # Menu bar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 975, 22))
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # Shortcuts
        self.createNoteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+N"), self._centralwidget)
        self.saveNoteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self._centralwidget)
        
    def selectSessionDialog(self):
        item, ok = QtWidgets.QInputDialog.getItem(self._centralwidget, 'Open/New Session', 'Choose if you want to open a session or create a new one.', ["Open session", "New session"],editable=False)
        
        if ok:
            if item == "Open session":
                return "open"
            else:
                return "new"
        else:
            sys.exit()

    def openSessionDialog(self):
        name, filter = QtWidgets.QFileDialog.getOpenFileName(self._centralwidget, "Select session")
        return name

    def nameNewSessionForm(self):
        #TODO: Choose optional date.
        name, ok = QtWidgets.QInputDialog.getText(self._centralwidget, 'New Session', 'Session name:')
        if ok:
            return name
        else:
            sys.exit()

    def newNoteForm(self):
        noteName, ok = QtWidgets.QInputDialog.getText(self._centralwidget, 'New Note', 'Note name:')
        if ok:
            return noteName
        else:
            return 'noName'
    def test(self):
        print("Working")