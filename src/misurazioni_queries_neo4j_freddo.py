import time
import sys
import csv
import os
from neo4j import GraphDatabase

# Configurazione del database
URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "database"

queries = [
    """
    MATCH (p:Persona)
    WHERE p.eta >= 25 AND p.eta <= 50
    AND (p.nome STARTS WITH "A" OR p.nome STARTS WITH "M")
    RETURN p;   
    """, 
    """
    MATCH (p:Persona)-[:HA_CONTO]->(c:Conto)-[:AFFILIATO]->(b:Banca)
    WITH p, COLLECT(DISTINCT b) AS banche
    WHERE SIZE(banche) > 5
    RETURN p;
    """,
    """
    MATCH (c:CartaIdentita)
    WITH c.numero AS numero, COLLECT(c) AS carte
    WHERE SIZE(carte) = 2  // Considera solo carte con esattamente due duplicati
    AND carte[0].ente_emittente <> carte[1].ente_emittente  // Controllo sulla data di emissione
    UNWIND carte AS carta
    MATCH (p:Persona)-[:HA_CARTA]->(carta)
    MATCH (p)-[:APPARTIENE_A]->(n:Nazione)
    WHERE n.nome = "Fiji"
    MATCH (p)-[:HA_CONTO]->(conto:Conto)
    RETURN conto;   
    """,
    """
    WITH date() AS oggi, date() - duration({months: 1}) AS un_mese_fa
    MATCH (p:Persona)-[:HA_CONTO]->(c:Conto)-[t:TRANSAZIONE]->()
    WHERE t.data >= un_mese_fa AND t.data <= oggi
    WITH p, count(t) AS totale_transazioni_ultimo_mese
    WHERE totale_transazioni_ultimo_mese > 13

    OPTIONAL MATCH (p)-[:APPARTIENE_A]->(n:Nazione)
    OPTIONAL MATCH (p)-[:HA_CARTA]->(ci:CartaIdentita)

    RETURN p, n.nome AS nazionalita, ci.numero AS numero_carta_identita, totale_transazioni_ultimo_mese
    ORDER BY totale_transazioni_ultimo_mese DESC    
    """
    ]

def connessione(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))

def esegui_query(connessione, query, parameters=None):
    with connessione.session() as session:
        return session.run(query, parameters)  # Ritorna il cursore senza elaborare i risultati

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[ERRORE] Formato comando deve rispettare: py nome_programma numero_query")
        sys.exit(1)

    numero_query = int(sys.argv[1]) - 1 # Converti argomento in numero
    if numero_query < 0 or numero_query > 3 :
        print("Il numero deve essere compreso tra 1 e 4")
        sys.exit(1)
    
    # Scelgo query in base all'argomento passato
    query = queries[numero_query]

    # File per i tempi
    filename = "tempi_query_" + str(numero_query + 1) + "_neo4j_freddo.csv"
    
    # Lista per contenere i risultati 
    risultati = [["TIPO", "NUMERO QUERY", "TEMPO (ms)"]]

    # Query a freddo (istanza del db appena avviata)
    conn = connessione(URI, USER, PASSWORD)

    print("Eseguo la query numero" + str(numero_query + 1))
    start_time = time.perf_counter()
    esegui_query(conn, query, parameters=None)
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000   # Convertire da secondi a millisecondi

    # Scrittura dei risultati in append
    file_exists = os.path.exists(filename)
    write_header = not file_exists or os.path.getsize(filename) == 0

    # Apro il csv in modalita' append
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["TIPO", "NUMERO QUERY", "TEMPO (ms)"])
        writer.writerow(["a freddo", numero_query + 1, "{:.3f}".format(elapsed_time)])
    
    conn.close()