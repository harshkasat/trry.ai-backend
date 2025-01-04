from selenium import webdriver
import asyncio
from selenium.webdriver.chrome.options import Options
# Define the dimensions for different devices
device_dimensions = {
    'tablet': (768, 1024),  # Tablet (portrait)
    'fold_phone': (540, 960),  # Fold phone (portrait)
    'normal_phone': (375, 667),  # Normal phone (portrait)
    'desktop': (1920, 1080)  # Desktop
}


# Semaphore to limit concurrency
MAX_CONCURRENT_TASKS = 4
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
def create_stealth_driver(device: str):
    """
    Creates a Chrome driver with stealth settings to avoid detection as a bot.
    """
    import time
    start_time = time.time()
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set device emulation, if applicable
    if device == "normal_phone":
        chrome_options.add_argument("--user-agent=some-mobile-user-agent")

    chrome_options.add_argument(f"--window-size={device_dimensions[device][0]},{device_dimensions[device][1]}") # Set window size to 1920x1080


    # chrome_options.add_argument(f"--remote-debugging-port={9222 + hash(device) % 1000}")

    driver = webdriver.Chrome(options=chrome_options)
    print(f"Driver created for {device} in {time.time() - start_time} seconds")

    return driver