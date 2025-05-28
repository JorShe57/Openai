from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class SearchQuery(BaseModel):
    query: str

def scrape_city_website(query):
    base_url = "https://www.cityofwestlake.org" 
    search_url = f"{base_url}/search?q={query.replace(' ', '+')}"
    
    try:
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for result in soup.select("a[href]")[:5]:
            title = result.get_text().strip()
            link = result["href"]
            if title and link:
                if not link.startswith("http"):
                    link = base_url + link
                results.append({"title": title, "url": link})
        
        return results if results else [{"title": "No results found", "url": base_url}]
    except Exception as e:
        return [{"title": "Error retrieving data", "url": base_url, "error": str(e)}]

@app.post("/search_city_website")
def search_city_website(query: SearchQuery):
    results = scrape_city_website(query.query)
    return {"results": results}