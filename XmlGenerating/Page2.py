import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QFileDialog
import xml.etree.ElementTree as ET


class Page2(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        self.config_file = "config.json"
        self.folderPath = ""
        self.load_config()

    def initUI(self):
        self.create_elements()
        self.create_event_connections()
        self.create_layouts()

    def create_elements(self):
        self.button_generate = QPushButton('Generate', self)
        self.button_back = QPushButton('Back', self)
        self.button_select_folder = QPushButton('Select Save Folder', self)
        self.text_target_model_class_path = QLineEdit(self)
        self.text_method_name = QLineEdit(self)
        self.text_category = QLineEdit(self)
        self.text_api = QLineEdit(self)
        self.text_parameters = QTextEdit()
        self.text_session = QTextEdit()
        self.text_cookie = QTextEdit()
        self.text_http_params = QTextEdit()
        self.text_case_count = QLineEdit(self)
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet('color: red')

    def create_event_connections(self):
        self.button_generate.clicked.connect(self.generate_clicked)
        self.button_back.clicked.connect(self.parent.switch_to_page_1)
        self.button_select_folder.clicked.connect(self.select_folder)

    def create_layouts(self):
        self.set_placeholders()

        hbox = QHBoxLayout()
        hbox.addWidget(self.button_generate)
        hbox.addWidget(self.button_back)

        vbox = QVBoxLayout()
        vbox.addWidget(self.button_select_folder)
        vbox.addWidget(self.text_target_model_class_path)
        vbox.addWidget(self.text_method_name)
        vbox.addWidget(self.text_category)
        vbox.addWidget(self.text_api)
        vbox.addWidget(self.text_parameters)
        vbox.addWidget(self.text_session)
        vbox.addWidget(self.text_cookie)
        vbox.addWidget(self.text_http_params)
        vbox.addWidget(self.text_case_count)
        vbox.addLayout(hbox)
        vbox.addWidget(self.error_label)
        self.setLayout(vbox)

        self.text_session.hide()
        self.text_cookie.hide()
        self.text_http_params.hide()

    def set_placeholders(self):
        self.text_target_model_class_path.setPlaceholderText(
            "Target Model Class Path 例: Mccm\Product\Model\Product"
        )
        self.text_method_name.setPlaceholderText("Method Name 例: getProduct")
        self.text_category.setPlaceholderText('Category 例: Customer, Product')
        self.text_api.setPlaceholderText('API Number 例: MCAPI00000, MCSHC0000')
        self.text_parameters.setPlaceholderText('Parameters (JSON)')
        self.text_session.setPlaceholderText('Session (JSON)')
        self.text_cookie.setPlaceholderText('Cookie (JSON)')
        self.text_http_params.setPlaceholderText('Http Params (JSON)')
        self.text_case_count.setPlaceholderText(
            'Total case number we need 例: 4'
        )

    def generate_clicked(self):
        if os.path.exists(self.config_file):
            self.generate_xml()
            self.parent.switch_to_page_3()
        else:
            self.select_folder()

    def set_visuality(self, states):
        session_checked, cookie_checked, http_checked = states
        self.text_session.setVisible(session_checked)
        self.text_cookie.setVisible(cookie_checked)
        self.text_http_params.setVisible(http_checked)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_path = folder_path
            self.save_config()

    def save_config(self):
        config = {'folder_path': self.folder_path}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.folder_path = config.get('folder_path')

    def generate_xml(self):
        try:
            tree_test = ET.parse('ReferXml/ProductMCAPI30270Test.xml')
            tree_action_group = ET.parse(
                'ReferXml/ProductMCAPI30270TestCase1ActionGroup.xml')
            tree_data = ET.parse('ReferXml/ProductMCAPI30270TestCase1Data.xml')
            root_test = tree_test.getroot()
            root_action_group = tree_action_group.getroot()
            root_data = tree_data.getroot()

            with open('ReferXml/ProductMCAPI30270Test.xml', 'r') as f:
                header = ''.join([f.readline() for i in range(7)])
        except Exception as e:
            self.error_label.setText(str(e))
            return

        self.modify_xml(root_test, root_action_group, root_data, header)

    def modify_xml(self, root_test, root_action_group, root_data, header):
        category = self.text_category.text()
        api = self.text_api.text()
        try:
            case_count = int(self.text_case_count.text())
        except Exception as e:
            self.error_label.setText(
                str(e) + '\n' + 'Please enter a case number.')
            return
        root_test.find('test').set('name', category + api + "Test")
        root_test.find(
            ".//actionGroup[@ref='ProductMCAPI30270Case1ActionGroup']"
        ).set('ref', category + api + "Case1ActionGroup")
        root_test.find(
            ".//actionGroup[@stepKey='ProductMCAPI30270Case1ActionGroup']"
        ).set('stepKey', category + api + "Case1ActionGroup")
        for i in range(2, case_count + 1):
            action_group = ET.Element('actionGroup')
            action_group.set('ref', category + api + f'Case{i}ActionGroup')
            action_group.set('stepKey', category + api + f'Case{i}ActionGroup')
            root_test.find('test').append(action_group)
        with open(self.folder_path + '/' + category + api + 'Test.xml', 'w') as f:
            f.write(header)
            f.write(ET.tostring(root_test, encoding='unicode'))

        # Action Group
        for i in range(1, case_count + 1):
            root_action_group.find('actionGroup').set(
                'name', category + api + f"Case{i}ActionGroup"
            )
            root_action_group.find(".//argument[@name='targetModelClassPath']").set(
                'defaultValue', '{{' + category + api +
                f"Case{i}Data.targetModelClassPath" + '}}'
            )
            root_action_group.find(".//argument[@name='methodName']").set(
                'defaultValue', '{{' + category + api +
                f"Case{i}Data.methodName" + '}}'
            )
            root_action_group.find(".//argument[@name='parameters']").set(
                'defaultValue', '{{' + category + api +
                f"Case{i}Data.parameters" + '}}'
            )
            with open(self.folder_path + '/' + category + api + f"Case{i}ActionGroup.xml", 'w') as f:
                f.write(header)
                f.write(ET.tostring(root_action_group, encoding='unicode'))

        # Data
        for i in range(1, case_count + 1):
            root_data.find('entity').set(
                'name', category + api + f"Case{i}Data")
            for element in root_data.findall(".//data"):
                if element.get('key') == 'targetModelClassPath':
                    element.text = self.text_target_model_class_path.text()
                elif element.get('key') == 'methodName':
                    element.text = self.text_method_name.text()
                elif element.get('key') == 'parameters':
                    element.text = self.text_parameters.toPlainText()
            with open(self.folder_path + '/' + category + api + f"Case{i}Data.xml", 'w') as f:
                f.write(header)
                f.write(ET.tostring(root_data, encoding='unicode'))

        # TODO: add session
        # TODO: add cookie
        # TODO: add http params


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Page2()
    ex.show()
    sys.exit(app.exec_())
