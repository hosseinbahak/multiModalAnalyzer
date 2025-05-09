# backend/tools/pdf_tools.py
"""
Tools for PDF analysis and processing.
"""
import os
import tempfile
from pdf2image import convert_from_path
from backend.tools.registry import tool
from backend.tools.image_tools import analyze_image

@tool
def analyze_pdf_page(pdf_path: str, page_number: int = 0, instruction: str = "Please describe this image in detail.") -> str:
    """
    Extract and analyze a specific page from a PDF document.
    
    :function: analyze_pdf_page
    :param str pdf_path: Path to the PDF file
    :param int page_number: Page number to analyze (0-based index)
    :param str instruction: Custom instruction for image analysis
    :return: Analysis result of the specified PDF page
    """
    try:
        # Convert PDF page to image
        with tempfile.TemporaryDirectory() as temp_dir:
            pages = convert_from_path(pdf_path)
            if page_number >= len(pages):
                return f"Error: Page number {page_number} is out of range. PDF has {len(pages)} pages."
            
            temp_image_path = os.path.join(temp_dir, f'page_{page_number}.png')
            pages[page_number].save(temp_image_path, 'PNG')
            
            # Use the existing analyze_image tool
            return analyze_image(temp_image_path, instruction)
    except Exception as e:
        return f"Error analyzing PDF: {str(e)}"