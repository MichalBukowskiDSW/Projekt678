import sys
import json
import yaml
import xmltodict
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

def parse_arguments():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    return input_file, output_file

def load_json(input_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        print("JSON data loaded successfully")
        return data
    except Exception as e:
        print(f"Failed to load JSON file: {e}")
        sys.exit(1)

def save_json(data, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print("JSON data saved successfully")
    except Exception as e:
        print(f"Failed to save JSON file: {e}")
        sys.exit(1)

def load_yaml(input_file):
    try:
        with open(input_file, 'r') as f:
            data = yaml.safe_load(f)
        print("YAML data loaded successfully")
        return data
    except Exception as e:
        print(f"Failed to load YAML file: {e}")
        sys.exit(1)

def save_yaml(data, output_file):
    try:
        with open(output_file, 'w') as f:
            yaml.safe_dump(data, f)
        print("YAML data saved successfully")
    except Exception as e:
        print(f"Failed to save YAML file: {e}")
        sys.exit(1)

def load_xml(input_file):
    try:
        with open(input_file, 'r') as f:
            data = xmltodict.parse(f.read())
        print("XML data loaded successfully")
        return data
    except Exception as e:
        print(f"Failed to load XML file: {e}")
        sys.exit(1)

def save_xml(data, output_file):
    try:
        with open(output_file, 'w') as f:
            xmltodict.unparse(data, output=f, pretty=True)
        print("XML data saved successfully")
    except Exception as e:
        print(f"Failed to save XML file: {e}")
        sys.exit(1)

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.input_label = QLabel("Input File: None")
        self.output_label = QLabel("Output File: None")
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.output_label)

        self.input_button = QPushButton('Select Input File')
        self.output_button = QPushButton('Select Output File')
        self.convert_button = QPushButton('Convert')

        self.input_button.clicked.connect(self.select_input_file)
        self.output_button.clicked.connect(self.select_output_file)
        self.convert_button.clicked.connect(self.convert_files)

        self.layout.addWidget(self.input_button)
        self.layout.addWidget(self.output_button)
        self.layout.addWidget(self.convert_button)

        self.setLayout(self.layout)
        self.setWindowTitle('Data Converter')
        self.show()

    def select_input_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "All Files (*);;JSON Files (*.json);;YAML Files (*.yml *.yaml);;XML Files (*.xml)", options=options)
        if file:
            self.input_label.setText(f"Input File: {file}")
            self.input_file = file

    def select_output_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "All Files (*);;JSON Files (*.json);;YAML Files (*.yml *.yaml);;XML Files (*.xml)", options=options)
        if file:
            self.output_label.setText(f"Output File: {file}")
            self.output_file = file

    def convert_files(self):
        self.thread = threading.Thread(target=self._convert_files)
        self.thread.start()

    def _convert_files(self):
        try:
            if self.input_file.endswith('.json'):
                data = load_json(self.input_file)
            elif self.input_file.endswith('.yml') or self.input_file.endswith('.yaml'):
                data = load_yaml(self.input_file)
            elif self.input_file.endswith('.xml'):
                data = load_xml(self.input_file)

            if self.output_file.endswith('.json'):
                save_json(data, self.output_file)
            elif self.output_file.endswith('.yml') or self.output_file.endswith('.yaml'):
                save_yaml(data, self.output_file)
            elif self.output_file.endswith('.xml'):
                save_xml(data, self.output_file)
            self.output_label.setText("Conversion Successful!")
        except Exception as e:
            self.output_label.setText(f"Conversion Failed: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterApp()
    sys.exit(app.exec_())