import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QVBoxLayout
from PyQt5.QtCore import pyqtSignal


class Page1(QWidget):

    sendCheckboxStates = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Create a button in the window
        buttonNextPage = QPushButton('Next Step', self)
        buttonNextPage.clicked.connect(self.switchToPage2)

        # Create check boxes
        self.checkboxSession = QCheckBox('session', self)
        self.checkboxCookie = QCheckBox('cookie', self)
        self.checkboxHttpParams = QCheckBox('http params', self)

        # Create a vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.checkboxSession)
        vbox.addWidget(self.checkboxCookie)
        vbox.addWidget(self.checkboxHttpParams)
        vbox.addWidget(buttonNextPage)
        self.setLayout(vbox)
        
    def switchToPage2(self):
        sessionChecked = self.checkboxSession.isChecked()
        cookieChecked = self.checkboxCookie.isChecked()
        httpChecked = self.checkboxHttpParams.isChecked()

        # Emit the signal with the checkbox states
        self.sendCheckboxStates.emit((sessionChecked, cookieChecked, httpChecked))
        self.parent.switchToPage2()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Page1()
    ex.show()
    sys.exit(app.exec_())
