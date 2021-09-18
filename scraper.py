import requests
from bs4 import BeautifulSoup
import string
import re
import os

col_page = int(input())
article = input()
tot = 0
tot_art = []

for i in range(1, col_page + 1): # list 183
    name_dir = os.path.join('Page_' + str(i))
    if not os.access(name_dir, os.F_OK):
        os.mkdir(name_dir)
    url = ('https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=' + str(i))
    response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(response.content, 'html.parser')
    type_article = soup.find_all('span', attrs = {'class': 'c-meta__type'}, string=article)

    for col in type_article:
        name_article = col.find_previous('div', class_="c-card__body u-display-flex u-flex-direction-column").find('a')
        name_file2 = ''
        for letters in name_article:
            if letters in string.punctuation:
                letters = "_"
            elif letters == r':':
                letters = '_'
            name_file2 += letters
        print(name_file2)
        name_file = name_file2.strip()
        new_name_file = os.path.join(name_file.replace(' ', "_") + r'.txt')
        print(new_name_file)
        link_article = 'https://www.nature.com' + name_article.get('href')
        re_article = requests.get(link_article, headers={'Accept-Language': 'en-US,en;q=0.5'})
        art_soup = BeautifulSoup(re_article.content, 'html.parser')
        path = os.path.join(name_dir, new_name_file)
        file_article = open(path, 'w', encoding='utf-8')
        text_article = art_soup.find('div', class_='c-article-body u-clearfix')
        file_article.write(text_article.text)
        tot_art.append(new_name_file)
        file_article.close()
        tot += 1
        # print('Total = ', tot)
print(tot_art)
