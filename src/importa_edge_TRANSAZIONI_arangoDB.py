import json
from arango import ArangoClient

# Configurazione ArangoDB
USERNAME = 'root'
PASSWORD = 'secret'
DB_NAME = 'database25'

ENTITY_FROM = "Persona"
ENTITY_TO = "Nazione"
PRIMARY_KEY = "uuid"
IMPORT_FILE = "APPARTIENE_A.json"
EDGE_COLLECTION = "APPARTIENE_A"

# Connessione al database
client = ArangoClient()
db = client.db(DB_NAME, username=USERNAME, password=PASSWORD)  # Modifica se necessario

# Nome del graph e edge collection
graph = db.graph('bank_graph')
EDGE_COLLECTION = graph.edge_collection(EDGE_COLLECTION)
 
# Caricamento del file
with open('json/' + IMPORT_FILE, 'r') as f:
    for line in f:
        data = json.loads(line)
        relazione = data['r']
        start_id = relazione['start']['properties'][PRIMARY_KEY]
        end_id = relazione['end']['properties'][PRIMARY_KEY]
        # Costruisci _id per i nodi
        from_id = ENTITY_FROM + "/" + start_id
        to_id = ENTITY_TO + "/" + end_id
        # Proprietà dell’arco
        properties = relazione['properties']
        # Inserisci l’arco nel grafo
        try:
            EDGE_COLLECTION.insert({
                "_from": from_id,
                "_to": to_id,
                **properties
            })  # overwrite evita duplicati se già presenti
            #print(f"Inserito arco da {from_id} a {to_id}")
        except Exception as e:
            print(f"Errore inserendo arco da {from_id} a {to_id}: {e}")