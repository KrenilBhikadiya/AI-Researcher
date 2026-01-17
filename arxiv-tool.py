# search papers using arXiv API
import requests

query = "Generative AI"
max_results = 10

url = (
    "http://export.arxiv.org/api/query"
    f"?search_query=all:{query}"
    f"&start=0&max_results={max_results}"
    "&sortBy=relevance"
    "&sortOrder=descending"
)

response = requests.get(url)
print(response.text)