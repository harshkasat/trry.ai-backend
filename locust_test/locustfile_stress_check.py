import subprocess
import os
import time
from typing import List
import signal
import psutil

class ConcurrentLocustRunner:
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.base_dir = "performance_tests/stress_check"
        self.processes = []
        
        # Create necessary directories
        os.makedirs(self.base_dir, exist_ok=True)
        
    def generate_locust_file(self, url: str, index: int) -> str:
        """Generate a unique Locust file for each URL"""
        filename = f"{self.base_dir}/locustfile_{index}.py"
        
        content = f'''
from locust import HttpUser, task, between, events
from datetime import datetime

import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLTestUser(HttpUser):
    wait_time = between(0, 1)
    host = ''  # Base host is empty since we're using full URLs

    @task
    def test_url(self):
        with self.client.get("{url}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {{response.status_code}}")

@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    logger.info("Locust process shutting down...")
    sys.exit(0)

# Log successful requests
@events.request.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    with open("{self.base_dir}/success_log_{index}.csv", "a") as f:
        f.write(f"{{datetime.now()}},{{request_type}},{{name}},{{response_time}},{{response_length}}\\n")

# Log failed requests
@events.request.add_listener
def on_request_failure(request_type, name, response_time, exception, **kwargs):
    with open("{self.base_dir}/failure_log_{index}.csv", "a") as f:
        f.write(f"{{datetime.now()}},{{request_type}},{{name}},{{response_time}},{{exception}}\\n")
'''
        
        with open(filename, 'w') as f:
            f.write(content)
        
        return filename

    def kill_process_tree(self, pid):
        """Kill a process and all its children"""
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            
            # Kill children
            for child in children:
                try:
                    child.kill()
                except psutil.NoSuchProcess:
                    pass
            
            # Kill parent
            try:
                parent.kill()
            except psutil.NoSuchProcess:
                pass
            
        except psutil.NoSuchProcess:
            pass

    def start_locust_process(self, locust_file: str, index: int) -> subprocess.Popen:
        """Start a Locust process for a specific file"""
        csv_base = f"{self.base_dir}/results_{index}"
        
        cmd = [
            'locust',
            '-f', locust_file,
            '--headless',
            '-u', '1000',  # Number of users
            '-r', '100',   # Spawn rate
            '--run-time', '5s',
            f'--csv={csv_base}'
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # preexec_fn=os.setsid  # Create new process group
        )
        return process

    def cleanup(self, signum=None, frame=None):
        """Clean up all running processes"""
        print("\nCleaning up processes...")
        for process in self.processes:
            if process.poll() is None:  # If process is still running
                try:
                    self.kill_process_tree(process.pid)
                except Exception as e:
                    print(f"Error killing process {process.pid}: {e}")

        # Wait for processes to terminate
        for process in self.processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.kill_process_tree(process.pid)

        print("Cleanup completed")


    def run_tests(self):
        """Run Locust tests for all URLs concurrently"""
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)

        try:
            # Start all processes
            for index, url in enumerate(self.urls):
                locust_file = self.generate_locust_file(url, index)
                process = self.start_locust_process(locust_file, index)
                self.processes.append(process)
                print(f"Started Locust process for {url}")
                time.sleep(1)  # Small delay between starts

            # Wait for all processes to complete
            print("\nWaiting for all tests to complete...")
            
            # Set a timeout for the entire test suite
            start_time = time.time()
            timeout = 35
            
            while time.time() - start_time < timeout:
                if all(p.poll() is not None for p in self.processes):
                    break
                time.sleep(1)
            
            # Force cleanup if timeout reached
            self.cleanup()
            return 

        except Exception as e:
            print(f"Error occurred: {e}")
            self.cleanup()

async def run_stress_test(URLS: list):
    print("Running stress test...")
    runner = ConcurrentLocustRunner(urls=URLS)
    result = runner.run_tests()