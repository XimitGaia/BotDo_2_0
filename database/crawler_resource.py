import requests
from sqlite import Database

internal_type_id = {
    1: 47,
    2: 48,
    3: 49,
    4: 50,
    5: 51,
    6: 52,
    7: 53,
    8: 54,
    9: 55,
    10: 56,
    11: 57,
    12: 58,
    13: 59,
    14: 60,
    15: 61,
    16: 62,
    17: 63,
    18: 64,
    19: 65,
}

def get_position_by_resource_id(internal_id: int, internal_type_id: dict):
    url = f'https://dofus-map.com/getRessourceData.php?ressourceId={internal_type_id[internal_id]}&groupId=0'
    result = requests.get(url)
    print(f'Getting dta from {url}')
    response = list()
    if result.status_code == 200:
        full_content = result.text
        full_content_array = full_content.replace('"', '').split('&')
        content = full_content_array[-1]
        full_content_array  = None
        registers = content.split('_')
        content = None
        positions = generate_positions_from_registers(registers)
        for position in positions:
            response.append((
                position.get('x'), 
                position.get('y'), 
                internal_id,
                position.get('quantity'), 
                1
            ))
    return response


def generate_positions_from_registers(registers: list)-> list:
    positions = list()
    for register in registers:
        register_array = register.split('*')
        quantity = register_array[0]
        encode_positon = register_array[1]
        encode_positons_array = encode_positon.split('+')
        for encode_positon_array in encode_positons_array:
            xs = encode_positon_array.split(':')[0]
            ys = encode_positon_array.split(':')[1]
            xs = xs.split(' ')
            ys = ys.split(' ')
            for x in xs:
                for y in ys:
                    positions.append({
                        'x': int(x),
                        'y': int(y),
                        'quantity': int(quantity)
                    })
    return positions

database = Database()
for type_id in internal_type_id:
    rows = get_position_by_resource_id(type_id, internal_type_id)
    for row in rows:
        database.insert_job_resources_location(row=row)
