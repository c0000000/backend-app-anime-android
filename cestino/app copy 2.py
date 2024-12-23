from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Percorsi dei file
ANIME_PREFERITI_FILE = 'anime-preferiti.json'
ANIME_DB_FILE = 'anime_db.json'
USERS_FILE = 'users.json'

# Esegui la correzione dei file JSON
@app.route('/')
def index():
    # Restituisce un template HTML
    return render_template('index.html')
@app.route('/add-anime', methods=['GET'])  # Endpoint per aggiungere anime preferiti
def add_anime():
    try:
        # Legge i dati dalla query string e li converte in interi
        id_utente = int(request.args.get('idUtente'))
        id_anime = int(request.args.get('idAnime'))

        # Controlla che i parametri siano presenti
        
        print(f"Aggiunta anime preferito utente {id_utente} - anime {id_anime}")

        # Carica i dati esistenti dal file
        with open(ANIME_PREFERITI_FILE, 'r', errors="ignore") as file:
            preferiti = json.load(file)

        # Trova o crea l'utente nel file preferiti
        utente_esistente = next((item for item in preferiti if item['idUtente'] == id_utente), None)

        if utente_esistente:
            # Aggiunge l'idAnime alla lista dell'utente, evitando duplicati
            if id_anime not in [anime['id'] for anime in utente_esistente['idAnimes']]:
                utente_esistente['idAnimes'].append({"id": id_anime, "episodiVisti": 0})
        else:
            # Crea un nuovo utente con il suo primo anime preferito
            preferiti.append({
                "idUtente": id_utente,
                "idAnimes": [{"id": id_anime, "episodiVisti": 0}]
            })

        # Scrive i dati aggiornati nel file
        with open(ANIME_PREFERITI_FILE, 'w') as file:
            json.dump(preferiti, file, indent=4)

        return jsonify({"message": "Anime aggiunto con successo!", "data": {"idUtente": id_utente, "idAnime": id_anime}}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/anime/preferiti', methods=['GET'])
def get_anime_preferitis():
    try:
        # Recupera l'idUtente dalla query string
        id_utente = request.args.get('idUtente')
        if not id_utente:
            return jsonify({"error": "idUtente è richiesto"}), 400

        # Converte l'idUtente in intero
        id_utente = int(id_utente)

        # Carica i dati dei preferiti dal file
        with open(ANIME_PREFERITI_FILE, 'r', errors="ignore") as file:
            preferiti_data = json.load(file)

        # Trova i preferiti dell'utente
        utente_preferiti = next(
            (item for item in preferiti_data if item['idUtente'] == id_utente), 
            None
        )

        if not utente_preferiti:
            return jsonify({"error": f"Nessun preferito trovato per idUtente {id_utente}"}), 404

        # Estrae gli idAnimes con episodi visti
        id_animes = utente_preferiti['idAnimes']

        # Carica i dati degli anime dal file
        with open(ANIME_DB_FILE, 'r', errors="ignore") as file:
            anime_data = json.load(file)

        # Filtra gli anime in base agli idAnimes e aggiunge gli episodi visti
        anime_list = []
        for anime_preferito in id_animes:
            anime_id = anime_preferito['id']
            episodi_visti = anime_preferito['episodiVisti']
            
            # Trova i dettagli dell'anime
            anime = next((item for item in anime_data if item['id'] == anime_id), None)
            if anime:
                # Aggiunge i dettagli degli episodi visti
                anime['episodiVisti'] = episodi_visti
                anime_list.append(anime)

        return jsonify(anime_list), 200

    except ValueError:
        return jsonify({"error": "idUtente deve essere un numero intero"}), 400
    except FileNotFoundError as e:
        return jsonify({"error": f"File non trovato: {str(e)}"}), 500
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Errore nel parsing del file JSON: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Errore sconosciuto: {str(e)}"}), 500
    


@app.route('/episodi-visti/<id_utente>/<id_anime>', methods=['GET'])
def get_episodi_visti(id_utente, id_anime):
    try:
        # Carica i dati esistenti dal file
        with open(ANIME_PREFERITI_FILE, 'r',errors='ignore') as file:
            preferiti = json.load(file)

        # Trova l'utente nel file preferiti
        utente = next((item for item in preferiti if item['idUtente'] == id_utente), None)

        if not utente:
            return jsonify({"error": "Utente non trovato."}), 404

        # Trova l'anime specifico per l'utente
        anime = next((anime for anime in utente['idAnimes'] if anime['id'] == id_anime), None)

        if not anime:
            return jsonify({"error": "Anime non trovato per questo utente."}), 404

        # Restituisce l'intero oggetto dell'anime, inclusi gli episodi visti
        return jsonify(anime), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/login', methods=['POST'])
def login():
    try:
        # Carica il file users.json
        with open(USERS_FILE, 'r',errors='ignore') as file:
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
                return jsonify(user), 200
        except FileNotFoundError:
            return jsonify({"error": "File associato non trovato"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/profilo', methods=['GET'])
def get_utente_form_id():
    try:
            # Carica il file users.json
        with open(USERS_FILE, 'r', errors='ignore') as file:
            users = json.load(file)

        print("users count:", len(users))
        # Estrai l'ID dall'query string
        user_id = request.args.get('idUtente')

        print("User ID extracted from query string:", user_id)
        print("Users[0] ID extracted from query string:", users[0]["id"])

        # Cerca un utente con l'ID fornito
        user = next((u for u in users if u['id'] == int(user_id)), None)


        if not user:
            return jsonify({"error": "Utente non trovato","idUtente":user_id}), 404

        # Legge e restituisce il file associato all'utente
        try:
            return jsonify(user), 200
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
        stagione = stagione.capitalize()
        # Ottieni il percorso assoluto del file
        file_path = os.path.abspath(ANIME_DB_FILE)
        print("Percorso del file:", file_path)  # Stampa il percorso per il debug

        with open(file_path, 'r',errors='ignore') as file:
            data = json.load(file)

        # Filtra gli anime in base ai parametri
        anime_stagionali = [anime for anime in data if anime['premiered'] == f"{stagione} {anno}"]

        return jsonify(anime_stagionali), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/anime-db', methods=['GET'])
def get_anime_db():
    try:
        # Ottieni il percorso assoluto del file
        file_path = os.path.abspath(ANIME_DB_FILE)
        print("Percorso del file:", file_path)  # Stampa il percorso per il debug

        with open(file_path, 'r',errors='ignore') as file:
            data = json.load(file)

        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/anime/trova/<nome_anime>', methods=['GET'])
def get_anime_from_title(nome_anime):
    try:
        # Legge il file JSON con la lista degli anime
        with open(ANIME_DB_FILE, 'r',errors='ignore') as file:
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

@app.route('/anime/trova', methods=['GET'])
def get_anime_from_id():
    try:
        id_anime = request.args.get('idAnime')  # Ottieni il valore della query string 'id_anime'
        print("id_anime:", id_anime)
        
        if not id_anime:
            return jsonify({"error": "ID dell'anime non fornito"}), 400
        
        # Legge il file JSON con la lista degli anime
        with open(ANIME_DB_FILE, 'r', errors='ignore') as file:
            anime_list = json.load(file)

        # Cerca l'anime corrispondente al nome dato
        risultato = next((anime for anime in anime_list if anime['id'] == int(id_anime)), None)
        if risultato:
            return jsonify(risultato), 200
        else:
            return jsonify({"error": "Anime non trovato"}), 404

    except FileNotFoundError:
        return jsonify({"error": "File non trovato"}), 404
    except ValueError:
        return jsonify({"error": "ID dell'anime non valido"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/anime/preferiti/<id_utente>', methods=['GET'])
def get_anime_preferiti(id_utente):
    try:
        # Converte id_utente in un numero intero
        id_utente = int(id_utente)

        # Legge il file anime-preferiti.json
        with open(ANIME_PREFERITI_FILE, 'r', errors='ignore') as file_preferiti:
            preferiti = json.load(file_preferiti)

        # Trova l'utente specificato
        utente = next((u for u in preferiti if u['idUtente'] == id_utente), None)

        if not utente:
            return jsonify({"error": f"Nessun preferito trovato per l'utente con id {id_utente}."}), 404

        # Ottieni gli ID degli anime associati all'utente
        id_anime_list = utente.get('idAnimes', [])

        # Legge il file anime-lista.json
        with open(ANIME_DB_FILE, 'r', errors='ignore') as file_lista:
            anime_lista = json.load(file_lista)

        # Trova gli anime corrispondenti agli ID
        risultati = [anime for anime in anime_lista if any(anime['id'] == obj['id'] for obj in id_anime_list)]

        return jsonify(risultati), 200

    except FileNotFoundError as e:
        return jsonify({"error": f"File non trovato: {str(e)}"}), 404
    except ValueError:
        return jsonify({"error": "L'ID utente deve essere un numero intero valido."}), 400
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Errore nella decodifica del file JSON: {str(e)}"}), 400
    except UnicodeDecodeError as e:
        return jsonify({"error": f"Errore di codifica: {str(e)}. Controlla la codifica del file."}), 400

    
@app.route('/registrazione', methods=['POST'])
def registrazione():
    try:
        # Legge i dati dalla richiesta (assicurati che sia in formato JSON)
        nuovo_utente = request.json

        # Definisci i campi richiesti
        campi_richiesti = ['email', 'password', 'username']

        # Controlla che il JSON contenga tutti i campi richiesti
        if not nuovo_utente or any(campo not in nuovo_utente for campo in campi_richiesti):
            return jsonify({"error": f"Dati non validi. Sono richiesti {', '.join(campi_richiesti)}."}), 400

        # Legge il file users.json
        if not os.path.exists(USERS_FILE):
            # Se il file non esiste, crealo con un array vuoto
            with open(USERS_FILE, 'w',errors='ignore') as file:
                json.dump([], file)

        with open(USERS_FILE, 'r',errors='ignore') as file:
            utenti = json.load(file)

        # Verifica se l'email esiste già
        if any(utente['email'] == nuovo_utente['email'] for utente in utenti):
            return jsonify({"error": "Email già registrata."}), 409

        #nuovo_utente['totale_tempo'] = [{"tempo_s": 0, "giorno": 1}]
        # Aggiunge il nuovo utente
        utenti.append(nuovo_utente)

        # Scrive il file aggiornato
        with open(USERS_FILE, 'w',errors='ignore') as file:
            json.dump(utenti, file, indent=4)
        
        return jsonify(nuovo_utente), 201

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

        with open(ANIME_DB_FILE, 'r', errors='ignore') as file:
            anime_list = json.load(file)

        # Crea un dizionario con la classifica posizione-id anime
        classifica_lista = [{'idAnime': int(anime['id']), 'rank': rank} for rank, anime in enumerate(sorted(anime_list, key=lambda x: int(x['ranked'].strip('#'))), start=1)]

        # Mi restustice un file json lista 

        return jsonify(classifica_lista), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=True)
