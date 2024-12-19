
| **Endpoint**         | **Metodi** | **Descrizione**                                                                              | **Parametri**                                                                                           | **Return**                                                                                               |
|---------------------|-------------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| `/`                 | GET         | Restituisce il template HTML principale.                                                     | Nessun parametro.                                                                                      | Renderizza e restituisce il template HTML.                                                             |
| `/add-anime`       | POST        | Aggiunge un anime preferito per un utente.                                                  | `idUtente` (ID dell'utente), `idAnime` (ID dell'anime)                                                  | JSON con un messaggio di successo o errore.                                                             |
| `/episodi-visti/<id_utente>/<id_anime>` | GET   | Restituisce gli episodi visti di un anime per un utente specifico.                        | `id_utente`, `id_anime`                                                                                 | JSON con l'intero oggetto dell'anime trovato o un errore.                                                 |
| `/login`           | POST        | Verifica le credenziali dell'utente e restituisce i dati dell'utente.                      | `email`, `password`                                                                                      | JSON con i dati dell'utente o un errore.                                                                 |
| `/anime-stagionali` | GET        | Restituisce gli anime stagionali per un anno e una stagione specifici.                    | `anno`, `stagione` (es. 'Inverno', 'Primavera')                                                         | JSON con gli anime stagionali trovati.                                                                   |
| `/anime/trova/<nome_anime>` | GET   | Cerca un anime per titolo.                                                                  | `nome_anime` (parola chiave del titolo)                                                                  | JSON con gli anime corrispondenti al nome dato o un errore.                                               |
| `/anime/trova/<id_anime>`  | GET   | Cerca un anime per ID.                                                                      | `id_anime`                                                                                               | JSON con l'anime corrispondente al ID dato o un errore.                                                     |
| `/anime/preferiti/<id_utente>` | GET | Restituisce gli anime preferiti di un utente.                                               | `id_utente`                                                                                             | JSON con gli anime preferiti dell'utente o un errore.                                                      |
| `/registrazione`    | POST        | Crea un nuovo utente e lo aggiunge al sistema.                                               | `email`, `password`, `username`, `nome`, `cognome`, `data_nascita`                                      | JSON con un messaggio di successo e i dati del nuovo utente o un errore.                                 |
| `/classifica`       | GET         | Restituisce la classifica degli anime in base alla loro posizione.                       | Nessun parametro.                                                                                      | JSON con la classifica degli anime.                                                                      |

**Parametri**:
- I parametri di query o i dati inviati via POST sono ben specificati per ciascun endpoint.
- I dati POST sono in formato JSON.

**Return**:
- Ogni endpoint restituisce una risposta JSON con:
  - Un messaggio di successo o errore.
  - I dati richiesti (come gli anime preferiti, i dati dell'utente, gli anime stagionali, ecc.).
  - Status code HTTP appropriato (200 per successo, 400 per errore di input, 404 per non trovato, 409 per conflitto, ecc.).

