from jarvis.interfaces.research import ResearchInterface
import requests

class WebResearch(ResearchInterface):
    def search(self, query: str) -> dict:
        # DuckDuckGo Instant Answer API (no key required, limited info)
        url = 'https://api.duckduckgo.com/'
        params = {'q': query, 'format': 'json', 'no_redirect': 1, 'no_html': 1}
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return resp.json()
        return {}

    def summarize(self, results: dict) -> str:
        # Use AbstractText and AbstractURL if available
        abstract = results.get('AbstractText')
        url = results.get('AbstractURL')
        if abstract and url:
            return f"{abstract}\nSource: {url}"
        elif abstract:
            return abstract
        elif url:
            return f"Source: {url}"
        else:
            return "No summary available."