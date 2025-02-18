import json
import asyncio
import os
from PIL import Image
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
MAX_CONCURRENT_TASKS = 40
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

            try:
                # Process the image (if needed, move this logic to another function for clarity)
                try:
                    image = await asyncio.to_thread(Image.open, save_path)
                except Exception as e:
                    logger.error(f"Error opening image: {e}")
                    return
                issue_identify_by_llm = await ApiClient().generate_content_for_image(image=image)
                response = json.loads(issue_identify_by_llm.text)[0]['response']
                logger.info("LLm successfully processed image")

                # Path for the main JSON file to store all responses
                main_response_file = os.path.join(save_dir, "all_responses.json")

                # Load existing responses if the file exists
                if os.path.exists(main_response_file):
                    with open(main_response_file, 'r') as file:
                        all_responses = json.load(file)
                else:
                    all_responses = []

                # Append the new response
                all_responses.append({"file_path": save_path, "response": response})

                # Save all responses back to the main JSON file
                with open(main_response_file, 'w') as file:
                    json.dump(all_responses, file, indent=4)
                logger.info(f"Response saved to main JSON file: {main_response_file}")
            except Exception as e:
                logger.error(f"Error processing image: {e}")

            return response

        except Exception as e:
            logger.error(f"Error capturing screenshot for {url} on {device}: {e}")

