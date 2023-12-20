import requests
from bs4 import BeautifulSoup
import time
import xml.etree.ElementTree as ET
import csv

def extract_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    tree = ET.fromstring(response.content)
    urls = [url.text for url in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    return urls

def scrape_to_csv(urls, domain, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Content'])

        for url in urls:
            if url.startswith(domain):
                try:
                    print(f"Scraping: {url}")
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    main_content = soup.find('main')
                    if main_content:
                        text_content = main_content.get_text(separator=' ', strip=True)
                        writer.writerow([url, text_content])
                        print("Content saved.")
                    else:
                        print("No main content found.")
                    time.sleep(1)
                except requests.exceptions.RequestException as e:
                    print(f"Error scraping {url}: {e}")

sitemap_url = 'https://www.folkhalsomyndigheten.se/sitemap.xml'
root_domains = ['https://www.folkhalsomyndigheten.se/livsvillkor-levnadsvanor/andts/tillsynsvagledning/alkoholdrycker/utbildningsinsats-om-alkohollagen/',
                'https://www.folkhalsomyndigheten.se/kunskapsprov-om-alkohollagstiftning/']
csv_filename = 'scraped_content.csv'

sitemap_urls = extract_sitemap_urls(sitemap_url)

for domain in root_domains:
    scrape_to_csv(sitemap_urls, domain, csv_filename)

print("Scraping complete.")
