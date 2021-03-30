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
    20: 23,
    21: 24,
    22: 25,
    23: 26,
    24: 27,
    25: 29,
    26: 28,
    27: 30,
    28: 31,
    29: 32,
    30: 33,
    31: 34,
    32: 35,
    33: 36,
    34: 37,
    35: 38,
    36: 39,
    37: 40,
    38: 80,
    39: 41,
    40: 42,
    41: 43,
    42: 44,
    43: 46,
    44: 45,
    45: 68,
    46: 67,
    47: 69,
    48: 70,
    49: 71,
    50: 72,
    51: 73,
    52: 74,
    53: 75,
    54: 76,
    55: 77,
    56: 78,
    57: 79,
    58: 1,
    59: 2,
    60: 3,
    61: 4,
    62: 5,
    63: 6,
    64: 7,
    65: 8,
    66: 9,
    67: 10,
    68: 11,
    69: 12,
    70: 13,
    71: 14,
    72: 15,
    73: 16,
    74: 17,
    75: 18,
    76: 19,
    77: 20,
    78: 21,
    79: 22
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
