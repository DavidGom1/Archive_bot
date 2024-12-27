import json

# importamos le archivo de datos de configuracion
# (leer readme.md para mas informacion)
with open('config_data/config_data.json') as f:
    config_data = json.load(f)

TOKEN = config_data['TOKEN']