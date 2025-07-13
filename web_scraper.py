import requests
from bs4 import BeautifulSoup
import csv


URL = "http://books.toscrape.com/"


# Step 1: Fetch the page content safely
try:
    response = requests.get(URL)
    response.raise_for_status()  # Will throw error for 4xx or 5xx
except requests.exceptions.RequestException as e:
    print(f"❌ Error fetching the page: {e}")
    exit()  # Exit if there’s a problem


# Step 2: Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')
books = soup.select('article.product_pod')


# Step 3: Prepare and write CSV
with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Rating'])


    for book in books:
        # Extract book title
        title_tag = book.h3.a
        title = title_tag.get('title', 'N/A') if title_tag else 'N/A'


        # Extract price
        price_tag = book.find('p', class_='price_color')
        price = price_tag.text.strip() if price_tag else 'N/A'


        # Extract rating
        rating_tag = book.find('p', class_='star-rating')
        rating_classes = rating_tag.get('class', []) if rating_tag else []
        rating = rating_classes[1] if len(rating_classes) > 1 else 'Not Rated'


        writer.writerow([title, price, rating])


print("✅ Scraping complete! Data saved to 'scraped_data.csv'")


