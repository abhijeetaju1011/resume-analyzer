import fitz  # PyMuPDF - PDF reading
import docx  # python-docx - DOCX reading
import logging

# Logger setup
logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file using PyMuPDF."""
    try:
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        logger.info(f"PDF parsed successfully: {file_path}")
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        raise ValueError(f"Could not read PDF file: {e}")


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file using python-docx."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        logger.info(f"DOCX parsed successfully: {file_path}")
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing DOCX: {e}")
        raise ValueError(f"Could not read DOCX file: {e}")


def parse_resume(file_path: str) -> str:
    """
    Main function - detect file type and extract text.
    Supports PDF and DOCX formats.
    """
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")