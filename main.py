import requests
from bs4 import BeautifulSoup
import time
from random import randrange
import json

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
}

def get_articles_urls(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    
    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find('span', class_='navigations').find_all("a")[-1].text)
    articles_urls_list = []
    for page in range(1, pagination_count+1):
        
        url = f'https://hi-tech.news/page/{page}/'
        response = s.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        article_urls = soup.find_all('a', class_='post-title-a')

        for au in article_urls:
            art_url = au.get('href')
            articles_urls_list.append(art_url)
        time.sleep(randrange(2, 5))
        print(f'Done {page}/{pagination_count}')
    
    with open('articles_urls.txt', 'w') as file:
        for url in articles_urls_list:
            file.write(f'{url} \n')
    return 'The action of receiving urls is done'

def get_data(file_path):
    with open(file_path) as file:
        url_list = [line.strip() for line in file.readlines()]
    urls_count = len(url_list)
    s = requests.Session()
    result_data = []

    for url in enumerate(url_list):
        response = s.get(url=url[1], headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        article_title = soup.find('div', class_='post-content').find('h1', class_='title').text.strip()
        article_data = soup.find('div', class_='post-media-full').find('div', title='Дата публикации').text
        article_img = soup.find('div', class_='post-media-full').find('img').get('src')
        article_text = soup.find('div', class_='the-excerpt').text.strip().replace('\n', '')
        result_data.append(
            {
                'original_url': url[1],
                'article_img': 'https://hi-tech.news/' + article_img,
                'article_title': article_title,
                'article_text':article_text,
                'article_data': article_data
        })
        print(f'Done {url[0] + 1} / {urls_count}')

    with open('result.json', 'w') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


        




def main():
    get_articles_urls(url='https://hi-tech.news/')
    get_data('articles_urls.txt')

if __name__ == '__main__':
    main()
