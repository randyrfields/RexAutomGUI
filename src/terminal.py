import customtkinter


class Terminal:

    def __init__(self, mainTB):
        self.mainTextBox = mainTB

    def clearTerminal(self):
        self.mainTextBox.delete("0.0", "end")
        self.mainTextBox.insert("0.0", "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        self.mainTextBox.insert("0.0", "")

    def addTextTerminal(self, text):
        self.mainTextBox.insert("0.0", " ")
