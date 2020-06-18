from selenium import webdriver
import json
import modules
from bs4 import BeautifulSoup
import os
from clear import convert
import requests
from settings import PATH_TO_COOKIES, PATH_TO_DATA


def start():

	session = requests.Session()


	# do login

	with open(PATH_TO_COOKIES) as f:
	    session.cookies.update(json.load(f))


	with open(PATH_TO_DATA, encoding='utf-8') as f:
	    data = json.load(f)

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(chrome_options=options)

	cookies = [
		{'domain': 'author.today', 'httpOnly': True, 'name': 'CSRFToken', 'path': '/', 'secure': False, 'value': 'z3OgUPGyLe4buBPz15xL0RTc9QpBbNyF46pFnOI0ElO3NZzZ6j4pfaR6IP-4XlZN147-7lIwQdxhxd1bOhJ2-c6EMGk1'}, 
		{'domain': '.author.today', 'expiry': 1596613514, 'httpOnly': False, 'name': '_fbp', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'fb.1.1588837494491.331634666'}, 
		{'domain': 'author.today', 'expiry': 1590047112, 'httpOnly': True, 'name': 'LoginCookie', 'path': '/', 'secure': True, 'value': 'kLKZblgWXLxE-GMcJ_RSN1vnVjgjHa1LSX2YL7W3Noq_8x6H24CyX-CpokQRNxjfQbglt-qBx0J4cTv_BZB_JUUFwnMqZUlZNZhoEJXA46tHs0NWgZu5FUA7G2ltshMAGcMp2iqYBbPBKoEMYYZpWYshPdWSLICsy499SrEU-PzYKIa6JwW2NrRPhSHRAuBp5fHs01t8q6te2N4eu9Ej2Ps_sQ4jP93BmYe0GQqBF1W_P33ufODS-mtt6Q9qpw1xorptaNivDGlmNc-hYS1N2nCXik_7jy3EybA5bCcGdhP4Sdf0PZFw9LP9OeDoo3EJlFr6lzCKM1a5k_-XLud2w7RhEg6FWbg3iGJGbTLFw30mKGwT9OXXhBorsQrBc9Cvrsu0Ze1s_sWbgNgKCsfpjuVIagI_pfAdSf1asQ8Q0NKE6alNgyrVKhLwe513-bewRsptFMD7qjlb3eHUU9z6w9uFj8UjUc7aZ6WlaXrwON2W6MkbyryIA4LpGgeOvReL04vDvcW5mFvTY_AnoYzf5TnM-0BxJDG3vjNlMAi1NeSt4D_Ngg61SnEWeh2H1cJq36FjeO6WCox_bFbwQI_wEs8BhUpuIn7vMDwfY69YaAeMrBL8'},
		{'domain': '.author.today', 'expiry': 1588839314, 'httpOnly': False, 'name': '_ym_visorc_35844850', 'path': '/', 'secure': False, 'value': 'b'},
		{'domain': '.author.today', 'expiry': 1588837554, 'httpOnly': False, 'name': '_gat', 'path': '/', 'secure': False, 'value': '1'},
		{'domain': '.author.today', 'expiry': 1588909495, 'httpOnly': False, 'name': '_ym_isad', 'path': '/', 'secure': False, 'value': '2'},
		{'domain': '.author.today', 'expiry': 1591429493, 'httpOnly': True, 'name': '__cfduid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'd6167ea9fc115566744c2ea127068dad31588837493'}, 
		{'domain': '.author.today', 'expiry': 1620373494, 'httpOnly': False, 'name': '_ym_uid', 'path': '/', 'secure': False, 'value': '1588837495865101731'},
		{'domain': '.author.today', 'expiry': 1651909514, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.1628119607.1588837495'}, 
		{'domain': 'author.today', 'httpOnly': True, 'name': 'ASP.NET_SessionId', 'path': '/', 'secure': False, 'value': 'qzevtcx0ep5xgqy3ab22adj3'}, 
		{'domain': 'author.today', 'expiry': 1588885200, 'httpOnly': False, 'name': 'country_code', 'path': '/', 'secure': False, 'value': 'RU'},
		{'domain': '.author.today', 'expiry': 1620373494, 'httpOnly': False, 'name': '_ym_d', 'path': '/', 'secure': False, 'value': '1588837495'},
		{'domain': '.author.today', 'expiry': 1588923914, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.1730559695.1588837495'}]

	driver.get(url='https://author.today')
	for cookie in cookies:
		driver.add_cookie(cookie)
	driver.get(url='https://author.today')

	lst = [i['title'] for i in data['books']]

	for i in range(len(lst)):
		print(f'{i} {lst[i]}')


	index = int(input())

	try:

		book = data['books'][index]
		response = session.get(book['link_on_profile'])
		soup = BeautifulSoup(response.content, 'html.parser')
		chapters = modules.get_chapter_book(soup)
		book_title = modules.clear_text(book['title'])
	except IndexError:
		print('Такой книги в каталоге нет!')
		chapters = []

	if chapters != []:
		os.mkdir(f'../{book_title}')
		os.mkdir(f'../{book_title}/html')
		os.mkdir(f'../{book_title}/md')

		for chapter in chapters:
			link = chapter['link_on_chapter']
			title = chapter['title']

			driver.get(url=link)
			soup = BeautifulSoup(driver.page_source, 'html.parser')
			text = soup.find('div', class_='text-container').text

			title = modules.clear_text(title)
			with open(f'../{book_title}/html/{title}.html', 'w', encoding='utf-8') as f:
				f.write(driver.page_source)
				f.close()

		convert(book_title)


if __name__ == '__main__':
	start()