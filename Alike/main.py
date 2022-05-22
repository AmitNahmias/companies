import requests
from bs4 import BeautifulSoup
import codecs

response = requests.get('https://www.ynet.co.il/news/category/184')
with open('test.html', 'wb') as file_handler:
    file_handler.write(response.content)
g = codecs.open('test.html', 'r', encoding='utf8')
f = g.read()
while True:
    # if end == '<div class="itemToggler toOpen">'
    start = f.find('<div class="title">')  # + 7
    end = f[start:].find('</div>')  # - 1
    paragraphs = f[start:start + end]
    print(paragraphs)
    f = f[start + end:]
    if start == 0:
        break

g.close()

# result = BeautifulSoup(response.content).get_text("\n")
# print(result)
