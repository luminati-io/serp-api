# SERP API

[![Promo](https://github.com/luminati-io/LinkedIn-Scraper/raw/main/Proxies%20and%20scrapers%20GitHub%20bonus%20banner.png)](https://brightdata.com/products/serp-api) 

This repository provides two approaches for collecting Search Engine Results Page (SERP) data:
1. A free, small-scale Google scraper suitable for basic data collection
2. An enterprise-grade API solution for large-scale, real-time data collection from major search engines

## Table of Contents
- [Free SERP Scraper](#free-serp-scraper)
   - [Input Parameters](#input-parameters)
   - [Implementation](#implementation)
   - [Sample Output](#sample-output)
- [Limitations](#limitations)
- [Bright Data SERP API](#bright-data-serp-api)
   - [Key Features](#key-features)
   - [Getting Started](#getting-started)
   - [Direct API Access](#direct-api-access)
   - [Native Proxy-Based Access](#native-proxy-based-access)
- [Query Parameters Overview](#query-parameters-overview)
   - [Google](#google)
     - [Google Search](#1-google-search)
     - [Google Maps](#2-google-maps)
     - [Google Trends](#3-google-trends)
     - [Google Reviews](#4-google-reviews)
     - [Google Lens](#5-google-lens)
     - [Google Hotels](#6-google-hotels)
     - [Google Flights](#7-google-flights)
   - [Bing](#bing)
   - [Yandex](#yandex)
   - [DuckDuckGo](#duckduckgo)
- [Other Settings for SERP API](#other-settings-for-serp-api)
   - [Asynchronous Requests](#asynchronous-requests)
   - [Multi-Query Requests](#multi-query-requests)
- [Support & Resources](#support--resources)

## Free SERP Scraper
[The free scraper](https://github.com/luminati-io/serp-api/tree/main/free_serp_scraper) allows small-scale Google SERP data collection.

<img width="700" alt="google-search" src="https://github.com/user-attachments/assets/9e27ee5c-369b-407f-9e3d-ad65375b48e6" />


### Input Parameters
- **File:** Text file containing search terms (required)
- **Format:** One search term per line

### Implementation
Modify these parameters in the Python file:
```python
# free_serp_scraper/google_serp.py
HEADLESS = False
MAX_RETRIES = 2
REQUEST_DELAY = (1, 4)

with open("search_terms.txt", "r", encoding="utf-8") as file:
    pass
```

### Sample Output
<img width="700" alt="google-serp-data" src="https://github.com/user-attachments/assets/cf187ff9-6a09-4d1a-95c1-5095c3f53f98" />


## Limitations
Google implements several anti-scraping measures:

1. **CAPTCHAs**: Used to differentiate between humans and bots
2. **IP Blocks**: Temporary or permanent bans for suspicious activity
3. **Rate Limiting**: Quick detection and blocking of unidentified requests
4. **Geotargeting**: Results vary by location, language, and device
5. **Honeypot Traps**: Hidden elements to detect automated access

## Bright Data SERP API
[Bright Data's SERP API](https://brightdata.com/products/serp-api) offers a robust solution for reliable SERP data collection.

### Key Features

- Pay-per-successful-request model
- Fast response times
- Location-specific targeting
- Support for multiple device types and search parameters
- Coverage of major search engines (Google, Bing, DuckDuckGo, Yandex, Baidu, Yahoo, Naver)
- Built-in anti-bot solutions
- Real-time results with city-level accuracy
- Structured data output (JSON/HTML)

**Note:** The **SERP API** is part of [**Bright Data’s Web Scraping Suite**](https://docs.brightdata.com/scraping-automation/introduction) and includes full proxy management, unblocking, and parsing capabilities.

### Getting Started

1. **Prerequisites:**
    - Create a [Bright Data account](https://brightdata.com/) (New users receive a $5 credit)
    - Obtain your [API key](https://docs.brightdata.com/general/account/api-token)
2. **Setting Up SERP API:** Follow the [step-by-step guide](https://github.com/triposat/SERP-API/blob/main/setup_serp_api.md) to set up the new SERP API in your Bright Data account.
3. **Implementation Methods:**
    1. Direct API Access
    2. Native Proxy-Based Access

### Direct API Access
The simplest way to use the API is by making a direct request.

**cURL Example**
```bash
curl https://api.brightdata.com/request \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_TOKEN" \
  -d '{
        "zone": "ZONE_NAME",
        "url": "https://www.google.com/search?q=ollama&brd_json=1",
        "format": "raw"
      }'
```

**Python Example**
```python
import requests
import json

url = "https://api.brightdata.com/request"

headers = {"Content-Type": "application/json", "Authorization": "Bearer API_TOKEN"}

payload = {
    "zone": "ZONE_NAME",
    "url": "https://www.google.com/search?q=ollama&brd_json=1",
    "format": "raw",
}

response = requests.post(url, headers=headers, json=payload)

with open("serp_direct_api.json", "w") as file:
    json.dump(response.json(), file, indent=4)

print("Response saved to 'serp_direct_api.json'.")
```

👉 See the [full JSON output](https://github.com/triposat/SERP-API/blob/main/serp_api_outputs/serp_direct_api.json)

**Note**: Use `brd_json=1` for parsed JSON or `brd_json=html` for parsed JSON + full nested HTML.

Learn more about parsing results: [SERP API Parsing Guide](https://docs.brightdata.com/scraping-automation/serp-api/parsing-search-results)

### Native Proxy-Based Access
An alternative method using proxy routing.

**cURL Example**
```bash
curl -i \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<CUSTOMER_ID>-zone-<ZONE_NAME>:<ZONE_PASSWORD> \
  -k \
  "https://www.google.com/search?q=ollama"
```

**Python Example**
```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = "brd.superproxy.io"
port = 33335
username = "brd-customer-<customer_id>-zone-<zone_name>"
password = "<zone_password>"
proxy_url = f"http://{username}:{password}@{host}:{port}"

proxies = {"http": proxy_url, "https": proxy_url}

url = "https://www.google.com/search?q=ollama"
response = requests.get(url, proxies=proxies, verify=False)

with open("serp_native_proxy.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Response saved to 'serp_native_proxy.html'.")
```

👉 See the [full HTML output](https://github.com/triposat/SERP-API/blob/main/serp_api_outputs/serp_native_proxy.html)

**SSL Certificate**: Load Bright Data’s SSL certificate for production. Learn more: [SSL Certificate Guide](https://docs.brightdata.com/general/account/ssl-certificate)

## Query Parameters Overview
Bright Data SERP API lets you tailor requests for multiple search engines—including Google, Bing, Yandex, and DuckDuckGo—using query parameters for localization, pagination, device emulation, and more. This overview provides a high-level look at the API’s capabilities.

> For a complete list and detailed explanation of all query parameters, please refer to the [Detailed Query Parameters Documentation](https://docs.brightdata.com/scraping-automation/serp-api/query-parameters).

### Google
SERP API supports various Google services, including **Search**, **Maps**, **Trends**, **Reviews**, **Lens**, **Hotels**, and **Flights**. Below are key configuration parameters for each service:

#### 1. Google Search
Customize your search results with options for localization, search type, pagination, geolocation, and device targeting.

**Localization**
- `gl`: Country code for the search location (e.g., `gl=us`).
- `hl`: Language code for the results (e.g., `hl=en`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/search?q=pizza&gl=us&hl=en"
```

**Search Type:**
Use the **`tbm`** parameter to specify the search type:

- Images: `tbm=isch`
- Shopping: `tbm=shop`
- News: `tbm=nws`
- Videos: `tbm=vid`

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/search?q=pizza&tbm=shop"
```

**Pagination:**
- `start`: Result offset (0 for the first page, 20 for the second, etc.).
- `num`: Number of results per page (default is 20).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/search?q=pizza&start=20&num=50"
```

**Geolocation:**
- `uule`: Encoded location string for geo-specific results

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/search?q=pizza&uule=w+CAIQICINVW5pdGVkK1N0YXRlcw"
```

**Device Targeting:**
Use the **`brd_mobile`** parameter:

- `0`: Desktop (default)
- `1`: Random mobile
- Specific values: `ios` (or `iphone`), `ipad`, `android`, `android_tablet`

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/search?q=pizza&brd_mobile=1"
```

#### 2. Google Maps
Customize maps queries by specifying coordinates and filtering by accommodation type.

**Coordinates:**
- Format: `@latitude,longitude,zoom` (e.g., zoom from `3z` to `21z`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/maps/search/restaurants/@47.30227,1.67458,14.00z"
```

**Accommodation Search:**

- `brd_accomodation_type`:
    - `hotels` (default)
    - `vacation_rentals`

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/maps/search/hotels+new+york/?brd_accomodation_type=vacation_rentals"
```

#### 3. Google Trends
Retrieve trend data with customizable time ranges and widget options.

**Required Parameters:**

- `brd_json=1`: Return parsed JSON results.
- `brd_trends`: Specify widgets (e.g., `timeseries,geo_map`).

**Time Range:**

- `date`: Defines the time range (e.g., `now 1-d` for the past day).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://trends.google.com/trends/explore?q=pizza&date=now+1-d&brd_trends=timeseries,geo_map&brd_json=1"
```

#### 4. Google Reviews
Fetch reviews using a feature ID and sort them as needed.

**Key Parameters:**

- `fid`: Feature ID from search results.
- `sort`: Sorting order (e.g., `newestFirst`, `ratingHigh`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user "brd-customer-<id>-zone-<name>:<pass>" \
  "https://www.google.com/reviews?fid=0x808fba02425dad8f&sort=newestFirst"
```

#### 5. Google Lens
Search by image using a URL or file upload.

**Image Search:**

- `url`: The image URL to search.
- `brd_json=1`: Return results as JSON.

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://lens.google.com/uploadbyurl?url=https://example.com/image.jpg&brd_json=1"
```

#### 6. Google Hotels
Customize hotel searches with booking dates and currency options.

**Booking Parameters:**

- `brd_dates`: Check-in and check-out dates (`YYYY-MM-DD,YYYY-MM-DD`).
- `brd_currency`: Currency code (e.g., `USD`, `EUR`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/travel/hotels?q=hotels+new+york&brd_dates=2022-01-20,2022-02-05"
```

#### 7. Google Flights
Search for flights using similar localization parameters.

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.google.com/travel/flights?q=flights+new+york&gl=us&hl=en"
```


### Bing
Configure Bing queries with options for localization, geo-targeting, pagination, device and browser targeting, and output formats.

**Localization**

- `setLang`: Language for the interface (e.g., `setLang=en-US`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.bing.com/search?q=pizza&setLang=en-US"
```

**Geo-Location**

- `location`: Search origin (e.g., `location=New+York`).
- `cc`: Country code (e.g., `cc=us`).
- `mkt`: Market code (e.g., `mkt=en-US`).


```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.bing.com/search?q=pizza&location=New+York&cc=us&mkt=en-US"
```

**Pagination**

- `count`: Number of results (e.g., `count=50`).
- `first`: Offset for pagination (e.g., `first=11` for the second page).


```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.bing.com/search?q=pizza&count=50&first=11"
```

**Filters**

- `safesearch`: Adult content filter (e.g., `safesearch=off`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.bing.com/search?q=pizza&safesearch=off"
```

**Device Targeting**

- `brd_mobile`: Specifies the device type (e.g., `brd_mobile=1` for mobile, or `brd_mobile=ios`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.bing.com/search?q=pizza&brd_mobile=1"
```

**Browser Targeting**

- `brd_browser`: Specifies the browser (e.g., `brd_browser=chrome`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.bing.com/search?q=pizza&brd_browser=chrome"
```

**Parsing**

- `brd_json`: Returns parsed JSON (e.g., `brd_json=1`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.bing.com/search?q=pizza&brd_json=1"
```

### Yandex
Briefly configure Yandex queries with parameters for localization, pagination, time range, and device/browser targeting.

**Localization**
- `lr`: Specifies the region (e.g., `lr=84` for the USA).
- `lang`: Page language (e.g., `lang=en`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.yandex.com/search/?text=pizza&lr=84&lang=en"
```

**Pagination**
- `p`: Result page number (e.g., `p=2` for the second page).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.yandex.com/search/?text=pizza&p=2"
```

**Time Range**
- `within`: Specifies the time range (e.g., `within=1`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.yandex.com/search/?text=pizza&within=1"
```

**Device Targeting**
```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.yandex.com/search/?text=pizza&brd_mobile=1"
```

**Browser Targeting**
```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://www.yandex.com/search/?text=pizza&brd_browser=chrome"
```

### DuckDuckGo
A quick overview of DuckDuckGo search customization using localization, safe search, time range, and device/browser targeting.

**Localization**

- `kl`: Country and language (e.g., `kl=us-en`).
- `kad`: Defines the language for interface elements.

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://duckduckgo.com/?q=pizza&kl=us-en"
```

**Safe Search**

- `kp`: Enables safe search (e.g., `kp=1`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://duckduckgo.com/?q=pizza&kp=1"
```

**Time Range**

- `df`: Specifies the time range (e.g., `df=d`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://duckduckgo.com/?q=pizza&df=d"
```

**Device Targeting**

- `brd_mobile`: For mobile device emulation.

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://duckduckgo.com/?q=pizza&brd_mobile=1"
```

**Browser Targeting**

- `brd_browser`: For specifying a browser (e.g., `chrome`).

```bash
curl \
  --proxy brd.superproxy.io:33335 \
  --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
  "https://duckduckgo.com/?q=pizza&brd_browser=chrome"
```

## Other Settings for SERP API

### Asynchronous Requests
- Sync (default): Get a real-time response immediately.
- Async: Retrieve results later (ideal for high-volume requests).

Learn more: [How Async Works](https://docs.brightdata.com/scraping-automation/serp-api/asynchronous-requests#how-it-works)


### Multi-Query Requests
Send **parallel queries** in one API call, sharing the same IP and session using the `multi` parameter.

```python
multi:[
  {"keyword":"shoes","num":50},
  {"keyword":"shoes","num":200}
]
```
Learn more: [Multiple Queries Guide](https://docs.brightdata.com/scraping-automation/serp-api/asynchronous-requests#multiple-queries-in-a-single-request)


## Support & Resources
- **Documentation:** [SERP API Docs](https://docs.brightdata.com/scraping-automation/serp-api/)
- **Query Parameters Documentation:** [Detailed Query Parameters Docs](https://docs.brightdata.com/scraping-automation/serp-api/query-parameters)
- **Other Guides:** [Web Unlocker API](https://github.com/luminati-io/web-unlocker-api), [Google Maps](https://github.com/luminati-io/Google-Maps-Scraper), [Google News](https://github.com/luminati-io/Google-News-Scraper)
- **Technical Support:** [Contact Us](mailto:support@brightdata.com)
