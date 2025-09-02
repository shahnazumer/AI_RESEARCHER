# Import necessary libraries
from langchain_core.tools import tool   # For defining the function as a LangChain tool
import io                               # To handle in-memory binary streams (for PDF data)
import PyPDF2                           # For reading and extracting text from PDF files
import requests                         # For downloading the PDF from a given URL

@tool
def read_pdf(url: str) -> str:
    """Read and extract text from a PDF file given its URL.

    Args:
        url: The URL of the PDF file to read

    Returns:
        The extracted text content from the PDF
    """
    try:
        # Send HTTP GET request to fetch the PDF file from the URL
        response = requests.get(url)

        # Load PDF content into memory as a binary stream
        pdf_file = io.BytesIO(response.content)

        # Initialize PDF reader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Get total number of pages in PDF
        num_pages = len(pdf_reader.pages)

        # Initialize an empty string to store extracted text
        text = ""

        # Loop through each page and extract text
        for i, page in enumerate(pdf_reader.pages, 1):
            print(f"Extracting text from page {i}/{num_pages}")
            text += page.extract_text() + "\n"

        # Print summary of extraction
        print(f"Successfully extracted {len(text)} characters of text from PDF")

        # Return the cleaned extracted text
        return text.strip()

    except Exception as e:
        # Handle and raise errors if PDF reading fails
        print(f"Error reading PDF: {str(e)}")
        raise
