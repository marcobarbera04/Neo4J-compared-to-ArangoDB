import json
from arango import ArangoClient
 
# Connessione al database
client = ArangoClient()
db = client.db('database50', username='root', password='secret')  # Modifica se necessario

ENTITY = "Conto"
PRIMARY_KEY = "uuid"
IMPORT_FILE = "TRANSAZIONI.json"
EDGE_COLLECTION = "TRANSAZIONE"

# Nome del graph e edge collection
graph = db.graph('Sistema_bancario_50')
EDGE_COLLECTION = graph.EDGE_COLLECTION(EDGE_COLLECTION)
 
# Caricamento del file
with open('import/TRANSAZIONI.json', 'r') as f:
    for line in f:
        data = json.loads(line)
        relazione = data['r']
        start_id = relazione['start']['properties'][PRIMARY_KEY]
        end_id = relazione['end']['properties'][PRIMARY_KEY]
        # Costruisci _id per i nodi
        from_id = ENTITY + "/" + start_id
        to_id = ENTITY + "/" + end_id
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