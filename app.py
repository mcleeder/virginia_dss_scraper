import requests
from lxml.html import fromstring
from scraper import elements
import asyncio
import aiohttp

def _get_urls() -> list[str]:
    data_url = "https://www.dss.virginia.gov/facility/search/cc2.cgi"

    form_data = {
        "rm" : "Search",
        "search_keywords_name" : None,
        "search_exact_fips": None,
        "search_contains_zip" : None,
        "search_require_client_code-2101" : 1,
    }

    response = requests.post(url = data_url, data=form_data)

    html_tree = fromstring(response.content)

    raw_anchor_tags = elements(html_tree, "//a[contains(@href, 'code-2101')]")

    return [f"https://www.dss.virginia.gov{x.attrib.get("href")}" for x in raw_anchor_tags]

async def fetch_url(url, retries=3, retry_interval=1):
    while retries:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()
        except aiohttp.ClientConnectorError:
            retries -= 1
            await asyncio.sleep(retry_interval)

async def fetch_urls(urls):
    tasks = []
    async with aiohttp.ClientSession():
        for url in urls:
            task = asyncio.create_task(fetch_url(url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses

async def main():
    urls = _get_urls()
    responses = await fetch_urls(urls)
    for response in responses:
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
