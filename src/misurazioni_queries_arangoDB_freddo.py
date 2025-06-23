import time
import sys
import csv
import os
from arango import ArangoClient

# Configurazione ArangoDB
USER = 'root'
PASSWORD = 'secret'
DB_NAME = ''
URI = "http://127.0.0.1:8529"

queries = [
    """
    """,
    """
    """,
    """
    """,
    """
    """
]

def connessione(uri, username, password):
    client = ArangoClient(hosts=uri)
    db = client.db(DB_NAME, username=username, password=password)
    return db

def esegui_query(db, query, bind_vars=None):
    cursor = db.aql.execute(query, bind_vars=bind_vars)
    return cursor  # Cursor da iterare

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[ERRORE] Formato comando deve rispettare: py nome_programma numero_query")
        sys.exit(1)

    numero_query = int(sys.argv[1]) - 1
    if numero_query < 0 or numero_query > 3:
        print("Il numero deve essere compreso tra 1 e 4")
        sys.exit(1)

    # Scelgo query in base all'argomento passato
    query = queries[numero_query]

    # File per i tempi
    filename = "tempi_esecuzione_" + str(numero_query + 1) + "_query_arangoDB_freddo.csv"

    # Lista per contenere i risultati 
    risultati = [["TIPO", "NUMERO QUERY", "TEMPO (ms)"]]

    # Query a freddo (istanza del db appena avviata)
    db = connessione(URI, USER, PASSWORD)

    print(f"Eseguo la query numero {numero_query+1}")
    start_time = time.perf_counter()
    list(esegui_query(db, query))
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000

    # Scrittura dei risultati in append
    file_exists = os.path.exists(filename)
    write_header = not file_exists or os.path.getsize(filename) == 0

    # Apro il csv in modalita' append
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["TIPO", "NUMERO QUERY", "TEMPO (ms)"])
        writer.writerow(["a freddo", numero_query + 1, "{:.3f}".format(elapsed_time)])

    print("Salvati tempi di esecuzione su file csv")
