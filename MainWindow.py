# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from XmlGenerating.Page1 import Page1
from XmlGenerating.Page2 import Page2
from XmlGenerating.Page3 import Page3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('XML Generator')
        self.resize(800, 600)
        self.stack = QStackedWidget()
        self.page1 = Page1(parent=self)
        self.page2 = Page2(parent=self)
        self.page3 = Page3(parent=self)
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)
        self.setCentralWidget(self.stack)

    def switch_to_page_1(self):
        self.stack.setCurrentIndex(0)

    def switch_to_page_2(self):
        # Get the state of the checkboxes in Page1
        self.page1.sendCheckboxStates.connect(self.page2.set_visuality)

        self.stack.setCurrentIndex(1)

    def switch_to_page_3(self):
        self.stack.setCurrentIndex(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
