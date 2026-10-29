import httpx

URL = "https://api.github.com/repos/psf/requests"
HEADERS = {"Accept": "application/vnd.github+json"}


def fetch_repo(url: str = URL) -> dict:
    # httpx has a default timeout, but stating it keeps both examples equal.
    # Unlike requests, httpx does not follow redirects unless told to.
    response = httpx.get(url, headers=HEADERS, timeout=5.0, follow_redirects=True)
    # Turn 4xx/5xx replies into an exception instead of failing silently.
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    try:
        repo = fetch_repo()
        print(repo["full_name"], "has", repo["stargazers_count"], "stars")
    except httpx.HTTPStatusError as exc:
        print("Server replied with an error:", exc.response.status_code)
    except httpx.RequestError as exc:
        # Covers timeouts, connection failures and anything else from httpx.
        print("Request failed:", exc)
