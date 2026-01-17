# search papers using arXiv API
import requests


def parse_query(query: str) -> str:
    """
    Docstring for parse_query
    
    :param query: The search query string
    :type query: str
    :return: The parsed query string with invalid characters removed
    :rtype: str
    """

    # remove invalid characters
    invalid_chars = ['"', "'", "\\", "/", ":", ";", "(", ")", "[", "]", "{", "}", "<", ">", "|", "`", "~", "!"]
    for char in invalid_chars:
        query = query.replace(char, " ")

    # replace multiple spaces with single space
    query = ''.join(query.split())
    if not query:
        raise ValueError("Please provide a valid search query.")
    return query


def parse_xml_response(xml_response: str) -> dict:
    """
    Docstring for parse_xml_response
    
    :param xml_response: The raw XML response from the arXiv API
    :type xml_response: str
    :return: A dictionary containing parsed paper information
    :rtype: dict[Any, Any]
    """
    
    import xml.etree.ElementTree as ET
    entries = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_response)

    for entry in root.findall("atom:entry", ns):
        # extract author names
        authors = [
            author.findtext("atom:name", namespaces=ns)
            for author in entry.findall("atom:author", ns)
        ]

        # extract categories
        categories = [
            category.attrib.get("term", "")
            for category in entry.findall("atom:category", ns)
        ]

        # extract PDF link
        pdf_link = ""
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href", "")
                break

        entries.append({
            "title": entry.findtext("atom:title", namespaces=ns),
            "summary": entry.findtext("atom:summary", namespaces=ns),
            "authors": authors,
            "categories": categories,
            "pdf_link": pdf_link,
        })
    
    return {
        "entries": entries
    }


def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
    """
    Docstring for search_arxiv_papers
    
    :param topic: The topic to search for
    :type topic: str
    :param max_results: The maximum number of results to return
    :type max_results: int
    :return: The parsed response from the arXiv API
    :rtype: str
    """

    parsed_query = parse_query(topic)
    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query=all:{parsed_query}"
        f"&start=0&max_results={max_results}"
        "&sortBy=relevance"
        "&sortOrder=descending"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data from arXiv API: {response.status_code}")
    
    data = parse_xml_response(response.text)
    return data


print(search_arxiv_papers("Black Hole", 3))
