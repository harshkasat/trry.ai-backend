# trry.ai-backend: Website Performance Testing and Analysis

This project provides a backend service for analyzing and testing the performance of websites. It uses various tools and techniques to gather performance metrics, capture screenshots, and conduct load tests.  The service is built using Flask, Python, and several libraries for web scraping, performance testing, and image capture.

## 1. Project Overview

`trry.ai-backend` offers a comprehensive suite of website performance analysis tools accessible via a REST API.  Key features include:

* **Website Performance Metrics:**  Collects performance data using the Google PageSpeed Insights API, providing metrics like First Contentful Paint, Largest Contentful Paint, and Cumulative Layout Shift.
* **Screenshot Capture:** Captures screenshots of websites for visual analysis.
* **Load Testing:** Performs load tests using Locust, simulating user traffic to assess website stability under stress.
* **Link Validation:** Extracts and validates links from a given URL.


## 2. Table of Contents

* [Project Overview](#1-project-overview)
* [Prerequisites](#4-prerequisites)
* [Installation Guide](#5-installation-guide)
* [API Reference](#10-api-reference)
* [Contributing Guidelines](#11-contributing-guidelines)


## 4. Prerequisites

* Python 3.7+
* `pip` (Python package installer)
* Dependencies listed in `requirements.txt` (install using `pip install -r requirements.txt`)
* A Google Cloud Platform (GCP) API key for PageSpeed Insights (for the `lighthouse_metrics.py` functionality).


## 5. Installation Guide

1. Clone the repository: `git clone https://github.com/harshkasat/trry.ai-backend.git`
2. Navigate to the project directory: `cd trry.ai-backend`
3. Install dependencies: `pip install -r requirements.txt`
4. (Optional) Create a virtual environment for isolation: `python3 -m venv .venv && source .venv/bin/activate`


## 10. API Reference

The backend exposes several endpoints:

* `/health/`:  (GET) Health check endpoint. Returns `{"message": "Server is running Health Check"}`.
* `/`: (GET) Simple greeting message.
* `/test_websites_performance/`: (POST)  Performs a Lighthouse performance test on a given URL.  Requires a JSON payload with a `url` field (e.g., `{"url": "https://www.example.com"}`).  Returns the Lighthouse results.
* `/capture_screenshots_websites/`: (POST) Captures screenshots of links from a given URL. Requires a JSON payload with a `url` field. Returns a success message or error.
* `/lighthouse_test/`: (POST)  Similar to `/test_websites_performance/`, but likely a more streamlined version.
* `/load_tests/`: (POST)  Performs a load test on links from a given URL. Requires a JSON payload with a `url` field. Returns the list of tested URLs.
* `/gernerate_valid_links/`: (POST) Extracts and validates links from a given URL.  Requires a JSON payload with a `url` field. Returns a list of valid links.


**Example using `curl` to test `/test_websites_performance/`:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.example.com"}' http://localhost:5000/test_websites_performance/
```

**Note:**  Replace `http://localhost:5000` with the actual address of your running server.  The server starts on port 5000 by default (see `app.py`).


## 11. Contributing Guidelines

Contributions are welcome! Please follow standard GitHub forking and pull request procedures.  A detailed contribution guide is not explicitly provided in the current repository.


## Code Snippets

**Example from `lighthouse_metrics.py` (fetching Lighthouse data):**

```python
def fetch(url):
    """Fetch the URL using requests."""
    try:
        google_api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + url
        response = requests.get(google_api, timeout=20.0)
        return response.json()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return {}
```

**Example from `async_locust.py` (load testing):**

```python
async def load_test_main(target_urls, file_path: Optional[str] = 'performance_tests'):
    try:
        # ... (code to run Locust load tests using `run_break_test` and `run_stress_test`) ...
    except Exception as e:
        logger.error(f"Error running performance tests: {e}")
    finally:
        shutil.make_archive(file_path, 'zip', file_path)
```

This README provides a foundation.  Further details on specific functions and error handling would need to be added based on a deeper review of the codebase.  The repository lacks comprehensive documentation within the code itself, making a fully comprehensive README challenging to create without significant reverse-engineering.
