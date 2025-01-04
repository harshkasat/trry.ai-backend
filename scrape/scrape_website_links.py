import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin


async def fetch_links(url):
    """Fetch and parse all links from the given URL."""  
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                await asyncio.sleep(2)
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
                return links
        except Exception as e:
            print(f"Error fetching links from {url}: {e}")
            return []

async def check_link_status(link, session):
    """Check the status code of a link using a HEAD request."""
    try:
        async with session.head(link, timeout=10) as response:
            return link, response.status
    except Exception as e:
        return link, f"Error: {e}"

async def scrape_and_validate_links(url):
    """Scrape links and validate them asynchronously."""
    import time
    start_time = time.time()
    valid_links = []
    links = await fetch_links(url)
    print(f"Found {len(links)} links.")

    async with aiohttp.ClientSession() as session:
        tasks = [check_link_status(link, session) for link in links]
        results = await asyncio.gather(*tasks)

    for link, status in results:
        if not str(status).startswith('2'):
            pass
            # print(f"{link} - Status: {status}")
        else:
            valid_links.append(link)
    print(f"Successfully scrape {len(valid_links)} links in the following time intervals: {time.time() - start_time}")
    return valid_links
