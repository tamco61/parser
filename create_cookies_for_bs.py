'''
Create cookies for your session (../data/cookies.json).

It is not magic!!!
1) creating session using the requests.
2) using method session.post() with arguments: data(payload), headers(headers).
3) then we take the cookies and write them to a file cookies.json
'''


import requests, json

session = requests.Session()


# do login

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
}


payload = {
	# POST data

	'Login': 'Email',
	'Password': 'Password',
	'RememberMe': 'true'
}


session.post('https://author.today/account/login', data=payload, headers=headers)

with open('cookies.json', 'w') as f:
    json.dump(requests.utils.dict_from_cookiejar(session.cookies), f)