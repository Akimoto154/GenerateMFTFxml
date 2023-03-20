import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


class Page3(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Create button
        buttonStartOver = QPushButton('Create another Xml', self)
        buttonEndProcess = QPushButton('Close', self)

        # Click event
        buttonStartOver.clicked.connect(self.parent.switchToPage1)
        buttonEndProcess.clicked.connect(QApplication.instance().quit)

        vbox = QVBoxLayout()
        vbox.addWidget(buttonStartOver)
        vbox.addWidget(buttonEndProcess)
        self.setLayout(vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Page3()
    ex.show()
    sys.exit(app.exec_())
