from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_resume_text(upload_file):
    filename = upload_file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(upload_file.file)

    elif filename.endswith(".docx"):
        return extract_text_from_docx(upload_file.file)

    else:
        return ""