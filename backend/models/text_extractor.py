import fitz  # contains PyMuPDF module 
import io

def extract_text_from_pdf(pdf_file) -> str:
    pdf_bytes = io.BytesIO(pdf_file.file.read())
    text = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text("text")
            if not page_text:
                page_text = page.get_text()
            text.append(page_text)
    return "\n".join(text)
