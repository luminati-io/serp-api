import asyncio
import csv
import time
import random
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# Configuration
HEADLESS = False
MAX_RETRIES = 2
REQUEST_DELAY = (1, 4)  # Random delay between requests in seconds

async def scrape_search_element(search_element, rank, search_term):
    try:
        # Extract title
        title_element = await search_element.query_selector("h3")
        title = await title_element.inner_text() if title_element else None

        # Extract URL
        url_element = await search_element.query_selector("a[href]")
        raw_url = await url_element.get_attribute("href") if url_element else None
        parsed_url = urlparse(raw_url)
        if parsed_url.path == "/url" and 'q' in parse_qs(parsed_url.query):
            url = parse_qs(parsed_url.query)['q'][0]
        else:
            url = raw_url

        # Extract description
        description_element = await search_element.query_selector("div[data-content-feature]")
        if not description_element:
            description_element = await search_element.query_selector("div > div > div > div > div > div > span")
        description = await description_element.inner_text() if description_element else None

        return {
            'search_term': search_term,
            'rank': rank,
            'url': url,
            'title': title,
        }
    except Exception as e:
        print(f"Error scraping result {rank}: {str(e)}")
        return None

async def perform_search(page, search_term, current_count, total_terms):
    for attempt in range(MAX_RETRIES):
        try:
            print(f"[{current_count}/{total_terms}] Attempt {attempt+1} for {search_term}...")
            
            await page.goto("https://www.google.com/?hl=en-US", timeout=60000)
            
            # Handle cookie consent
            try:
                await page.wait_for_selector("button:has-text('Accept all')", timeout=5000)
                await page.click("button:has-text('Accept all')")
                await page.wait_for_selector("button:has-text('Accept all')", state="hidden", timeout=3000)
            except:
                pass

            # Perform search
            await page.fill("textarea[aria-label='Search']", search_term)
            await page.keyboard.press("Enter")
            
            # Wait for results
            await page.wait_for_selector("div.g", timeout=15000)
            
            # Random delay to mimic human behavior
            await asyncio.sleep(random.uniform(*REQUEST_DELAY))
            
            # Extract results
            search_elements = await page.query_selector_all("div.g")
            results = []
            for rank, element in enumerate(search_elements, 1):
                result = await scrape_search_element(element, rank, search_term)
                if result:
                    results.append(result)

            print(f"✓ Found {len(results)} results")
            return results

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt == MAX_RETRIES - 1:
                return []
            await asyncio.sleep(2 ** (attempt + 1))

async def main():
    start_time = time.time()
    
    # Read search terms
    with open("free_serp_scraper/search_terms.txt", "r", encoding="utf-8") as file:
        search_terms = [line.strip() for line in file if line.strip()]
    
    print(f"Starting scraper at {datetime.now().strftime('%H:%M:%S')}")
    print(f"Processing {len(search_terms)} search terms")

    # Prepare CSV
    csv_filename = f"serp_data.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["search_term", "rank", "url", "title"])
        writer.writeheader()

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=HEADLESS)
            context = await browser.new_context()
            page = await context.new_page()
            await stealth_async(page)

            for idx, term in enumerate(search_terms, 1):
                results = await perform_search(page, term, idx, len(search_terms))
                if results:
                    writer.writerows(results)
                    csvfile.flush()  # Ensure immediate write
                
                if idx < len(search_terms):
                    delay = random.uniform(*REQUEST_DELAY)
                    await asyncio.sleep(delay)

            await browser.close()

    duration = time.time() - start_time
    print(f"\nCompleted in {duration:.1f}s")
    print(f"Total results: {sum(1 for _ in open(csv_filename)) - 1}")  # Subtract header
    print(f"Saved to: {csv_filename}")

if __name__ == "__main__":
    asyncio.run(main())