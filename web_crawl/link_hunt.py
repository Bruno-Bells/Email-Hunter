import re 
import requests
import pandas
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup


def URLS_HUNTER(link):
    urls_list = []
    
    unscraped = deque([link])
    

    while len(unscraped):
        url = unscraped.popleft()
        
        parts = urlsplit(url)
        try:
            base_url = "{0.scheme}://{0.netloc}".format(parts)
        except(requests.exceptions.InvalidSchema):
            pass
        try:
            page = requests.get(base_url)
            new_link = base_url

        except:
            try:
                page = requests.get(f'http://{parts.path}')
                new_link = f'http://{parts.path}'

            except:
                try:
                    page = requests.get(f'https://{parts.path}')
                    new_link = f'https://{parts.path}'
                
                except(requests.exceptions.InvalidSchema, requests.exceptions.InvalidURL, requests.exceptions.ConnectionError) as e:
                    print(e) 
                    pass

        soup = BeautifulSoup(page.content, 'lxml')

        for tag in soup.find_all('a'):
            if 'href' in tag.attrs:
                link = tag.attrs['href']

                if not link.startswith('#') or not link == ' ' or not link.startswith('tel') or not link.startswith('mailto'):
                    social_media = re.match(r'(facebook.com|twitter.com|instagram.com|linkedIn.com|messenger.com)', link)
                    if not social_media:
                        if link.startswith('/'):
                            link = new_link + link
                            urls_list.append(link)

                        elif link.startswith('./'):
                            link = new_link + link[1:]
                            urls_list.append(link)

                        elif not link.startswith('/') and link != ' ' and not link.startswith('https') and not link.startswith('http'):
                            link = new_link + '/' + link
                            urls_list.append(link)

                        elif link.startswith('https') or link.startswith('http'):
                            urls_list.append(link)

                        elif not link.endswith('jpg') or not link.endswith('png'):
                            if not link in unscraped:
                                unscraped.append(link)

            else:
                break


    print(set(urls_list))
    return set(urls_list)

URLS_HUNTER('Tesla.com')
