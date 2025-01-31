import time
import json
import asyncio
import os
import errno
from PIL import Image

from selenium.webdriver.support.ui import WebDriverWait
from core.llm.config import ApiClient
import sys
import logging
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
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

class TakeScreenshot:
    def __init__(self, driver):
        self.driver = driver

    async def capture_screenshot(self, url, device, save_dir):
        """Capture screenshot for a URL with specific device dimensions."""
        try:
            # Create directory if it doesn't exist
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # File path for saving the screenshot
            file_name = f"{device}_{str(url).split('//')[1].split('/')[0]}.png"
            save_path = os.path.join(save_dir, file_name)

            # Navigate to URL (blocking call)
            self.driver.get(url)
            logger.info(f"Navigated to {url} on {device}")

            # Save the screenshot (blocking call)
            self.driver.save_screenshot(save_path)
            logger.info(f"Screenshot saved: {save_path}")
            # Process the image (if needed, move this logic to another function for clarity)
            image = await asyncio.to_thread(Image.open, save_path)
            issue_identify_by_llm = await ApiClient().generate_content_for_image(image=image)

            return json.loads(issue_identify_by_llm.text)[0]['response']

        except Exception as e:
            logger.error(f"Error capturing screenshot for {url} on {device}: {e}")

