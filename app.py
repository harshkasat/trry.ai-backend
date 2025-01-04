from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import main


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
        print(url)
        response = await main(target_url=url)
        return {"message": f"URL {url} {response}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
