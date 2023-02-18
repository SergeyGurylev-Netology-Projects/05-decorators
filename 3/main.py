import requests
from logger import logger


@logger(3, 5, 'main.log')
def who_is_smartest():
    response = requests.get('https://akabab.github.io/superhero-api/api/all.json')
    downloaded_heroes_list = response.json()
    desired_heroes_list = ['Hulk', 'Captain America', 'Thanos'] # список анализируемых героев
    smartest_hero = {'name': 'Smartest hero not found', 'intelligence': None} # результат - кто самый умный

    desired_heroes_list = [n.lower() for n in desired_heroes_list]

    for hero in downloaded_heroes_list:
        if hero['name'].lower() in desired_heroes_list:
            hero_intelligence = hero['powerstats']['intelligence']
            if smartest_hero['intelligence'] is None or hero_intelligence>smartest_hero['intelligence']:
                smartest_hero['name'] = hero['name']
                smartest_hero['intelligence'] = hero_intelligence

    return smartest_hero


if __name__ == '__main__':
    result = who_is_smartest()
    if result['intelligence'] is None:
        print(result['name'])
    else:
        print(f'Smartest hero is {result["name"]} with intelligence {result["intelligence"]}')
