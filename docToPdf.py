import os
import sys
import subprocess

class DocToPdfConverter:
    def __init__(self):
        self.folder_path = "/home/yz/Documents/Files Container"  # Change this to your folder path

    def convert_docs_to_pdf(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".doc") or filename.endswith(".docx"):
                doc_path = os.path.join(self.folder_path, filename)
                pdf_path = os.path.join(self.folder_path, os.path.splitext(filename)[0] + ".pdf")
                self.convert_to_pdf(doc_path, pdf_path)
                os.remove(doc_path)  # Remove the original doc/docx file

    def convert_to_pdf(self, input_path, output_path):
        try:
            subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(output_path), input_path], stderr=subprocess.DEVNULL)
            print(f"Converted {input_path} to {output_path}")
        except Exception as e:
            print(f"Error converting {input_path} to PDF: {e}")

def main():
    converter = DocToPdfConverter()
    converter.convert_docs_to_pdf()

if __name__ == '__main__':
    main()


