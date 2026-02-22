from pypdf import PdfReader

def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    return '\n'.join(page.extract_text() or '' for page in reader.pages)