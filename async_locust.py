from gevent import monkey
monkey.patch_all()
import asyncio
import time
import shutil
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

async def load_test_main(target_urls, file_path: Optional[str] = 'performance_tests'):
    try:
        start_time = time.time()
        tasks = []
        logger.info("Starting performance tests...")

        from gevent import monkey
        monkey.patch_all()
        from locust_test.locustfile_break_check import run_break_test
        from locust_test.locustfile_stress_check import run_stress_test
        tasks = [
            run_break_test(urls=target_urls),
            run_stress_test(urls=target_urls)
        ]
        await asyncio.gather(*tasks)
        logger.info(f"Performance tests completed in {time.time() - start_time} seconds.")

    except Exception as e:
        logger.error(f"Error running performance tests: {e}")
    finally:
        shutil.make_archive(file_path, 'zip', file_path)

# if __name__ == "__main__":
#     target_urls = [
#         "https://example.com",
#         "https://anotherexample.com",
#         "https://www.tryfix.ai/",
#         "https://www.whoisharsh.space/",
#     ]
#     asyncio.run(load_test_main(target_urls=target_urls))
