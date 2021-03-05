import requests, json
from bs4 import BeautifulSoup

r = requests.get('https://covidtracking.com/data')
soup = BeautifulSoup(r.text, 'html.parser')
state_links = [[i['href'].split('/')[-1], f"https://covidtracking.com{i['href']}"] for i in soup.find_all('a', string='Full state data including data sources and notes')]
for state, link in state_links:
	r = requests.get(f'https://covidtracking.com/data/download/{state}-history.csv')
	soup = BeautifulSoup(r.text, 'html.parser')
	with open('state_data/{}.csv'.format(state), 'w') as state_writer:
		print(soup.text)
		state_writer.write(soup.text)
		state_writer.close()
	print(state)

with open('state_name_list.json', 'w') as state_writer:
	state_writer.write(json.dumps([i[0] for i in state_links]))
	state_writer.close()
	