import httpx
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

async def fetch_links(url):
    """Fetch and parse all links from the given URL."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            await asyncio.sleep(2)  # Simulate delay
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
            return links
        except Exception as e:
            print(f"Error fetching links from {url}: {e}")
            return []

async def check_link_status(link, client):
    """Check the status code of a link using a HEAD request."""
    try:
        response = await client.head(link, timeout=10.0)
        return link, response.status_code
    except Exception as e:
        return link, f"Error: {e}"

async def scrape_and_validate_links(url):
    """Scrape links and validate them asynchronously."""
    start_time = time.time()
    valid_links = []
    links = await fetch_links(url)
    print(f"Found {len(links)} links.")

    try:
        async with httpx.AsyncClient() as client:
            tasks = [check_link_status(link, client) for link in links]
            results = await asyncio.gather(*tasks)

        for link, status in results:
            if not str(status).startswith('2'):
                pass
                # print(f"{link} - Status: {status}")
            else:
                valid_links.append(link)
        print(f"Successfully scraped {len(valid_links)} valid links in {time.time() - start_time} seconds.")
        return valid_links
    except Exception as e:
        print(f"Error generating valid links: {e}")
        return []

async def main(url):
    await scrape_and_validate_links(url)

if __name__ == "__main__":
    asyncio.run(main(url="https://aigrant.com/"))
