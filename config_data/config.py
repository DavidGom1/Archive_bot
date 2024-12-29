import json

# importamos le archivo de datos de configuracion
# (leer readme.md para mas informacion)
with open('config_data/config_data.json') as f:
    config_data = json.load(f)

TOKEN = config_data['TOKEN']
local_path = config_data['local_path']
chat_id = [config_data['chat_id_1'], config_data['chat_id_2'], config_data['chat_id_3'], config_data['chat_id_4']]