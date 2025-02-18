import sys
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
from datetime import datetime
import logging
import asyncio
import aiohttp
import statistics
from time import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RequestStats:
    """Keeps track of request statistics"""
    def __init__(self):
        self.response_times: List[float] = []
        self.num_requests: int = 0
        self.num_failures: int = 0
        self.start_time: float = time()
        self.last_request_time: float = 0

    @property
    def avg_response_time(self) -> float:
        return statistics.mean(self.response_times) if self.response_times else 0

    @property
    def median_response_time(self) -> float:
        return statistics.median(self.response_times) if self.response_times else 0

    @property
    def min_response_time(self) -> float:
        return min(self.response_times) if self.response_times else 0

    @property
    def max_response_time(self) -> float:
        return max(self.response_times) if self.response_times else 0

class LoadTester:
    """Manages load testing using aiohttp"""
    def __init__(self):
        self.stats = RequestStats()
        self.session: Optional[aiohttp.ClientSession] = None

    async def make_request(self, url: str) -> None:
        """Make a single request and record statistics"""
        if not self.session:
            raise RuntimeError("Session not initialized")

        start_time = time()
        try:
            async with self.session.get(url) as response:
                await response.read()
                if response.status >= 400:
                    self.stats.num_failures += 1
                else:
                    response_time = (time() - start_time) * 1000  # Convert to milliseconds
                    self.stats.response_times.append(response_time)
                    self.stats.last_request_time = time()
        except Exception as e:
            logger.error(f"Request failed for {url}: {e}")
            self.stats.num_failures += 1
        finally:
            self.stats.num_requests += 1

    async def generate_load(self, url: str, num_requests: int) -> None:
        """Generate load by making multiple concurrent requests"""
        tasks = [self.make_request(url) for _ in range(num_requests)]
        await asyncio.gather(*tasks)

    def save_results(self, url: str) -> None:
        """Save test results to JSON file"""
        report = {
            "target_url": url,
            "total_requests": self.stats.num_requests,
            "total_failures": self.stats.num_failures,
            "average_response_time": self.stats.avg_response_time,
            "median_response_time": self.stats.median_response_time,
            "min_response_time": self.stats.min_response_time,
            "max_response_time": self.stats.max_response_time,
            "timestamp": datetime.now().isoformat(),
            "test_duration": self.stats.last_request_time - self.stats.start_time
        }

        results_dir = Path("reports/break_check")
        results_dir.mkdir(parents=True, exist_ok=True)

        url_part = url.replace('https://', '').replace('http://', '').replace('/', '_').replace('.', '_')
        filename = results_dir / f"{url_part}.json"
        
        with open(filename, "w") as f:
            json.dump(report, f, indent=4)
        logger.info(f"Test results saved to {filename}")

class LoadTestRunner:
    """Manages execution of load tests for multiple URLs"""
    async def run_concurrent_tests(self, urls: List[str], requests_per_url: int = 1000) -> None:
        """Run load tests for multiple URLs concurrently"""
        unique_urls = list(dict.fromkeys(urls))
        logger.info(f"Starting concurrent tests for {len(unique_urls)} URLs")
        
        async with aiohttp.ClientSession() as session:
            for url in unique_urls:
                tester = LoadTester()
                tester.session = session
                
                logger.info(f"Testing {url}")
                await tester.generate_load(url, requests_per_url)
                tester.save_results(url)

async def run_break_test(urls: List[str], requests_per_url: int = 1000):
    """Main entry point for running load tests"""
    if not urls:
        logger.error("No URLs provided")
        return
    runner = LoadTestRunner()
    
    try:
        await runner.run_concurrent_tests(urls=urls, requests_per_url=requests_per_url)
        logger.info("Break tests completed successfully")
    except KeyboardInterrupt:
        logger.info("Tests interrupted by user")
    except Exception as e:
        logger.error(f"Tests failed with error: {e}")


if __name__ == "__main__":
    test_urls = ['https://github.com/harshkasat', 'https://x.com/harsh__kasat', 'https://www.whoisharsh.space/project/inscribeai', 'https://www.whoisharsh.space/project/eudaimonia']
    start = time()
    asyncio.run(run_break_test(test_urls))
    print(f"Total time taken: {time() - start} seconds")