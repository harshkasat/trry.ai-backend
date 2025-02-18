import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List
import time

@dataclass
class LinkStatus:
    url: str
    status_code: int
    is_alive: bool
    response_time: float
    error: str = None

def check_link_health(url: str) -> LinkStatus:
    """Check health of a single URL and return its status."""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10.0, allow_redirects=True)
        response_time = time.time() - start_time
        
        return LinkStatus(
            url=url,
            status_code=response.status_code,
            is_alive=response.status_code == 200,
            response_time=response_time
        )
    except Exception as e:
        return LinkStatus(
            url=url,
            status_code=-1,
            is_alive=False,
            response_time=-1,
            error=str(e)
        )

def get_links_from_url(url: str) -> List[str]:
    """Scrape all links from a single URL."""
    try:
        response = requests.get(url, timeout=10.0)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        print(f"Found {len(links)} links on {url}")
        return links
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

def check_links_health(links: List[str], max_workers: int = 20) -> List[LinkStatus]:
    """Check health of multiple links concurrently."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(check_link_health, links))
    return results

def fetch_and_check_links(start_url: str, max_workers: int = 20) -> List[LinkStatus]:
    """Main function to fetch links and check their health."""
    # Step 1: Get all links from the starting URL
    print(f"Fetching links from {start_url}")
    links = get_links_from_url(start_url)
    
    # Step 2: Check health of all links concurrently
    print(f"Checking health of {len(links)} links...")
    results = check_links_health(links, max_workers)
    
    return [r.url for r in results if r.is_alive]

# if __name__ == "__main__":
#     start_url = "https://aigrant.com/"
#     start_time = time.time()
    
#     # Fetch and check all links
#     results = fetch_and_check_links(start_url, max_workers=20)
    
#     # Print results
#     # print_results(results)
#     print(results)
    
#     print(f"\nTotal time taken: {time.time() - start_time:.2f} seconds")