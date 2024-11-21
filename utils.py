from PyPDF2 import PdfReader
from docx import Document


def extract_text(filepath: str) -> str:
    if filepath.endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    elif filepath.endswith('.docx'):
        return extract_text_from_docx(filepath)
    else:
        return None
    
def extract_text_from_pdf(filepath: str) -> str:
    with open(filepath, 'rb') as file:
        pdf = PdfReader(file)
        text = ''
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()
        return text
    

def extract_text_from_docx(filepath: str) -> str:
    doc = Document(filepath)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text