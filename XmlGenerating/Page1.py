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
        button_next_page = QPushButton('Next Step', self)
        button_next_page.clicked.connect(self.switch_to_page_2)

        # Create check boxes
        self.checkbox_session = QCheckBox('session', self)
        self.checkbox_cookie = QCheckBox('cookie', self)
        self.checkbox_http_params = QCheckBox('http params', self)

        # Create a vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.checkbox_session)
        vbox.addWidget(self.checkbox_cookie)
        vbox.addWidget(self.checkbox_http_params)
        # vbox.addStretch(1)
        vbox.addWidget(button_next_page)
        self.setLayout(vbox)

    def switch_to_page_2(self):
        session_checked = self.checkbox_session.isChecked()
        cookie_checked = self.checkbox_cookie.isChecked()
        http_checked = self.checkbox_http_params.isChecked()

        # Emit the signal with the checkbox states
        self.sendCheckboxStates.emit(
            (session_checked, cookie_checked, http_checked)
        )
        self.parent.switch_to_page_2()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Page1()
    ex.show()
    sys.exit(app.exec_())
