import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/"
res = requests.get(url)

print(res)

soup = BeautifulSoup(res.text)
print(soup.title)
print(soup.title.text)

# print(soup.find("h1"))
print(soup.find("h1").get_text(strip=True))

