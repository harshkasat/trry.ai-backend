import asyncio
import time
from core.suss_file import generate_valid_links
import logging
from core.pydantic_model import URLModel
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

async def load_test_main(target_url: URLModel, load_test_source_path: Optional[str] = "reports/performance_tests"):
    try:
        start_time = time.time()
        tasks = []
        logger.info("Starting performance tests...")
        target_urls = generate_valid_links(target_url.url)

        from core.break_test import run_break_test
        from core.locust_test.locustfile_stress_check import run_stress_test
        tasks = [
            run_break_test(urls=target_urls),
            run_stress_test(urls=target_urls)
        ]
        await asyncio.gather(*tasks)
        logger.info(f"Performance tests completed in {time.time() - start_time} seconds.")
    except Exception as e:
        logger.error(f"Error running performance tests: {e}")


# if __name__ == "__main__":
#     target_urls = [
#         "https://www.tryfix.ai/",
#     ]
#     asyncio.run(load_test_main(target_urls=target_urls))
