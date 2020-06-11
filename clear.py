import html2markdown as hm
from bs4 import BeautifulSoup
import os


# while there's fucking magic xD

def convert(book_title):
	
	os.chdir(f'../{book_title}/html')
	files = os.listdir()

	for file in files: 
		with open(file, encoding='utf-8') as f:
			soup = BeautifulSoup(f.read(), 'html.parser')

		text = str(soup.find('div', 'text-container'))
		setting = clear_from_whitespace_in_text(text[:text.find('>') + 1])
		text = clear_from_whitespace_in_text(text[text.find('>') + 1:])
		text = clear_from_span_in_text(hm.convert(text))
		with open(f'../md/{file[:file.find(".")]}.md', 'w', encoding='utf-8') as f:
			f.write(text)


def clear_from_whitespace_in_text(text):
	result = ''
	access = True

	for i in text.strip():
		if i not in [' ', '\n']:
			result += i
			access = True
		elif access:
			result += ' '
			access = False

	return result


def handling_setting(setting):
	setting = setting[setting.find('style='):]
	setting = setting[setting.find('"') + 1:setting.rfind('"')]
	parametrs = dict()

	for parametr in setting.split(';'):
		parametr = parametr.strip()
		key, value = parametr.split(':')
		parametrs[key.strip()] = value.strip()
	parametrs['color'] = 'black'
	return(parametrs)


def clear_from_span_in_text(text):
	access = True
	result = ''
	for index in range(len(text)):
		char = text[index]
		try:
			if char in '<' and text[index + 1] in ['/', 's']:
				access = False
			elif char == '>' and not access:
				access = True
			elif access:
				result += char
		except IndexError:
			pass

	return result