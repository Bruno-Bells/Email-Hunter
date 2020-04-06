import re 
import requests
import pandas as pd
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
from link_hunt import URLS_HUNTER

new_url = input('Enter a URL:  ')

save_as = input('Save as:  ')

list_urls = URLS_HUNTER(new_url)

Unscraped = deque([new_url])

emails = set()

while len(Unscraped):

    url = Unscraped.popleft()
    
    for url_link in list_urls:

        base_url = url_link

        page = requests.get(base_url)

        soup = BeautifulSoup(page.content, 'lxml')

        print("Crawling URL %s " % base_url)
        print()

        for i in range(len(soup.find_all('p'))):
            try:
                text_email = soup.find_all('p')[i].get_text()
                new_emails = set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text_email, re.I))
                emails.update(new_emails)
                df = pd.DataFrame(emails, columns=['Emails'])
                if not new_url.startswith('http'):
                    link = 'http://' + new_url
                    df['URLs'] = link
                    df.to_csv(f'{save_as}.csv', index=False)
                else:
                    df['URLs'] = new_url
                    df.to_csv(f'{save_as}.csv', index=False)

            except (requests.exceptions.ConnectionError, TimeoutError) :
                pass

        for i in range(len(soup.find_all('a'))):
            try:
                text_email = soup.find_all('a')[i].get_text()
                new_emails = set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text_email, re.I))
                emails.update(new_emails)
                df = pd.DataFrame(emails, columns=['Emails'])
                if not new_url.startswith('http'):
                    link = 'http://' + new_url
                    df['URLs'] = link
                    df.to_csv(f'{save_as}.csv', index=False)
                else:
                    df['URLs'] = new_url
                    df.to_csv(f'{save_as}.csv', index=False)

            except (requests.exceptions.ConnectionError, TimeoutError) :
                pass

print(emails)
print()