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
    sql = f"""SELECT * FROM job_resources_list"""
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

@app.route('/bot_api/selected_data', methods=['GET', 'POST'])
def get_selected_data():
    result_request = request.get_json(force=True)
    valid_accounts = []
    selects = []
    result = check_recived_data(
        data=result_request,
        valid_accounts=valid_accounts,
        selects=selects
    )
    arg_to_pass = {"accounts": valid_accounts, "selects": selects, "mode": result_request['mode']}
    if result == 'OK':
        json_str = json.dumps(arg_to_pass).replace('"', '?').replace(' ', '')
        os.system(f"python {root_path}{os.sep}bot_starter.py {json_str}")
    return result

app.run()