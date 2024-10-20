import requests
import json
import os

def incrementUrl(url: str) -> str:
    url_split = url.split('=')
    base_url = url_split[0]
    page = int(url_split[1])
    next_page = str(page + 1)
    next_url = base_url+'='+next_page

    return next_url

def save_monsters_to_json(monster_list: list, output_file: str):
    with open(output_file, 'w') as json_file:
        json.dump(monster_list, json_file, indent=4)

monster_list = []
output_dir = 'monsters'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "monsters.json")

url = 'https://api.open5e.com/v1/monsters/?page=1'

while url:
    dat = requests.get(url)
    if dat.status_code != 200:
        print(f'Bad response for {url}')
        url = incrementUrl(url)
        continue
    print(url)
    dat = dat.json()
    url = dat['next']

    for monster in dat['results']:
        monster_list.append(monster)

save_monsters_to_json(monster_list, output_file)