from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import main, capture_screenshots_for_urls, generate_valid_links


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
    url: str


@app.get("/")
async def hello():
    return {"message": "Hello, World!"}

@app.get("/greeting")
async def greeting():
    return {"message": "Hello, Greet!"}

@app.post("/add_url")
async def add_url_to_fix(url: str):
    try:
        response = await main(target_url=url)
        return {"message": f"URL {url} {response}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/capture_screenshots")
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