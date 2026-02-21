import io
import requests
import PyPDF2
from langchain_core.tools import tool


@tool
def read_pdf(url: str) -> str:
    """
    Docstring for read_pdf
    
    :param url: The URL of the PDF file to read
    :type url: str
    :return: The extracted text from the PDF
    :rtype: str
    """
    try:
        response = requests.get(url)
        # Load PDF into memory
        pdf_file = io.BytesIO(response.content)
        # Read PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)
        text = ""

        for idx, page in enumerate(pdf_reader.pages, start=1):
            print(f"Reading page {idx}/{total_pages}")
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        raise
