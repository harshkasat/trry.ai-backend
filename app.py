from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import main, capture_screenshots_for_urls, generate_valid_links
from lighthouse_metrics import performance_metrics
from async_locust import load_test_main
from typing import Optional

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class URLModel(BaseModel):
    url: Optional[str] = "https://www.tryfix.ai/"


@app.get("/health")
async def health_check():
    return {"message": "Server is running Health Check"}

@app.get("/greeting")
async def greeting():
    return {"message": "Hello, Greet!"}

@app.post("/test_websites_performance/")
async def add_url_to_fix(target_url: URLModel):
    try:
        response = await main(target_url=target_url.url)
        return {"message": f"URL {target_url} {response}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/capture_screenshots_websites/")
async def add_urls_to_fix(target_url : URLModel):
    # Step 1: Scrape and validate links
    valid_links = await generate_valid_links(target_url)
    
    try:
        if isinstance(valid_links, list):
            # Step 2: Run all tasks asynchronously
            await capture_screenshots_for_urls(valid_links, "screenshots")
            return {"message": f"Captured screenshots for {len(valid_links)} URLs"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/load_tests/")
async def load_tests(target_url: URLModel):
    try:
        # Step 1: Scrape and validate links
        valid_links = await generate_valid_links(target_url.url)
        if isinstance(valid_links, list):

            response = await (load_test_main(target_urls=valid_links))
        # return {"message": f"Loaded test results for {target_url.url}: {response}"}
            return {"message": f"Loaded test results for {valid_links[:2]}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/lighthouse_test/")
async def lighthouse_test(target_url: URLModel):
    try:
        print(target_url.url)
        response = await performance_metrics(target_url=target_url.url)
        return {"message": f"Lighthouse test results for {target_url.url}: {response}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))