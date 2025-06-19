import json
from arango import ArangoClient

# Configurazione ArangoDB
ARANGO_URL = 'http://localhost:8529'
USERNAME = 'root'
PASSWORD = 'secret'
DB_NAME = 'database25'
COLLECTION_NAME = 'Conto'
PRIMARY_KEY = 'uuid'
IMPORT_FILE = 'conti.json'

# Connessione ad Arango
client = ArangoClient()
db = client.db(DB_NAME, username=USERNAME, password=PASSWORD)

# Crea collezione se serve
if not db.has_collection(COLLECTION_NAME):
    db.create_collection(COLLECTION_NAME)

collection = db.collection(COLLECTION_NAME)

# Funzione per caricare banche da file con oggetti separati senza virgola
def importa_banche_sequenziali(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # Ignora righe vuote
                try:
                    banca = json.loads(line)
                    properties = banca.get('n', {}).get('properties', {})
                    numero_conto = properties.get(PRIMARY_KEY)
                    if not numero_conto:
                        print("Numero conto mancante, riga saltata.")
                        continue
                    properties['_key'] = str(numero_conto)
                    collection.insert(properties, overwrite=True)
                    #print(f"Inserito Conto/{numero_conto}")
                except json.JSONDecodeError as e:
                    print(f"Errore di parsing: {e}")
                except Exception as e:
                    print(f"Errore inserendo conto: {e}")

# Esecuzione
importa_banche_sequenziali('json/' + IMPORT_FILE)
print("Importazione completata.")
