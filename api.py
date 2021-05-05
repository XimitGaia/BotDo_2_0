# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))
root_path = str(path.parents[0])

import flask
from flask import request, jsonify
from database.sqlite import Database
from flask_cors import CORS, cross_origin
import sys
import json
import requests
from bs4 import BeautifulSoup
import re
import base64
from bot_starter import run
app = flask.Flask(__name__)
app.config["DEBUG"] = True
database = Database()
CORS(app)



@app.route('/', methods=['GET'])
def home():
    return '''<h1>API DOFUS</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@cross_origin()
@app.route('/bot_api/resources', methods=['GET'])
def get_resources():
    database = Database()
    sql = f"""SELECT * FROM harvestables_list"""
    resources = database.query(sql=sql)
    return jsonify(resources)

@cross_origin()
@app.route('/bot_api/monsters', methods=['GET'])
def get_monsters():
    database = Database()
    sql = f"""SELECT * FROM monsters"""
    monsters = database.query(sql=sql)
    filtered_monsters = []
    for monster in monsters:
        values = [monster[1],monster[2]]
        if values not in filtered_monsters:
            filtered_monsters.append(values)

    return jsonify(filtered_monsters)

def check_recived_data(data,valid_accounts,selects):
    if data['selects'] == None:
        return 'No selection was made.'
    for account in data['accounts']:
        if len(account) == 1:
            continue
        if account['status'] == 'empty':
            continue
        if 1 < len(account) < 4 :
            return 'Please check your account'
        for value in account.values():
            if value == '':
                return 'Please check your account'
        valid_accounts.append({
            'login': account['login'],
            'password': account['password'],
            'name': account['name']
        })
    for select in data['selects']:
        selects.append(select['value'])
    if valid_accounts == []:
        if selects == []:
            return 'No selection was made and no accounts where given.'
        return 'No accounts where given.'
    if selects == []:
        return 'No selection was made.'
    return 'OK'

def get_dofus_image(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    result = requests.get(url,headers).content
    return base64.b64encode(result).decode('utf-8')

def scraping_character_profile(soup, character_info):
    fullSizeImage_url = soup.select_one('.ak-character-picture > div').get('style').split(')')[0].split('(')[-1]
    avatarImage_url = soup.select_one('.ak-directories-icon > div').get('style').split(')')[0].split('(')[-1]
    fullSizeImage = get_dofus_image(fullSizeImage_url)
    avatarImage = get_dofus_image(avatarImage_url)
    class_name = soup.select_one('.ak-directories-breed').getText().replace(' ','').replace('\n','')
    server = soup.select_one('.ak-directories-server-name').getText()
    character_info.update({
        'fullSizeImage': fullSizeImage,
        'avatarImage': avatarImage,
        'class': class_name,
        'server': server
    })
    level = soup.select_one('.ak-directories-level')
    if level.select('.ak-omega-level') == []:
        character_info['level'] = level.getText()
        level = re.search(r'(\d+)',level.getText()).group()
        character_info['level'] = level
    else:
        character_info['level'] = 200
    try:
        professions = soup.select_one('.ak-lists-paginable').select('.ak-content')
    except:
         professions = []
    for profession in professions:
        # print(profession.select_one('.ak-text').getText())
        name_prof = profession.select_one('.ak-title > a').getText().replace(' ','').replace('\n','')
        level_prof = profession.select_one('.ak-text').getText()
        level_prof = re.search(r'(\d+)',level_prof).group()
        character_info['professions'].update({name_prof: level_prof})

def scraping_character_characteristics_profile(soup, character_info):
    list_characteristics_divs  = soup.select('div.ak-container.ak-panel.ak-caracteristics-details > div.ak-panel-content > div.ak-caracteristics-table-container.row')
    list_characteristics_divs = list_characteristics_divs[:-1]
    characteristics_map = {
        'Primary characteristics': 'primaryCharacteristics',
        'Secondary characteristics': 'secundaryCharacteristics',
        'Damage': 'damages',
        'Resistances (%)': 'resistences'
    }
    for list_characteristics_div in list_characteristics_divs:
        tables = list_characteristics_div.select('table')
        for table in tables:
            title = table.select_one('thead > tr > th:nth-child(1)')
            title = title.getText()
            rows = table.select('tbody > tr')
            for row in rows:
                tds = row.select('td')
                name = tds[1].getText()
                value = tds[len(tds)-1].getText()
                character_info[characteristics_map.get(title)][name] = value
    print(character_info)


@cross_origin()
@app.route('/bot_api/character_info', methods=['GET', 'POST'])
def get_character_info():
    result_request = request.get_json(force=True)
    character_info = {
        'fullSizeImage': None,
        'avatarImage': None,
        'professions': {},
        'name': result_request.get('character'),
        'level': None,
        'server': None,
        'class': None,
        'primaryCharacteristics': {},
        'secundaryCharacteristics': {},
        'damages': {},
        'resistences': {}
    }
    if result_request.get('login') == '' or result_request.get('password') == '' or result_request.get('character') == '':
        return 'blank'
    result_search = requests.get(
        f"https://www.dofus.com/en/mmorpg/community/directories/character-pages?text={result_request['character']}&character_homeserv%5B%5D={result_request['server']}&character_level_min=0&character_level_max=2340#jt_list",
        headers={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68",
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "en-US,en;q=0.9"
            }
        )
    print(result_search,f"https://www.dofus.com/en/mmorpg/community/directories/character-pages?text={result_request['character']}&character_homeserv%5B%5D={result_request['server']}&character_level_min=0&character_level_max=2340#jt_list")
    search_soup = BeautifulSoup(result_search.text)
    names_founded = search_soup.select('.ak-responsivetable > tbody > tr > td:nth-child(2) > a')
    character_url = None
    for character in names_founded:
        if character.getText() == result_request.get('character'):
            character_url = f"https://www.dofus.com{character.get('href')}"
            break
    if character_url == None:
        return ''
    result_character_page = requests.get(character_url)
    character_page_soup = BeautifulSoup(result_character_page.text)
    scraping_character_profile(character_page_soup , character_info)
    result_character_page = requests.get(f'{character_url}/characteristics')
    character_page_soup = BeautifulSoup(result_character_page.text)
    scraping_character_characteristics_profile(character_page_soup , character_info)
    return character_info



@app.route('/bot_api/selected_data', methods=['GET', 'POST'])
def get_selected_data():
    result_request = request.get_json(force=True)
    print(result_request)
    run(result_request)
    return 'a'

app.run()