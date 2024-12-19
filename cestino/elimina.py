import json

# Leggi il file JSON originale
with open('anime_db.json', 'r') as file:
    data = json.load(file)

# Seleziona solo i primi 10 oggetti
data = data[:10]
print(len(data))
# Salva il nuovo file JSON
with open('anime_db.json', 'w') as file:
    json.dump(data, file, indent=2)