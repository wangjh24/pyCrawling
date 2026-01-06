import requests
from bs4 import BeautifulSoup
import time

# 1️Base URLs
base_url = "https://finance.naver.com"
news_list_url_template = "https://finance.naver.com/item/news_news.naver?code=005930&page={page}&clusterId="

# 2️Headers (must for Naver)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://finance.naver.com/item/main.naver?code=005930"
}

# 3️Use a set to track visited article URLs (to remove duplicates)
visited_links = set()

# 4️Crawl multiple pages
for page in range(1, 4):  # adjust number of pages as needed
    list_url = news_list_url_template.format(page=page)
    res = requests.get(list_url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # 5️Select news titles and links
    news_items = soup.select("td.title a")

    for news in news_items:
        title = news.text.strip()
        relative_link = news["href"]
        full_link = base_url + relative_link

        # 6️Skip duplicates
        if full_link in visited_links:
            continue
        visited_links.add(full_link)

        # 7️Request article page
        article_res = requests.get(full_link, headers=headers)
        article_soup = BeautifulSoup(article_res.text, "html.parser")

        # 8Extract article content
        

        # 9️Print results
        print(title)

        time.sleep(0.5)  # polite delay
