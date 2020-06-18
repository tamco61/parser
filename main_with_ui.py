# Interface with parser

from main import start
from create_cookies_for_bs import create_cookies_for_bs
from modules import empty_cookies
from settings import PATH_TO_COOKIES, REMEMBER


def start_program():
	func_lst = ['']

	print('Ready!!!')
	authorization()
	start()


# Set LOGIN and PASSWORD for settings.py
def set_setting():
	login = input('Write your login: ').strip()
	password = input('Write your password: ').strip()

	with open('settings.py', 'r') as f:
		text = f.readlines()
		for i in range(len(text)):
			row = text[i]
			if 'LOGIN' in row:
				spliter = row.find('=')
				row = row[: spliter + 1] + ' ' + f'"{login}"' + '\n'
				text[i] = row
			elif 'PASSWORD' in row:
				spliter = row.find('=')
				row = row[: spliter + 1] + ' ' + f'"{password}"' + '\n'
				text[i] = row

	with open('settings.py', 'w') as f:
		f.write(''.join(text))

	return login, password


# Get LOGIN and PASSWORD for settings.py
def get_setting():
	with open('settings.py', 'r') as f:
		text = f.readlines()
		for i in range(len(text)):
			row = text[i]
			if 'LOGIN' in row:
				spliter = row.find('=')
				LOGIN = ''.join([i for i in row[spliter + 2 :] if i not in ['"', "'"]]).strip()
			elif 'PASSWORD' in row:
				spliter = row.find('=')
				PASSWORD = ''.join([i for i in row[spliter + 2 :] if i not in ['"', "'"]]).strip()
	return LOGIN, PASSWORD


# Set for settings.py and get true REMEMBER
def set_and_get_remember(arg):
	if arg.lower() == 'y':
		arg = True
	else:
		arg = False

	with open('settings.py', 'r') as f:
		text = f.readlines()
		for i in range(len(text)):
			row = text[i]
			if 'REMEMBER' in row:
				spliter = row.find('=')
				row = row[: spliter + 1] + ' ' + f'{arg}' + '\n'
				text[i] = row

	with open('settings.py', 'w') as f:
		f.write(''.join(text))

	return arg


def authorization():
	# cycle is runs while users not write true login and password
	while True:
		
		if not REMEMBER:
		# if not users and REMEMBER == False 
			LOGIN, PASSWORD = set_setting()
		else:
			LOGIN, PASSWORD = get_setting()

		res = create_cookies_for_bs(LOGIN, PASSWORD, PATH_TO_COOKIES)

		if res[0]:
			print('Authorization was successful!')
			break
		else:
			print('\n'.join(res[1]))

	# change REMEMBER
	if not REMEMBER:
		set_remember(input('Do you want me to remember you? [Y/N]\n'))
			
		
if __name__ == '__main__':
	start_program()



