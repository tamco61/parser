from bs4 import BeautifulSoup


def get_information_from_library(soup):
	bookcards = soup.findAll('div', class_='bookcard')
	dct = {
		'books':[]
	}

	for bookcard in bookcards:
		
		# get link on profile book and link on text book
		content = bookcard.find('div', class_='bookcard-content')

		tag = content.find('div', class_='thumb-buttons')
		tags = tag.findAll('a')

		link_on_profile = 'https://author.today' + tags[0].get('href')
		link_on_text = 'https://author.today' + tags[1].get('href')


		# get title book and her author
		footer = bookcard.find('div', class_='bookcard-footer')

		tag = footer.find('h4', 'bookcard-title')
		title = tag.find('a').get_text(strip = True)

		tag = footer.find('h5', 'bookcard-authors')
		author = tag.find('a').get_text(strip = True)


		# get change status
		status = bookcard.find('span', class_='text-success')
		if status is None:
			status = None
		elif status.get_text(strip = True)[0] == '+':
			status = True
		elif status.get_text(strip = True)[0] == '-':
			status = False


		# get image
		image = 'https://author.today' + bookcard.find('img').get('data-src')

		dct['books'].append({
			'title': title,
			'author': author,
			'link_on_text': link_on_text,
			'link_on_profile': link_on_profile,
			'status': status,
			'image': image
			})

	return dct


def get_link_on_library(page_source):
	soup = BeautifulSoup(page_source, 'html.parser')

	tags = soup.findAll('a')
	for tag in tags:
		if 'Моя библиотека' == tag.get_text(strip = True):
			return 'https://author.today' + tag.get('href') + '/all'


def get_chapter_book(soup):
	tag = soup.find('ul', class_='list-unstyled table-of-content')
	chapters = tag.findAll('a')
	lst = []
	for chapter in chapters:
		title = chapter.get_text(strip = True)
		chapterLink = 'https://author.today' + chapter.get('href')
		lst.append({
				'title': title,
				'link_on_chapter': chapterLink
			})
	return lst


def create_html_file_from_webbook(book, session):
	file = open('data/books/' + book['title'] + '.html', 'w', encoding='utf-8')

	chapters = book['chapter']
	response = session.get('https://author.today/reader/37659/301121')
	soup = BeautifulSoup(response.content, 'html.parser')
	s = soup.find('div', class_='text-container')
	print(s)

	file.close()


def clear_text(text):
	result = ''

	for char in text:
		if char != '"':
			result += char

	return result