import asyncio
import shutil
import os
import time
import sys
import logging
import json
from typing import Optional, List
from core.scrape.scrape_website_links import fetch_and_check_links
from core.llm.config import ApiClient
from core.automation import device_dimensions, create_stealth_driver
from core.automation.take_screenshot import TakeScreenshot
from core.lighthouse.lighthouse_metrics import performance_metrics
from core.utils import zip_file
from core.pydantic_model import URLModel

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

def generate_valid_links(target_url, file_path: Optional[str] = 'valid_urls.txt'):
    """Scrape and validate links, then generate a summary report using LLM."""
    try:
        start_time = time.time()
        create_dummy_file(file_path)
        links = fetch_and_check_links(target_url)
        if links:
            content = f'Give me links that are important website :- {links} that are very important'
            llm = ApiClient().generate_valdi_urls(content)
            valid_links = json.loads(llm.text)[0]['response'][:4]
            logger.info('Total valid links generate: %d', len(valid_links))

            return valid_links
        logger.info('Generating Valid Links takes %d seconds', time.time() - start_time)
        return valid_links
    except Exception as e:
        logger.error(f"Error generating valid links: {e}")
        return []

async def capture_screenshots_for_urls(target_url:URLModel, screenshot_save_path: Optional[str] = "reports/capture_screenshots"):
    """
    Capture screenshots for multiple URLs and devices asynchronously.
    """
    try:
        start_time = time.time()
        urls = generate_valid_links(target_url.url)

        # Create tasks for each URL and device
        tasks = [
            create_stealth_driver(device=device, url=url, save_dir=screenshot_save_path)
            for url in urls
            for device in device_dimensions
        ]

        # Execute tasks concurrently
        await asyncio.gather(*tasks)

        logger.info(f"Screenshot capturing completed in {time.time() - start_time:.2f} seconds.")
    except Exception as e:
        logger.error(f"Error capturing screenshots: {e}")
    
    # finally:
    #     if os.path.exists(screenshot_save_path):
    #         # Delete the screenshots directory
    #         shutil.rmtree(screenshot_save_path)
    #         logger.info(f"Deleted screenshots directory: {screenshot_save_path}")


async def run_performance_metrics(target_url:URLModel):
    """Run Lighthouse performance metrics."""
    try:
        start_time = time.time()
        await performance_metrics(target_url=target_url)
        logger.info(f"Lighthouse performance metrics completed in {time.time() - start_time} seconds.")
    except Exception as e:
        logger.error(f"Error running Lighthouse performance metrics: {e}")

async def main(target_url:URLModel, save_dir: Optional[str] = "Z:/trryfix.ai/capture_screenshots"):
    try:

        # Step 2: Run all tasks asynchronously
        tasks = [
            capture_screenshots_for_urls(target_url=target_url),
            run_performance_metrics(target_url=target_url),
        ]
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"Error occurred: {e}")


# if __name__ == "__main__":
#     target_url="https://aigrant.com/"
#     # asyncio.run(main(target_url))
#     asyncio.run(capture_screenshots_for_urls([target_url]))
