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