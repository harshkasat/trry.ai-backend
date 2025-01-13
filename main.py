import asyncio
import aiofiles
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
from locust_test.locustfile_break_check import run_break_test
from locust_test.locustfile_stress_check import run_stress_test
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


async def performance_test(URLS):
    """Run performance tests asynchronously."""
    try:
        start_time = time.time()
        file_path = 'performance_tests'
        await asyncio.gather(
            run_break_test(URLS=URLS, run_time=5),
            run_stress_test(URLS=URLS, run_time=5)
        )
        logger.info(f"Performance tests completed in {time.time() - start_time} seconds.")
    except Exception as e:
        logger.error(f"Error running performance tests: {e}")
    finally:
        shutil.make_archive(file_path, 'zip', file_path)

async def generate_valid_links(target_url):
    """Scrape and validate links, then generate a summary report using LLM."""
    try:
        start_time = time.time()
        links = await scrape_and_validate_links(target_url)
        if links:

            content = f'Give me links that are important website :- {links} that are very important'
            llm = ApiClient().generate_content(content)
            valid_links = json.loads(llm.text)[0]['response'][:4]

            # Write links to valid_urls.txt asynchronously
            async with aiofiles.open('valid_urls.txt', 'w') as file:
                await file.writelines([f"{link}\n" for link in valid_links])
            
            logger.info(f"Generated valid links in {time.time() - start_time} seconds.")
            return valid_links
        else:
            logger.info("No valid links found. Exiting...")
            # Write links to valid_urls.txt asynchronously
            async with aiofiles.open('valid_urls.txt', 'w') as file:
                await file.writelines(target_url)

            return target_url

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

async def main(target_url):
    try:
        save_dir = "Z:/trryfix.ai/capture_screenshots"
        os.makedirs(save_dir, exist_ok=True)

        # target_url = "https://aigrant.com/"
        start_time = asyncio.get_event_loop().time()

        # Step 1: Scrape and validate links
        valid_links = await generate_valid_links(target_url)
        if not valid_links:
            logger.info("No valid links found. Exiting...")
            return

        # Step 2: Run all tasks asynchronously
        tasks = [
            capture_screenshots_for_urls(valid_links),
            performance_test(valid_links),
            run_performance_metrics(target_url)
        ]
        await asyncio.gather(*tasks)

        elapsed_time = asyncio.get_event_loop().time() - start_time
        logger.info(f"Process completed in {elapsed_time:.2f} seconds!")
        response = "The Task is done successfully"
        return response
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        sys.exit(0)
        os.remove(save_dir)



if __name__ == "__main__":
    target_url="https://aigrant.com/"
    asyncio.run(main(target_url="https://aigrant.com/"))
    # asyncio.run(generate_valid_links(target_url))    