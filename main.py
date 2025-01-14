import asyncio
import shutil
import os
import time
import sys
import logging
import json
from typing import Optional
from scrape.scrape_website_links import scrape_and_validate_links
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

async def capture_screenshots_for_urls(urls, save_dir:Optional[str] = "Z:/trryfix.ai/capture_screenshots"):
    """Capture screenshots for multiple URLs and devices asynchronously."""
    try:
        tasks = []
        start_time = time.time()
        for url in urls:
            for device in device_dimensions:
                logger.info(f"Processing {url} for device {device}")
                driver = await asyncio.to_thread(create_stealth_driver, device)
                screenshot = TakeScreenshot(driver)
                tasks.append(screenshot.capture_screenshot(url, device, save_dir))
        await asyncio.gather(*tasks)
        logger.info(f"Screenshot capturing completed in {time.time() - start_time} seconds.")
    except Exception as e:
        logger.error(f"Error capturing screenshots: {e}")
    finally:
        shutil.make_archive(save_dir, 'zip', save_dir)


async def generate_valid_links(target_url):
    """Scrape and validate links, then generate a summary report using LLM."""
    try:
        start_time = time.time()
        links = await scrape_and_validate_links(target_url)
        if links:

            content = f'Give me links that are important website :- {links} that are very important'
            llm = ApiClient().generate_content(content)
            valid_links = json.loads(llm.text)[0]['response'][:4]
            logger.info('Total valid links generate: %d', len(valid_links))
        else:
            logger.info("No valid links found. Exiting...")
            return [target_url]
        logger.info('Generating Valid Links takes %d seconds', time.time() - start_time)
        return valid_links
    except Exception as e:
        logger.error(f"Error generating valid links: {e}")
        return []


async def run_performance_metrics(url):
    """Run Lighthouse performance metrics."""
    try:
        start_time = time.time()
        await performance_metrics(url=url)
        logger.info(f"Lighthouse performance metrics completed in {time.time() - start_time} seconds.")
    except Exception as e:
        logger.error(f"Error running Lighthouse performance metrics: {e}")

async def main(target_url, save_dir: Optional[str] = "Z:/trryfix.ai/capture_screenshots"):
    try:
        os.makedirs(save_dir, exist_ok=True)

        # Step 1: Scrape and validate links
        valid_links = await generate_valid_links(target_url)
        if not valid_links:
            logger.info("No valid links found. Exiting...")
            return

        # Step 2: Run all tasks asynchronously
        tasks = [
            capture_screenshots_for_urls(valid_links),
            run_performance_metrics(target_url),
        ]
        await asyncio.gather(*tasks)
        response = "The Task is done successfully"
        return response
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        sys.exit(0)
        os.remove(save_dir)


if __name__ == "__main__":
    target_url="https://aigrant.com/"
    asyncio.run(main(target_url))
