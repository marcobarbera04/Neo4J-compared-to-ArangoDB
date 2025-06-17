import time
import sys
import csv
from neo4j import GraphDatabase

queries = ["MATCH (p:Persona) WHERE p.eta >= 25 AND p.eta <= 50 AND (p.nome STARTS WITH 'A' OR p.nome STARTS WITH 'M') RETURN p;", 
           "MATCH (p:Persona)-[:HA_CONTO]->(c:Conto)-[:AFFILIATO]->(b:Banca) WITH p, COLLECT(DISTINCT b) AS banche WHERE SIZE(banche) > 1 RETURN p;", 
           "MATCH (c:CartaIdentita) WITH c.numero AS numero, COLLECT(c) AS carte WHERE SIZE(carte) = 2 UNWIND carte AS carta MATCH (p:Persona)-[:HA_CARTA]->(carta) MATCH (p)-[:APPARTIENE_A]->(n:Nazione) WHERE n.nome = 'Maldive' MATCH (p)-[:HA_CONTO]->(conto:Conto) RETURN conto;", 
           "MATCH (p:Persona)-[:HA_CONTO]->(c:Conto)-[t:TRANSAZIONE]->(dest:Conto) WHERE t.data >= date() - duration('P1M') WITH p, COUNT(t) AS num_transazioni WHERE num_transazioni > 15 MATCH (p)-[:HA_CARTA]->(carta:CartaIdentita) MATCH (p)-[:APPARTIENE_A]->(n:Nazione) RETURN p, carta, n, num_transazioni;"]

def connessione(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))

def esegui_query(connessione, query, parameters=None):
    with connessione.session() as session:
        return session.run(query, parameters)  # Ritorna il cursore senza elaborare i risultati

def esegui_query_n_volte(uri, user, password, numero_query, n):
    #Scelgo la query in base all'argomento passato
    query = queries[numero_query]

    # File per i tempi
    filename = "tempi_esecuzione_" + str(numero_query + 1) + "_query.csv"
    
    # Lista per contenere i risultati 
    risultati = [["TIPO", "NUMERO QUERY", "TEMPO (ms)"]]

    # Query a freddo (istanza del db appena avviata)
    conn = connessione(uri, user, password)

    start_time = time.time()
    esegui_query(conn, query, parameters=None)
    elapsed_time = (time.time() - start_time) * 1000 # Convertire da secondi a millisecondi

    # Appendo il risultato a freddo nella lista
    risultati.append(["a freddo", numero_query + 1, "{:.3f}".format(elapsed_time)])

    for i in range(0,n):
        start_time = time.time()
        esegui_query(conn, query, parameters=None)
        elapsed_time = (time.time() - start_time) * 1000 # Convertire da secondi a millisecondi
        risultati.append(["iterativa", numero_query+1, "{:.3f}".format(elapsed_time)])
    conn.close()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(risultati)

# Esempio di utilizzo
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[ERRORE] Formato comando deve rispettare: py nome_programma numero_query")
        sys.exit(1)

    numero_query = int(sys.argv[1]) - 1 # Converti argomento in numero
    if numero_query < 0 or numero_query > 3 :
        print("Il numero deve essere compreso tra 1 e 4")
        sys.exit(1)
    
    # Configurazione del database
    URI = "neo4j://127.0.0.1:7687"
    USER = "neo4j"
    PASSWORD = "database"

    # Query di esempio
    print("Eseguo la query numero" + str(numero_query + 1))
    esegui_query_n_volte(URI, USER, PASSWORD, numero_query, 30)
    print("Salvati tempi di esecuzione su file csv")
