# Step1: Access arXiv using URL
import requests


def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
    # Prepare the search query by converting topic to lowercase and replacing spaces with '+'
    query = "+".join(topic.lower().split())

    # Check if query contains invalid characters (to avoid breaking the URL request)
    for char in list('()" '):
        if char in query:
            print(f"Invalid character '{char}' in query: {query}")
            raise ValueError(f"Cannot have character: '{char}' in query: {query}")

    # Build the arXiv API query URL with filters (max_results, sorted by date in descending order)
    url = (
            "http://export.arxiv.org/api/query"
            f"?search_query=all:{query}"
            f"&max_results={max_results}"
            "&sortBy=submittedDate"
            "&sortOrder=descending"
        )
    print(f"Making request to arXiv API: {url}")

    # Send GET request to arXiv API
    resp = requests.get(url)
    
    # Handle failed requests
    if not resp.ok:
        print(f"ArXiv API request failed: {resp.status_code} - {resp.text}")
        raise ValueError(f"Bad response from arXiv API: {resp}\n{resp.text}")
    
    # Parse the XML response into a structured dictionary
    data = parse_arxiv_xml(resp.text)
    return data


# Step2: Parse XML
import xml.etree.ElementTree as ET

def parse_arxiv_xml(xml_content: str) -> dict:
    """Parse the XML content from arXiv API response."""

    entries = []
    # Define namespace mapping for Atom and arXiv schema
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }

    # Parse XML string into an ElementTree object
    root = ET.fromstring(xml_content)

    # Loop through each <entry> in Atom namespace
    for entry in root.findall("atom:entry", ns):
        # Extract authors list
        authors = [
            author.findtext("atom:name", namespaces=ns)
            for author in entry.findall("atom:author", ns)
        ]
        
        # Extract categories (terms under <category>)
        categories = [
            cat.attrib.get("term")
            for cat in entry.findall("atom:category", ns)
        ]
        
        # Extract PDF link (where type is "application/pdf")
        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break

        # Collect paper metadata into dictionary
        entries.append({
            "title": entry.findtext("atom:title", namespaces=ns),
            "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
            "authors": authors,
            "categories": categories,
            "pdf": pdf_link
        })

    # Return all collected entries inside a dictionary
    return {"entries": entries}



# Step3: Convert the functionality into a tool
from langchain_core.tools import tool


@tool
def arxiv_search(topic: str) -> list[dict]:
    """Search for recently uploaded arXiv papers

    Args:
        topic: The topic to search for papers about

    Returns:
        List of papers with their metadata including title, authors, summary, etc.
    """
    print("ARXIV Agent called")
    print(f"Searching arXiv for papers about: {topic}")

    # Call the function to search arXiv API
    papers = search_arxiv_papers(topic)

    # Handle case where no papers are found
    if len(papers) == 0:
        print(f"No papers found for topic: {topic}")
        raise ValueError(f"No papers found for topic: {topic}")

    # Print number of papers found and return them
    print(f"Found {len(papers['entries'])} papers about {topic}")
    return papers
