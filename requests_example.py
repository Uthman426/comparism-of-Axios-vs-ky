"""GET a repository record from GitHub's public API using requests.

Install:  python -m pip install requests
Run:      python requests_example.py
"""

import requests

URL = "https://api.github.com/repos/psf/requests"
HEADERS = {"Accept": "application/vnd.github+json"}


def fetch_repo(url: str = URL) -> dict:
    # requests has no default timeout, so one must always be passed.
    response = requests.get(url, headers=HEADERS, timeout=5)
    # Turn 4xx/5xx replies into an exception instead of failing silently.
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        repo = fetch_repo()
        print(repo["full_name"], "has", repo["stargazers_count"], "stars")
    except requests.HTTPError as exc:
        print("Server replied with an error:", exc.response.status_code)
    except requests.RequestException as exc:
        # Covers timeouts, connection failures and anything else from requests.
        print("Request failed:", exc)
