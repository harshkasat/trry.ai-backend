import asyncio
import shutil
import os
import time
import sys
import logging
import json
from typing import Optional, List
from scrape.scrape_website_links import fetch_and_check_links
from llm.config import ApiClient
from automation import device_dimensions, create_stealth_driver
from automation.take_screenshot import TakeScreenshot
from lighthouse_metrics import performance_metrics

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("script.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

def create_dummy_file(file_path: Optional[str] = 'valid_urls.txt'):

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file if it doesn't exist
        with open(file_path, 'w') as file:
            file.write("")  # Create an empty file
        print(f"File created: {file_path}")
    else:
        print(f"File already exists: {file_path}")

async def capture_screenshots_for_urls(urls, save_dir: Optional[str] = "Z:/trryfix.ai/capture_screenshots"):
    """
    Capture screenshots for multiple URLs and devices asynchronously.
    """
    try:
        start_time = time.time()

        # Create tasks for each URL and device
        tasks = [
            create_stealth_driver(device=device, url=url, save_dir=save_dir)
            for url in urls
            for device in device_dimensions
        ]

        # Execute tasks concurrently
        await asyncio.gather(*tasks)

        logger.info(f"Screenshot capturing completed in {time.time() - start_time:.2f} seconds.")
    except Exception as e:
        logger.error(f"Error capturing screenshots: {e}")

    finally:
        # Create a zip archive of the screenshots
        shutil.make_archive(save_dir, 'zip', save_dir)


def generate_valid_links(target_url, file_path: Optional[str] = 'valid_urls.txt'):
    """Scrape and validate links, then generate a summary report using LLM."""
    try:
        start_time = time.time()
        create_dummy_file(file_path)
        links = fetch_and_check_links(target_url)
        if links:
            content = f'Give me links that are important website :- {links} that are very important'
            llm = ApiClient().generate_content(content)
            valid_links = json.loads(llm.text)[0]['response'][:4]
            logger.info('Total valid links generate: %d', len(valid_links))
            # Write the list to the file line by line
            with open(file_path, 'w') as file:
                for url in valid_links:
                    file.write(url + '\n')
        else:
            # Initialize an empty list
            url_list = []
            # Read the file and append each line to the list
            with open(file_path, 'r') as file:
                for line in file:
                    # Strip newline characters and append to the list
                    url_list.append(line.strip())
            logger.info("No valid links found. Taking url from valid_url Exiting...")
            return url_list
        logger.info('Generating Valid Links takes %d seconds', time.time() - start_time)
        return valid_links
    except Exception as e:
        logger.error(f"Error generating valid links: {e}")
        return []


async def run_performance_metrics(url):
    """Run Lighthouse performance metrics."""
    try:
        start_time = time.time()
        await performance_metrics(target_url=url)
        logger.info(f"Lighthouse performance metrics completed in {time.time() - start_time} seconds.")
    except Exception as e:
        logger.error(f"Error running Lighthouse performance metrics: {e}")

async def main(target_url, save_dir: Optional[str] = "Z:/trryfix.ai/capture_screenshots"):
    try:
        os.makedirs(save_dir, exist_ok=True)

        # Step 1: Scrape and validate links
        valid_links = generate_valid_links(target_url)
        if not valid_links:
            logger.info("No valid links found. Exiting...")
            return

        # Step 2: Run all tasks asynchronously
        tasks = [
            capture_screenshots_for_urls(valid_links),
            # run_performance_metrics(target_url),
        ]
        await asyncio.gather(*tasks)
        response = "The Task is done successfully"
        return response
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        os.remove(save_dir)


# if __name__ == "__main__":
#     target_url="https://aigrant.com/"
#     # asyncio.run(main(target_url))
#     asyncio.run(capture_screenshots_for_urls([target_url]))
