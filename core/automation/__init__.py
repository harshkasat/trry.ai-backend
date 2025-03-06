from selenium import webdriver
import os
import time
import logging
import sys
import asyncio
from typing import Optional
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from core.automation.take_screenshot import TakeScreenshot
from dotenv import load_dotenv
load_dotenv()

# Define the dimensions for different devices
device_dimensions = {
    'normal_phone': (375, 667),  # Normal phone (portrait)
    'tablet': (768, 1024),  # Tablet
    'desktop': (1920, 1080),  # Desktop
}
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

# Semaphore to limit concurrency
MAX_CONCURRENT_TASKS = 20
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)  # Adjust MAX_CONCURRENT_TASKS based on system capacity

async def create_stealth_driver(url: str, device: Optional[str] = 'desktop', save_dir: Optional[str] = "Z:/trryfix.ai/capture_screenshots"):
    """
    Creates a Chrome driver with stealth settings and captures a screenshot.
    """
    async with semaphore:  # Limit concurrency
        driver = None
        try:
            start_time = time.time()

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")


            # Create the WebDriver (blocking call)
            if os.getenv('LOCAL_WEBDRIVE'):
                driver = webdriver.Chrome(options=chrome_options)
            else:
                driver = webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                options=chrome_options
                )

            # Capture the screenshot
            screenshot = TakeScreenshot(driver)
            await screenshot.capture_screenshot(url=url, devices=device_dimensions, save_dir=save_dir)

        except Exception as e:
            logger.error(f"Error in create_stealth_driver for {url} on {device}: {e}")
        finally:
            # Ensure the driver is closed
            if driver:
                logger.info(f"Closing driver for {device}")
                driver.quit()
