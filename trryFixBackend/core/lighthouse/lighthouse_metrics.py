import requests
import asyncio
import json
import os
from core.utils import sanitize_filename
from core.pydantic_model import URLModel

def fetch(url):
    """Fetch the URL using HTTPX."""
    try:
        google_api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + url
        # timeout = httpx.Timeout(30.0, connect=10.0)
        # async with httpx.AsyncClient(timeout=timeout) as client:
        #     response = await client.get(google_api)
        #     print("Successfully fetched")
        #     return response.json()
        response = requests.get(google_api)
        print("Successfully fetched")
        return response.json()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return {}

class PerformanceMetrics:
    def __init__(self, json_string: json, dynamic_file_path: str) -> None:
        self.json_string = json_string
        self.metrics_results = {}
        self.file_path = dynamic_file_path 

    async def get_loading_metrics(self):
        try:
            print("Loading metrics")
            # Extract key loading metrics
            loading_experience_metrics = self.json_string['loadingExperience']['metrics']
            print("Key Performance Metrics:")
            print(f"  Cumulative Layout Shift Score: {loading_experience_metrics['CUMULATIVE_LAYOUT_SHIFT_SCORE']}")
            print(f"  First Contentful Paint: {loading_experience_metrics['FIRST_CONTENTFUL_PAINT_MS']} ms")
            print(f"  Largest Contentful Paint: {loading_experience_metrics['LARGEST_CONTENTFUL_PAINT_MS']} ms")

            self.metrics_results["loading_metrics"] = {
                "Cumulative Layout Shift Score": loading_experience_metrics['CUMULATIVE_LAYOUT_SHIFT_SCORE'],
                "First Contentful Paint (ms)": loading_experience_metrics['FIRST_CONTENTFUL_PAINT_MS'],
                "Largest Contentful Paint (ms)": loading_experience_metrics['LARGEST_CONTENTFUL_PAINT_MS'],
            }
            # Remove any None values (if extraction failed for a specific metric)
            self.metrics_results["loading_metrics"] = {k: v for k, v in self.metrics_results["loading_metrics"].items() if v is not None}
        except Exception as e:
            print(f"Error extracting loading metrics: {e}")

    async def get_lighthouse_metrics(self):
        try:
            # Extract key lighthouse_metrics
            print("Lighthouse metrics")
            lighthouse_metrics = self.json_string['lighthouseResult']['audits']['metrics']['details']['items'][0]
            print(f"  Lighthouse First Contentful Paint: {lighthouse_metrics['firstContentfulPaint']} ms")
            print(f"  Lighthouse Largest Contentful Paint: {lighthouse_metrics['largestContentfulPaint']} ms")
            print(f"  Lighthouse Speed Index: {lighthouse_metrics['speedIndex']}")
            print(f"  Lighthouse Total Blocking Time: {lighthouse_metrics['totalBlockingTime']} ms")

            self.metrics_results["lighthouse_metrics"] = {
                "Lighthouse First Contentful Paint (ms)": lighthouse_metrics['firstContentfulPaint'],
                "Lighthouse Largest Contentful Paint (ms)": lighthouse_metrics['largestContentfulPaint'],
                "Lighthouse Speed Index": lighthouse_metrics['speedIndex'],
                "Lighthouse Total Blocking Time (ms)": lighthouse_metrics['totalBlockingTime'],      
            }
            # Remove any None values (if extraction failed for a specific metric)
            self.metrics_results["lighthouse_metrics"] = {k: v for k, v in self.metrics_results["lighthouse_metrics"].items() if v is not None}
        except Exception as e:
            print(f"Error extracting lighthouse metrics: {e}")

    async def lighthouse_audit_issues(self):
        try:
            # Extract Lighthouse audit issues
            print("Lighthouse Audit")
            audit_issues = {}
            audits = self.json_string['lighthouseResult']['audits']
            for audit_name, audit_data in audits.items():
                if audit_data.get('score') is not None and audit_data.get('score') <= 1:
                    print(f"Lighthouse Audit Issue: {audit_data['title']}")
                    print(f"  Description: {audit_data['description']}")
                    audit_issues[audit_name] = {
                        "Title": audit_data['title'],
                        "Description": audit_data['description']
                    }
            self.metrics_results["lighthouse_audit_issues"] = audit_issues
        except Exception as e:
            print(f"Error extracting Lighthouse audit issues: {e}")
    
    async def save_to_json(self):
        try:
            print("Saving Metrics to JSON File...")
            with open(self.file_path, "w") as json_file:
                json.dump(self.metrics_results, json_file, indent=4)
            print(f"Metrics saved successfully to {self.file_path}")
        except Exception as e:
            print(f"Error saving metrics to JSON: {e}")


async def performance_metrics(target_url:URLModel):
    """Run Lighthouse performance metrics."""
    print('light house performance metrics', target_url)
    import time
    start_time = time.time()
    json_string = fetch(target_url.url)

    # Ensure the directory exists
    os.makedirs("reports", exist_ok=True)
    filename = sanitize_filename(target_url.url.__add__(target_url.name)) + '.json'
    file_path = os.path.join("reports", filename)

    metrics = PerformanceMetrics(json_string, dynamic_file_path=file_path)

    # Run all tasks concurrently
    await asyncio.gather(
        metrics.get_loading_metrics(),
        metrics.get_lighthouse_metrics(),
        metrics.lighthouse_audit_issues()
    )
    await metrics.save_to_json()

    print(f"Lighthouse performance metrics completed in {time.time() - start_time} seconds.")
    return file_path

# if __name__ == '__main__':
#     asyncio.run(performance_metrics(target_url='https://aigrant.com/'))
