#  Author.Today parser
#  create by tamco6
#  
from bs4 import BeautifulSoup
import requests
import json
import modules


# create session

session = requests.Session()


# apply your cookies from data folder

with open('cookies.json') as f:
    session.cookies.update(json.load(f))

def get_info():
	# get link on "My library" in author.today

	page_source = session.get('https://author.today/').content

	libraryLink = modules.get_link_on_library(page_source)

	# get information for library

	response = session.get(libraryLink)
	soup = BeautifulSoup(response.content, 'html.parser')

	datadict = modules.get_information_from_library(soup)


	print(datadict)
	# write info for library in json file
	with open('data.json', 'w', encoding='utf-8') as f:
		json.dump(datadict, f)



get_info()

