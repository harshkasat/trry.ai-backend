import time
import json
import asyncio
import os
import errno
from PIL import Image

from selenium.webdriver.support.ui import WebDriverWait
from llm.config import ApiClient

# Semaphore to limit concurrency
MAX_CONCURRENT_TASKS = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

class TakeScreenshot:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    async def get_screenshot(self, url, filename=None):
        """Async function to take a screenshot."""
        try:
            await asyncio.to_thread(self.driver.get, url)
            # await asyncio.sleep(0.5)  # Allow async sleep
            await asyncio.to_thread(self.driver.save_screenshot, filename)
            print(f"Screenshot saved as {filename}")

            # Pass image processing back to async context
            image = await asyncio.to_thread(Image.open, filename)
            issue_identify_by_llm = await ApiClient().generate_content_for_image(image=image)

            return json.loads(issue_identify_by_llm.text)[0]['response']
            
        except Exception as e:
            print(f"Error saving screenshot: {e}")
        finally:
            await asyncio.to_thread(self.driver.quit)
            

    async def capture_screenshot(self, url, device, save_dir):
        """Async function to capture screenshot for a URL with specific device dimensions."""
        async with semaphore:
            try:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            file_name = f"{device}_{str(url).split('//')[1].split('/')[0]}.png"
            save_path = os.path.join(save_dir, file_name)
            await self.get_screenshot(url, save_path)

