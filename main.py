from fastapi import FastAPI, HTTPException,Header,Depends
from scraper import ScrapeRequest,Product,scrape_catalogue
from typing import List,Optional
from service import segregate_products

app = FastAPI()

STATIC_TOKEN = "anYzl87!^%vsia8"

@app.get("/")
def index():
    return {
        "message":"Welcome!"
    }

def authenticate(token: Optional[str] = Header(None)):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Token")

@app.post("/scrape", response_model=List[Product])
async def scrape(request: ScrapeRequest, token: str = Depends(authenticate)):
    products = scrape_catalogue(request.base_url, request.page_limit, request.proxy_string)
    
    #check which products need to be updated in db
    segregate_products(products=products)    

    return {
        "message":"Data has been scraped, please check database."
    }