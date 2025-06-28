import time
import sys
import csv
from neo4j import GraphDatabase

# Configurazione del database
URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "database"

queries = [
"""
MATCH (p:Persona)
WHERE 
  p.eta > 20 AND p.eta < 25
  AND 
  (p.nome =~ '^M.*o$' OR p.cognome =~ '^R.*i$')
  AND p.codice_fiscale STARTS WITH 'M'
RETURN p
""",

"""
MATCH (c:Conto)
WHERE (c.tipo_conto = "Investimento" OR c.tipo_conto = "Personale")
  AND (c.valuta = "USD" OR c.valuta = "EUR")
  AND c.limite_prelievo > 1000
  AND c.saldo > 45000
  AND date(c.data_apertura) >= date() - duration('P13M')
RETURN c
""",

"""
// Prima calcoliamo i numeri sospetti (carte con più enti emittenti)
WITH [numero IN COLLECT {
    MATCH (c:CartaIdentita)
    WITH c.numero AS numero, COLLECT(DISTINCT c.ente_emittente) AS enti
    WHERE SIZE(enti) > 1
    RETURN numero
}] AS numeriSospetti

// Poi troviamo le nazioni target (Fiji)
WITH numeriSospetti, COLLECT {
    MATCH (n:Nazione)
    WHERE n.nome = "Fiji"
    RETURN n
} AS targetNazioni

// Infine eseguiamo la query principale
MATCH (c:CartaIdentita)
WHERE c.numero IN numeriSospetti
MATCH (persona:Persona)-[:HA_CARTA]->(c)
WHERE EXISTS {
    MATCH (persona)-[:APPARTIENE_A]->(n:Nazione)
    WHERE n.nome = "Fiji"
}
MATCH (persona)-[:HA_CONTO]->(conto:Conto)
RETURN conto 
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

def esegui_query_n_volte(uri, user, password, numero_query, n):
    #Scelgo la query in base all'argomento passato
    query = queries[numero_query]

    # File per i tempi
    filename = "tempi_query_" + str(numero_query + 1) + "_neo4j.csv"
    
    # Lista per contenere i risultati 
    risultati = [["TIPO", "NUMERO QUERY", "TEMPO (ms)"]]

    # Query a freddo (istanza del db appena avviata)
    conn = connessione(uri, user, password)

    # Prima esecuzione non registrata
    esegui_query(conn, query, parameters=None)

    for i in range(0,n):
        start_time = time.perf_counter()    
        esegui_query(conn, query, parameters=None)
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000 # Convertire da secondi a millisecondi
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

    # Query di esempio
    print("Eseguo la query numero" + str(numero_query + 1))
    esegui_query_n_volte(URI, USER, PASSWORD, numero_query, 30)
    print("Salvati tempi di esecuzione su file csv")
