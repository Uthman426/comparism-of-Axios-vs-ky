# Choosing a Python HTTP client for SwiftServe

Word count: about 660 (write-up only; code and source list are not counted).

## The need

For a SwiftServe pilot, a small service may need to ask a web API for information such as a vehicle record or service status. I compared two free Python libraries for the same job: send a GET request to GitHub's public API, check that the request succeeded, and read the JSON reply. The libraries are **requests** and **httpx**. The two examples are in this folder (`requests_example.py` and `httpx_example.py`). They were written from the documentation, so run them before relying on them.

## Size and dependencies

I did not measure installed size, so I compared dependencies, which show how much third-party code each library brings in. Requests relies on four packages: urllib3, certifi, idna and charset_normalizer. Httpx's manifest lists five (anyio, certifi, httpcore, idna and sniffio), and httpcore in turn builds on h11. Httpx also offers optional extras for HTTP/2, SOCKS proxies, Brotli, zstd and a command-line client, none of which are needed for a plain GET. The README files give a Python floor of 3.10 for requests and 3.9 for httpx.

## How active the maintenance is

The two projects are healthy in different ways. Requests has 54.6k GitHub stars, 6,495 commits, 156 open issues and 88 open pull requests. Its 2.33.0 release on 25 March 2026 fixed a security issue (CVE-2026-25645), added Python 3.14 support and dropped Python 3.9. Its README claims about 300 million downloads a week and more than four million dependent repositories. That is a mature library getting steady, careful updates.

Httpx has 15.2k stars and 149 open issues. A late-March 2026 snapshot showed only 17 commits from 15 people in the past year, and one author wrote 671 of its 1,482 commits. The last stable release on PyPI is 0.28.1 from December 2024, and a ground-up 1.0 rewrite has only appeared as development pre-releases. An August 2026 article reports that the Pydantic team now maintains a fork called httpx2, and that the OpenAI and Anthropic Python SDKs have moved to it. That article is a secondary source, so treat it as a signal worth checking, not settled fact. Even so, httpx is the better-known name with the less certain roadmap, and it is still pre-1.0.

## Quality of the documentation

Requests has a Read the Docs site and a short README with a clear feature list. Httpx has its own site with pages for async use, HTTP/2, advanced usage and third-party tools, plus a note that its Client is the equivalent of a requests Session, which makes migration easier. My judgement comes from the READMEs and documentation indexes, not a full read, so skim both for your own use case.

## How each example felt to write

The two scripts came out almost line for line the same, which is httpx's stated aim of building on requests' usability. The differences are small but real. Requests has no default timeout, so forgetting `timeout=` can hang a service forever. Httpx has a default but does not follow redirects unless told to, which matters because GitHub answers renamed repositories with a redirect. Exception names differ: `requests.HTTPError` and `RequestException` against `httpx.HTTPStatusError` and `RequestError`. Neither felt harder to write. Requests needed one fewer argument, while httpx would pay off only once the code needs async calls, which this pilot does not.

## Recommendation

I would choose **requests** for the SwiftServe pilot. The job is a few synchronous GET calls, and requests is the safer default: stable 2.x API, a recent security-fixed release, a huge user base, and answers to nearly every question online. Boring is a virtue for a pilot.

I would choose **httpx** instead if the service must make many calls at once, runs inside an async framework such as FastAPI, or needs HTTP/2. In that case, pin an exact version, expect the 1.0 rewrite to change the API, and watch whether the project's direction settles. If either library goes into production, pin versions in a lockfile and re-check these numbers first, because they come from snapshots taken between March and August 2026.

## Sources

- requests repository page and README: github.com/psf/requests
- requests 2.33.0 release notes (25 March 2026): github.com/psf/requests/blob/main/HISTORY.md
- httpx repository and registry snapshot (late March 2026): summary.ecosyste.ms/projects/368061
- httpx README and documentation index: github.com/encode/httpx and python-httpx.org
- httpx 1.0 pre-releases: pypi.org/project/httpx/1.0.dev5/
- httpx2 fork and SDK migration (secondary source, August 2026): dev.to/mr_manushukla, article on the Anthropic Python SDK 1.0 and httpx2
