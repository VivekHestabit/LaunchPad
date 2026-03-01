import os
import httpx
from dotenv import load_dotenv

load_dotenv()


async def serp_search(query: str) -> dict:
    api_key = os.environ["SERPAPI_KEY"]

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 10
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            "https://serpapi.com/search",
            params=params
        )

    response.raise_for_status()
    return response.json()


def clean_serpapi_results(data: dict) -> str:
    results = data.get("organic_results", [])

    cleaned = []
    for r in results[:5]:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")

        cleaned.append(
            f"SOURCE:"
            f"Title: {title}"
            f"Fact: {snippet}"
            f"URL: {link}"
        )

    return "\n".join(cleaned)


async def search_and_clean(query: str) -> str:
    raw_results = await serp_search(query)
    return clean_serpapi_results(raw_results)