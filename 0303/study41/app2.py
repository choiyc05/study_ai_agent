from bs4 import BeautifulSoup
import requests

url = 'https://news.naver.com/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')

main_brick = soup.find('div', class_="main_brick")

divs = main_brick.find('div', class_="grid1_wrap brick-house _brick_gid_wrapper")

parents = divs.find_all('div', class_="brick-vowel _brick_column", recursive=False)
# parent = divs.find('div', class_="brick-vowel _brick_column", recursive=False)

print(parents)

children = parents[1].find_all('div', class_="main_brick_item _channel_main_news_card_wrapper")
# print(f"찾은 자식 요소 개수: {len(children)}")

print(children)

arr = []
i = 0
# for div in divs:
#     if i == 1:
#         print(div)
#     arr.append(div)
#     i = i + 1

# print(arr[1])