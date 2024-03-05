import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidget, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QFont
import subprocess

class PrintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.folder_path = "/home/yz/Documents/Files Container"
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.title_label = QLabel("File Printing Kiosk", self)
        self.title_label.setFont(QFont("Arial", 20))
        self.layout.addWidget(self.title_label)

        self.file_list = QListWidget(self)
        self.load_files()
        self.layout.addWidget(self.file_list)

        self.print_files_button = QPushButton('Print Files', self)
        self.print_files_button.clicked.connect(self.print_all_files)
        self.layout.addWidget(self.print_files_button)

        self.close_button = QPushButton('Close', self)
        self.close_button.clicked.connect(self.close_application)
        self.layout.addWidget(self.close_button)

        self.setWindowTitle('File Printing Kiosk')
        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(), QApplication.desktop().screenGeometry().height())  # Full-screen
        self.showFullScreen()

    def load_files(self):
        files = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
        self.file_list.addItems(files)

    def print_all_files(self):
        for i in range(self.file_list.count()):
            file_path = os.path.join(self.folder_path, self.file_list.item(i).text())
            if file_path.lower().endswith('.pdf'):
                self.print_pdf(file_path)
            elif file_path.lower().endswith('.docx'):
                self.print_doc(file_path)

    def print_pdf(self, pdf_file):
        try:
            subprocess.run(["lp", pdf_file])
            print(f"Printing PDF file '{pdf_file}'")
        except Exception as e:
            print(f"Error printing PDF file '{pdf_file}': {e}")

    def print_doc(self, doc_file):
        try:
            subprocess.run(["libreoffice", "--headless", "--print", doc_file])
            print(f"Printing DOCX file '{doc_file}'")
        except Exception as e:
            print(f"Error printing DOCX file '{doc_file}': {e}")

    def close_application(self):
        self.close()


def main():
    app = QApplication(sys.argv)
    ex = PrintApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

