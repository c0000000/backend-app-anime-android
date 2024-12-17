from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Percorsi dei file
ANIME_FILE_PREFERITI = 'anime-preferiti.json'
ANIME_FILE_LISTA = 'anime-lista.json'
ANIME_FILE_STAGIONALI = 'anime_stagionali.json'
USERS_FILE = 'users.json'

# Inizializza il file anime-preferiti.json se non esiste

@app.route('/')
def index():
    # Restituisce un template HTML
    return render_template('index.html')


@app.route('/add-anime', methods=['POST'])  # Endpoint per aggiungere anime preferiti
def add_anime():
    try:
        # Legge i dati dalla richiesta
        data = request.json

        # Controlla che i dati contengano i campi richiesti
        if not data or 'idUtente' not in data or 'idAnime' not in data:
            return jsonify({"error": "Dati non validi. Sono richiesti 'idUtente' e 'idAnime'."}), 400

        id_utente = data['idUtente']
        id_anime = data['idAnime']

        # Carica i dati esistenti dal file
        with open(ANIME_FILE_PREFERITI, 'r') as file:
            preferiti = json.load(file)

        # Trova o crea l'utente nel file preferiti
        utente_esistente = next((item for item in preferiti if item['idUtente'] == id_utente), None)

        if utente_esistente:
            # Aggiunge l'idAnime alla lista dell'utente, evitando duplicati
            if id_anime not in utente_esistente['idAnime']:
                utente_esistente['idAnime'].append(id_anime)
        else:
            # Crea un nuovo utente con il suo primo anime preferito
            preferiti.append({
                "idUtente": id_utente,
                "idAnime": [id_anime]
            })

        # Scrive i dati aggiornati nel file
        with open(ANIME_FILE_PREFERITI, 'w') as file:
            json.dump(preferiti, file, indent=4)

        return jsonify({"message": "Anime aggiunto con successo!", "data": data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        # Carica il file users.json
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)

        # Legge email e password dalla richiesta
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Cerca un utente con le credenziali fornite
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)

        if not user:
            return jsonify({"error": "Credenziali non valide"}), 401

        # Legge e restituisce il file associato all'utente
        try:
            with open(user['data_file'], 'r') as data_file:
                user_data = json.load(data_file)
            return jsonify(user_data), 200
        except FileNotFoundError:
            return jsonify({"error": "File associato non trovato"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/anime-stagionali', methods=['GET'])
def get_anime_stagionali():
    try:
        # Ottieni il percorso assoluto del file
        file_path = os.path.abspath('anime_stagionali.json')
        print("Percorso del file:", file_path)  # Stampa il percorso per il debug

        with open(file_path, 'r') as file:
            data = file.read()
        return data, 200, {'Content-Type': 'application/json'}
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/anime/<nome_anime>', methods=['GET'])
def get_anime_from_nome(nome_anime):
    try:
        # Legge il file JSON con la lista degli anime
        with open(ANIME_FILE_LISTA, 'r') as file:
            anime_list = json.load(file)

        # Cerca l'anime corrispondente al nome dato
        risultato = next((anime for anime in anime_list if anime['nome'].lower() == nome_anime.lower()), None)

        if risultato:
            return jsonify(risultato), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({"error": "Anime non trovato"}), 404

    except FileNotFoundError:
        return jsonify({"error": "File non trovato"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/anime/preferiti/<id_utente>', methods=['GET'])
def get_anime_preferiti(id_utente):
    try:
        # Converte id_utente in un numero intero
        id_utente = int(id_utente)

        # Legge il file anime-preferiti.json
        with open(ANIME_LISTA_PREFERITI, 'r') as file_preferiti:
            preferiti = json.load(file_preferiti)

        # Trova l'utente specificato
        utente = next((u for u in preferiti if u['idUtente'] == id_utente), None)

        if not utente:
            return jsonify({"error": f"Nessun preferito trovato per l'utente con id {id_utente}."}), 404

        # Ottieni gli ID degli anime associati all'utente
        id_anime_list = utente.get('idAnime', [])

        # Legge il file anime-lista.json
        with open(ANIME_LISTA_LISTA, 'r') as file_lista:
            anime_lista = json.load(file_lista)

        # Trova gli anime corrispondenti agli ID
        risultati = [anime for anime in anime_lista if anime.get('idAnime') in id_anime_list]

        return jsonify(risultati), 200

    except FileNotFoundError as e:
        return jsonify({"error": f"File non trovato: {str(e)}"}), 404
    except ValueError:
        return jsonify({"error": "L'ID utente deve essere un numero intero valido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/registrazione', methods=['POST'])
def registrazione():
    try:
        # Legge i dati dalla richiesta (assicurati che sia in formato JSON)
        nuovo_utente = request.json

        # Controlla che il JSON contenga i campi richiesti
        if not nuovo_utente or 'email' not in nuovo_utente or 'password' not in nuovo_utente:
            return jsonify({"error": "Dati non validi. Sono richiesti 'email' e 'password'."}), 400

        # Legge il file users.json
        if not os.path.exists(USERS_FILE):
            # Se il file non esiste, crealo con un array vuoto
            with open(USERS_FILE, 'w') as file:
                json.dump([], file)

        with open(USERS_FILE, 'r') as file:
            utenti = json.load(file)

        # Verifica se l'email esiste già
        if any(utente['email'] == nuovo_utente['email'] for utente in utenti):
            return jsonify({"error": "Email già registrata."}), 409

        # Aggiunge il nuovo utente
        utenti.append(nuovo_utente)

        # Scrive il file aggiornato
        with open(USERS_FILE, 'w') as file:
            json.dump(utenti, file, indent=4)

        return jsonify({"message": "Registrazione avvenuta con successo!", "data": nuovo_utente}), 201

    except FileNotFoundError:
        return jsonify({"error": "File users.json non trovato."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=True)
