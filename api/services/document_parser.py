import docx
from pypdf import PdfReader

def extract_text_from_file(file_obj, filename: str) -> str:
    """Extract text from uploaded PDF or DOCX file."""
    ext = filename.lower().split('.')[-1]
    text = ""
    
    try:
        file_obj.seek(0)
        if ext == 'pdf':
            pdf = PdfReader(file_obj)
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif ext == 'docx':
            doc = docx.Document(file_obj)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing document {filename}: {e}")
        
    return text.strip()
