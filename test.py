from bs4 import BeautifulSoup
import requests

print(requests.get('https://author.today').content)
print(BeautifulSoup(requests.get('https://author.today').content, 'html.parser'))