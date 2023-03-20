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
        self.configFile = "config.json"
        self.loadConfig()

    def initUI(self):
        # Create elements
        buttonGenerate = QPushButton('Generate', self)
        buttonBack = QPushButton('Back', self)
        buttonSelectFolder = QPushButton('Select Save Folder', self)
        self.textTargetModelClassPath = QLineEdit(self)
        self.textMethodName = QLineEdit(self)
        self.textCategory = QLineEdit(self)
        self.textAPI = QLineEdit(self)
        self.textParameters = QTextEdit()
        self.textSession = QTextEdit()
        self.textCookie = QTextEdit()
        self.textHttpParams = QTextEdit()
        self.textCasecount = QLineEdit(self)

        # Create click event
        buttonGenerate.clicked.connect(self.generateClicked)
        buttonBack.clicked.connect(self.parent.switchToPage1)    
        buttonSelectFolder.clicked.connect(self.selectFolder)

        # Placeholder
        self.textTargetModelClassPath.setPlaceholderText(
            "Target Model Class Path 例: Mccm\Product\Model\Product"
        )
        self.textMethodName.setPlaceholderText("Method Name 例: getProduct")
        self.textCategory.setPlaceholderText('Category 例: Customer, Product')
        self.textAPI.setPlaceholderText('API Number 例: MCAPI00000, MCSHC0000')
        self.textParameters.setPlaceholderText('Parameters (JSON)')
        self.textSession.setPlaceholderText('Session (JSON)')
        self.textCookie.setPlaceholderText('Cookie (JSON)')
        self.textHttpParams.setPlaceholderText('Http Params (JSON)')
        self.textCasecount.setPlaceholderText('Total case number we need 例: 4')

        # Create label displaying error message
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet('color: red')

        # Horizontal layout
        hbox = QHBoxLayout()
        hbox.addWidget(buttonGenerate)
        hbox.addWidget(buttonBack)

        # Vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(buttonSelectFolder)
        vbox.addWidget(self.textTargetModelClassPath)
        vbox.addWidget(self.textMethodName)
        vbox.addWidget(self.textCategory)
        vbox.addWidget(self.textAPI)
        vbox.addWidget(self.textParameters)
        vbox.addWidget(self.textSession)
        vbox.addWidget(self.textCookie)
        vbox.addWidget(self.textHttpParams)
        vbox.addWidget(self.textCasecount)
        vbox.addLayout(hbox)
        vbox.addWidget(self.error_label)
        self.setLayout(vbox)

        # Hide by default
        self.textSession.hide()
        self.textCookie.hide()
        self.textHttpParams.hide()

    def generateClicked(self):
        if os.path.exists(self.configFile):
            self.generateXml()
            self.parent.switchToPage3()
        else:
            self.selectFolder()
    
    def setVisuality(self, states):
        sessionChecked, cookieChecked, httpChecked = states
        self.textSession.setVisible(sessionChecked)
        self.textCookie.setVisible(cookieChecked)
        self.textHttpParams.setVisible(httpChecked)

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folderPath:
            self.folderPath = folderPath
            self.saveConfig()

    def saveConfig(self):
        config = {'folder_path': self.folderPath}
        with open(self.configFile, 'w') as f:
            json.dump(config, f)

    def loadConfig(self):
        if os.path.exists(self.configFile):
            with open(self.configFile, 'r') as f:
                config = json.load(f)
                self.folderPath = config.get('folder_path')

    def generateXml(self):
        # Parse the XML file into an ElementTree object
        try:
            treeTest = ET.parse('ReferXml/ProductMCAPI30270Test.xml')
            treeActionGroup = ET.parse(
                'ReferXml/ProductMCAPI30270TestCase1ActionGroup.xml'
            )
            treeData = ET.parse('ReferXml/ProductMCAPI30270TestCase1Data.xml')
            rootTest = treeTest.getroot()
            rootActionGroup = treeActionGroup.getroot()
            rootData = treeData.getroot()
            # Read the first 7 lines of the original XML file
            with open('ReferXml/ProductMCAPI30270Test.xml', 'r') as f:
                header = ''.join([f.readline() for i in range(7)])
        except Exception as e:
            self.error_label.setText(str(e))
            return

        self.modifyXml(rootTest, rootActionGroup, rootData, header)

        # Write the modified XML to a new file, including the original header

    def modifyXml(self, rootTest, rootActionGroup, rootData, header):
        # Test
        category = self.textCategory.text()
        api = self.textAPI.text()
        try:
            casecount = int(self.textCasecount.text())
        except Exception as e:
            self.error_label.setText(
                str(e) + '\n' + 'Please enter a case number.')
            return
        rootTest.find('test').set('name', category + api + "Test")
        rootTest.find(
            ".//actionGroup[@ref='ProductMCAPI30270Case1ActionGroup']"
        ).set('ref', category + api + "Case1ActionGroup")
        rootTest.find(
            ".//actionGroup[@stepKey='ProductMCAPI30270Case1ActionGroup']"
        ).set('stepKey', category + api + "Case1ActionGroup")
        for i in range(2, casecount + 1):
            actionGroup = ET.Element('actionGroup')
            actionGroup.set('ref', category + api + f'Case{i}ActionGroup')
            actionGroup.set('stepKey', category + api + f'Case{i}ActionGroup')
            rootTest.find('test').append(actionGroup)
        with open(self.folderPath + '/' + category + api + 'Test.xml', 'w') as f:
            f.write(header)
            f.write(ET.tostring(rootTest, encoding='unicode'))

        # Action Group
        for i in range(1, casecount + 1):
            rootActionGroup.find('actionGroup').set(
                'name', category + api + f"Case{i}ActionGroup"
            )
            rootActionGroup.find(".//argument[@name='targetModelClassPath']").set(
                'defaultValue', category + api +
                f"Case{i}Data.targetModelClassPath"
            )
            rootActionGroup.find(".//argument[@name='methodName']").set(
                'defaultValue', category + api + f"Case{i}Data.methodName"
            )
            rootActionGroup.find(".//argument[@name='parameters']").set(
                'defaultValue', category + api + f"Case{i}Data.parameters"
            )
            with open(self.folderPath + '/' + category + api + f"Case{i}ActionGroup.xml", 'w') as f:
                f.write(header)
                f.write(ET.tostring(rootActionGroup, encoding='unicode'))

        # Data
        for i in range(1, casecount + 1):
            rootData.find('entity').set(
                'name', category + api + f"Case{i}Data")
            for element in rootData.findall(".//data"):
                if element.get('key') == 'targetModelClassPath':
                    element.text = self.textTargetModelClassPath.text()
                elif element.get('key') == 'methodName':
                    element.text = self.textMethodName.text()
                elif element.get('key') == 'parameters':
                    element.text = self.textParameters.toPlainText()
            with open(self.folderPath + '/' + category + api + f"Case{i}Data.xml", 'w') as f:
                f.write(header)
                f.write(ET.tostring(rootData, encoding='unicode'))

        # TODO: add session
        # TODO: add cookie
        # TODO: add http params

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Page2()
    ex.show()
    sys.exit(app.exec_())
