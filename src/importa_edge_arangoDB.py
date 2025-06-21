import json
from arango import ArangoClient

# Configurazione ArangoDB
ARANGO_URL = 'http://localhost:8529'
USERNAME = ''
PASSWORD = ''
DB_NAME = ''

ENTITY_FROM = ""
ENTITY_TO = ""
PRIMARY_KEY = "uuid"
IMPORT_FILE = ".json"
EDGE_COLLECTION = ""

# Connessione al database
client = ArangoClient(hosts=ARANGO_URL)
db = client.db(DB_NAME, username=USERNAME, password=PASSWORD)

# Nome del graph e edge collection
graph = db.graph('bank_graph')
EDGE_COLLECTION = graph.edge_collection(EDGE_COLLECTION)

# Caricamento del file
with open('json' + IMPORT_FILE, 'r') as f:
    for line in f:
        data = json.loads(line)
        relazione = data['r']
        
        # Estrazione degli ID
        start_id = relazione['start']['properties'][PRIMARY_KEY]
        end_id = relazione['end']['properties'][PRIMARY_KEY]
        
        # Costruzione degli _id per gli edge
        from_id = ENTITY_FROM + "/" + start_id
        to_id = ENTITY_TO + "/" + end_id

        # Verifica e caricamento delle proprietà
        if 'properties' in relazione:
            properties = relazione['properties']
        else:
            properties = {}
            #print(f"[INFO] Relazione '{relazione.get('label', 'UNKNOWN')}' tra {from_id} e {to_id} senza proprietà.")

        # Inserimento arco
        try:
            EDGE_COLLECTION.insert({
                "_from": from_id,
                "_to": to_id,
                **properties
            })
            # print(f"Inserito arco da {from_id} a {to_id}")
        except Exception as e:
            print(f"[ERRORE] Inserimento fallito tra {from_id} e {to_id}: {e}")