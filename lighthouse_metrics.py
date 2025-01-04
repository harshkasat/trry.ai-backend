
import aiohttp
import asyncio
import json

# # Start time
# start_time = time.time()
# json_string = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://www.tryfix.ai/").json()
# # End time


async def fetch(url):
    google_api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + url
    async with aiohttp.ClientSession() as session:
        async with session.get(google_api) as response:
            print("Successfully fetched")
            return await response.json()

# url = "https://example.com"  # Replace with your URL
# asyncio.run(fetch(url))


# print(f"PageSpeed API execution time: {time.time() - start_time} seconds")


class PerformanceMetrics(object):
    def __init__(self, json_string: json) -> None:
        self.json_string =json_string
    
    async def get_loading_metrics(self):
        print("Loading metrics")
        # Extract key loading metrics
        loading_experience_metrics = self.json_string['loadingExperience']['metrics']
        print("Key Performance Metrics:")
        print(f"  Cumulative Layout Shift Score: {loading_experience_metrics['CUMULATIVE_LAYOUT_SHIFT_SCORE']}")
        print(f"  First Contentful Paint: {loading_experience_metrics['FIRST_CONTENTFUL_PAINT_MS']} ms")
        print(f"  Interaction to Next Paint: {loading_experience_metrics['INTERACTION_TO_NEXT_PAINT']} ms")

    async def get_lighthouse_metrics(self):
        # Extract key lighthouse_metrics
        print("Lighthouse metrics")
        lighthouse_metrics = self.json_string['lighthouseResult']['audits']['metrics']['details']['items'][0]
        print(f"  Lighthouse First Contentful Paint: {lighthouse_metrics['firstContentfulPaint']} ms")
        print(f"  Lighthouse Largest Contentful Paint: {lighthouse_metrics['largestContentfulPaint']} ms")
        print(f"  Lighthouse Speed Index: {lighthouse_metrics['speedIndex']}")
        print(f"  Lighthouse Total Blocking Time: {lighthouse_metrics['totalBlockingTime']} ms")

    async def lighthouse_audit_issues(self):
        # Extract Lighthouse audit issues
        print("Lighthouse Audit")
        audits = self.json_string['lighthouseResult']['audits']
        for audit_name, audit_data in audits.items():
            if audit_data.get('score') != None and audit_data.get('score') < 1:
                print(f"Lighthouse Audit Issue: {audit_data['title']}")
                print(f"  Description: {audit_data['description']}")

async def performance_metrics(url:str):
    # url = 'https://www.tryfix.ai/'
    json_string = await fetch(url)
    metrics = PerformanceMetrics(json_string)

    # Run all tasks concurrently
    await asyncio.gather(
        metrics.get_loading_metrics(),
        metrics.get_lighthouse_metrics(),
        metrics.lighthouse_audit_issues()
    )

# if __name__ == '__main__':
#     asyncio.run(main())

