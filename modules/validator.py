import os

# Allowed file types
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

# Maximum file size: 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes


def validate_file(filename: str, file_size: int) -> dict:
    """
    Validate uploaded file - check extension and size.
    Returns dict with 'valid' (bool) and 'error' (str) keys.
    """

    # Check if file has an extension
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in ALLOWED_EXTENSIONS:
        return {
            "valid": False,
            "error": f"Invalid file type '{ext}'. Only PDF and DOCX allowed."
        }

    # Check file size
    if file_size > MAX_FILE_SIZE:
        return {
            "valid": False,
            "error": "File too large. Maximum size is 5MB."
        }

    # Check file is not empty
    if file_size == 0:
        return {
            "valid": False,
            "error": "File is empty."
        }

    return {"valid": True, "error": None}