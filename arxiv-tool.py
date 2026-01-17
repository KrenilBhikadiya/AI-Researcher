# search papers using arXiv API
import requests


def parse_query(query: str) -> str:
    # remove invalid characters
    invalid_chars = ['"', "'", "\\", "/", ":", ";", "(", ")", "[", "]", "{", "}", "<", ">", "|", "`", "~", "!"]
    for char in invalid_chars:
        query = query.replace(char, " ")

    # replace multiple spaces with single space
    query = ''.join(query.split())
    if not query:
        raise ValueError("Please provide a valid search query.")
    return query


def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
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
    
    return response.text


print(search_arxiv_papers("machine learning", 3))
