from bs4 import BeautifulSoup
import requests

url = 'http://127.0.0.1:5500/Study/2603study/0303/study41/index.html'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')

main_brick_item = soup.find('div', class_="main_brick_item")
parents = main_brick_item.find('div', class_="comp_news_feed comp_news_none")
lis_parent = parents.find('ul')
lis = lis_parent.find_all('li')

for li in lis:
    print( li.find("a").text)

