import json

# File JSON da leggere
ANIME_DB_FILE = 'anime_db.json'

# Leggi il file JSON
with open(ANIME_DB_FILE, 'r',errors='ignore') as file:
    data = json.load(file)

# Elimina le chiavi 'characters' e 'staff' da ogni elemento
for item in data:
    if 'characters' in item:
        del item['characters']
    if 'staff' in item:
        del item['staff']

# Riscrivi il file JSON aggiornato
with open(ANIME_DB_FILE, 'w') as file:
    json.dump(data, file, indent=4)
