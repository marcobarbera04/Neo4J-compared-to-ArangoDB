import time
import sys
import csv
from arango import ArangoClient

# Configurazione ArangoDB
USER = 'root'
PASSWORD = 'secret'
DB_NAME = 'database25'
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
    db = client.db(DB_NAME, username=username, password=password)  # Cambia db se serve
    return db

def esegui_query(db, query, bind_vars=None):
    cursor = db.aql.execute(query, bind_vars=bind_vars)
    return cursor  # Cursor da iterare

def esegui_query_n_volte(uri, username, password, numero_query, n):
    query = queries[numero_query]
    filename = "tempi_esecuzione_" + str(numero_query + 1) + "_query_arangoDB.csv"
    risultati = [["TIPO", "NUMERO QUERY", "TEMPO (ms)"]]

    db = connessione(uri, username, password)

    # Prima esecuzione a freddo
    start_time = time.perf_counter()
    list(esegui_query(db, query))
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000
    risultati.append(["a freddo", numero_query+1, f"{elapsed_time:.3f}"])

    for i in range(n):
        start_time = time.perf_counter()
        list(esegui_query(db, query))
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000
        risultati.append(["iterativa", numero_query+1, f"{elapsed_time:.3f}"])

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(risultati)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[ERRORE] Formato comando deve rispettare: py nome_programma numero_query")
        sys.exit(1)

    numero_query = int(sys.argv[1]) - 1
    if numero_query < 0 or numero_query > 3:
        print("Il numero deve essere compreso tra 1 e 4")
        sys.exit(1)


    print(f"Eseguo la query numero {numero_query+1}")
    esegui_query_n_volte(URI, USER, PASSWORD, numero_query, 30)
    print("Salvati tempi di esecuzione su file csv")
