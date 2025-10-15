from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    "Referer": 'https://www.amazon.com/',
    "Sec-Ch-Ua": "Not_A Brand",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
}

def get_amazon_data_books(num_books):
    # Base URL of the Amazon search results for data science books
    base_url = f"https://www.amazon.com/s?k=data+engineering+books"

    books = []
    seen_titles = set()  # To keep track of seen titles
    page = 1

    while len(books) < num_books:
        url = f"{base_url}&page={page}"
        print(f"Scrapping page {page}")
        
        # Send a request to the URL
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print("Failed to reach page.")
            break
            
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
            
        # Find book containers (you may need to adjust the class names based on the actual HTML structure)
        book_containers = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        for book in book_containers:
            title_tag = book.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else None

            author_tag = book.find("div", {"class": "a-row a-size-base a-color-secondary"})
            author = author_tag.get_text(strip=True) if author_tag else None

            rating_tag = book.find("span", {"class": "a-icon-alt"})
            rating = rating_tag.get_text(strip=True) if rating_tag else None

            price_tag = book.find("span", {"class": "a-offscreen"})
            price = price_tag.get_text(strip=True) if price_tag else None

            if title not in seen_titles:
                seen_titles.add(title)
                books.append({
                    "Title":title,
                    "Author":author,
                    "Rating":rating,
                    "Price":price
                })
        
        if not book_containers:
            break
        
        page += 1

    df = pd.DataFrame(books[:num_books])
    return df