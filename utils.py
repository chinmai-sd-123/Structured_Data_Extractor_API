import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

MAX_HTML_SIZE = 150000   # Prevent huge memory usage
TIMEOUT_SECONDS = 25     # Prevent hanging


def fetch_website_contents(url):
    """
    Fetch website content safely.
    - Adds timeout
    - Handles errors
    - Limits page size
    - Cleans unnecessary tags
    """

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=TIMEOUT_SECONDS,
            allow_redirects=True
        )

        response.raise_for_status()

        html = response.text[:MAX_HTML_SIZE]

        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title found"

        # Remove unwanted tags
        for tag in soup(["script", "style", "img", "input", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        return f"{title}\n\n{text[:2000]}"

    except requests.exceptions.Timeout:
        return "Error: Website took too long to respond."

    except requests.exceptions.RequestException as e:
        return f"Error fetching website: {str(e)}"