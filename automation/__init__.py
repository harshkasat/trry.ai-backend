from selenium import webdriver
import time
import logging
import sys
import asyncio
from typing import Optional
from selenium.webdriver.chrome.options import Options
from automation.take_screenshot import TakeScreenshot
# Define the dimensions for different devices
device_dimensions = {
    'normal_phone': (375, 667),  # Normal phone (portrait)
    'desktop': (1920, 1080)  # Desktop
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

async def create_stealth_driver(device: str, url: str, save_dir: Optional[str] = "Z:/trryfix.ai/capture_screenshots"):
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

            # Device-specific settings
            if device == "normal_phone":
                chrome_options.add_argument("--user-agent=some-mobile-user-agent")

            chrome_options.add_argument(f"--window-size={device_dimensions[device][0]},{device_dimensions[device][1]}")

            # Create the WebDriver (blocking call)
            driver = webdriver.Chrome(options=chrome_options)
            logger.info(f"Driver created for {device} in {time.time() - start_time:.2f} seconds")

            # Capture the screenshot
            screenshot = TakeScreenshot(driver)
            json_response = await screenshot.capture_screenshot(url, device, save_dir)
            return json_response


        except Exception as e:
            logger.error(f"Error in create_stealth_driver for {url} on {device}: {e}")
        finally:
            # Ensure the driver is closed
            if driver:
                logger.info(f"Closing driver for {device}")
                driver.quit()
