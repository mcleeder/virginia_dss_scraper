import requests
from lxml.html import fromstring
from scraper import elements, element, contains_string
import asyncio
import aiohttp

def _get_daycare_details_urls() -> list[str]:
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


def _parse_violations(response) -> list[str | None]:
    violation_detail_urls = []

    html_tree = fromstring(response)
    table = element(html_tree, "//b[contains(text(), 'Inspection Date')]/ancestor::table")
    rows = elements(table, "//tr")[1:] # Drop the header row
    for row in rows:
        if cells := elements(row, "//td"):
            violation_cell = cells[-1]
            has_violation = contains_string(violation_cell, "Yes")
            date_in_range = contains_string(cells[0], "2023") or contains_string(cells[0], "2022")
            if date_in_range and has_violation:
                url = element(violation_cell, "//a").attrib.get("href")
                violation_detail_urls.append(f"https://www.dss.virginia.gov{url}")
    return violation_detail_urls

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
    # urls = _get_daycare_details_urls()
    # Debug
    urls = ["https://www.dss.virginia.gov/facility/search/cc2.cgi?rm=Details;ID=35291;search_require_client_code-2101=1"]
    responses = await fetch_urls(urls)
    
    inspections_with_violations = []
    for resp in responses:
        inspections_with_violations += _parse_violations(resp)
    
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
