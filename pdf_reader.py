import io
import requests
import PyPDF2
from langchain_core.tools import tool


url = "https://arxiv.org/pdf/1508.02986v1"
response = requests.get(url)
pdf_file = io.BytesIO(response.content)
pdf_reader = PyPDF2.PdfReader(pdf_file)

print(len(pdf_reader.pages))