from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Percorsi dei file
ANIME_PREFERITI_FILE = 'anime-preferiti.json'
ANIME_DB_FILE = 'anime_db.json'
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
        with open(ANIME_PREFERITI_FILE, 'r') as file:
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
                "idAnimes": [{"id":id_anime,"episodiVisti": 0}]
            })

        # Scrive i dati aggiornati nel file
        with open(ANIME_PREFERITI_FILE, 'w') as file:
            json.dump(preferiti, file, indent=4)

        return jsonify({"message": "Anime aggiunto con successo!", "data": data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/episodi-visti/<id_utente>/<id_anime>', methods=['GET'])
def get_episodi_visti(id_utente, id_anime):
    #episodi-visti - get dato un idUtente

    print("Getting")


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
        # Ottieni i parametri dalla queryString
        anno = request.args.get('anno')
        stagione = request.args.get('stagione')

        # Ottieni il percorso assoluto del file
        file_path = os.path.abspath(ANIME_DB_FILE)
        print("Percorso del file:", file_path)  # Stampa il percorso per il debug

        with open(file_path, 'r') as file:
            data = json.load(file)

        # Filtra gli anime in base ai parametri
        anime_stagionali = [anime for anime in data if anime['premiered'] == f"{stagione} {anno}"]

        return jsonify(anime_stagionali), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/anime/trova/<nome_anime>', methods=['GET'])
def get_anime_from_title(nome_anime):
    try:
        # Legge il file JSON con la lista degli anime
        with open(ANIME_DB_FILE, 'r') as file:
            anime_list = json.load(file)

        # Filtra gli anime che contengono il nome dato nel titolo
        risultati = [anime for anime in anime_list if nome_anime.lower() in anime['title'].lower()]

        if risultati:
            return jsonify(risultati), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({"error": "Anime non trovato"}), 404

    except FileNotFoundError:
        return jsonify({"error": "File non trovato"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/anime/trova/<id_anime>', methods=['GET'])
def get_anime_from_id(id_anime):
    try:
        # Legge il file JSON con la lista degli anime
        with open(ANIME_DB_FILE, 'r') as file:
            anime_list = json.load(file)

        # Cerca l'anime corrispondente al nome dato
        risultato = next((anime for anime in anime_list if anime['id'] == id_anime), None)

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
        with open(ANIME_PREFERITI_FILE, 'r') as file_preferiti:
            preferiti = json.load(file_preferiti)

        # Trova l'utente specificato
        utente = next((u for u in preferiti if u['idUtente'] == id_utente), None)

        if not utente:
            return jsonify({"error": f"Nessun preferito trovato per l'utente con id {id_utente}."}), 404

        # Ottieni gli ID degli anime associati all'utente
        id_anime_list = utente.get('idAnimes', [])

        # Legge il file anime-lista.json
        with open(ANIME_DB_FILE, 'r') as file_lista:
            anime_lista = json.load(file_lista)

        # Trova gli anime corrispondenti agli ID
        risultati = [anime for anime in anime_lista if any(anime['id'] == obj['id'] for obj in id_anime_list)]

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

        # Definisci i campi richiesti
        campi_richiesti = ['email', 'password', 'username', 'nome', 'cognome', 'data_nascita']

        # Controlla che il JSON contenga tutti i campi richiesti
        if not nuovo_utente or any(campo not in nuovo_utente for campo in campi_richiesti):
            return jsonify({"error": f"Dati non validi. Sono richiesti {', '.join(campi_richiesti)}."}), 400

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

        #nuovo_utente['totale_tempo'] = [{"tempo_s": 0, "giorno": 1}]
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
@app.route('/classifica', methods=['GET'])
def get_classifica():
    try:
        # Legge il file ANIME_DB_FILE
        if not os.path.exists(ANIME_DB_FILE):
            return jsonify({"error": "File ANIME_DB_FILE non trovato."}), 404

        with open(ANIME_DB_FILE, 'r', encoding='utf-8') as file:
            anime_list = json.load(file)

        # Crea un dizionario con la classifica posizione-id anime
        classifica = {int(i+1): anime['id'] for i, anime in enumerate(sorted(anime_list, key=lambda x: int(x['ranked'].strip('#'))))}

        return jsonify(classifica), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=True)
