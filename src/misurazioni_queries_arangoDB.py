import time
import sys
import csv
from arango import ArangoClient

# Configurazione ArangoDB
USER = 'root'
PASSWORD = 'secret'
DB_NAME = 'database100'
URI = "http://127.0.0.1:8529"

queries = [
"""
FOR p IN Persona
FILTER 
  p.eta > 20 AND p.eta < 25
  AND 
  (REGEX_TEST(p.nome, '^M.*o$') OR REGEX_TEST(p.cognome, '^R.*i$'))
  AND STARTS_WITH(p.codice_fiscale, 'M')
RETURN p
""",

"""
FOR c IN Conto
  FILTER (c.tipo_conto == "Investimento" OR c.tipo_conto == "Personale")
    AND (c.valuta == "USD" OR c.valuta == "EUR")
    AND c.limite_prelievo > 1000
    AND c.saldo > 45000
    AND c.data_apertura >= DATE_SUBTRACT(DATE_NOW(), 13, "month")
  RETURN c
""",

"""
// Prima calcoliamo i numeri sospetti (carte con più enti emittenti)
LET numeriSospetti = (
  FOR c IN CartaIdentita
    COLLECT numero = c.numero INTO carte
    FILTER COUNT_DISTINCT(carte[*].c.ente_emittente) > 1
    RETURN numero
)

// Poi troviamo le nazioni target (Fiji)
LET targetNazioni = (FOR n IN Nazione FILTER n.nome == "Fiji" RETURN n._id)

// Infine eseguiamo la query principale
FOR c IN CartaIdentita
  FILTER c.numero IN numeriSospetti
  FOR persona IN INBOUND c HA_CARTA
    FILTER LENGTH(
      FOR nid IN targetNazioni
        FOR edge IN APPARTIENE_A
          FILTER edge._from == persona._id AND edge._to == nid
          LIMIT 1
          RETURN 1
    ) > 0
    FOR conto IN OUTBOUND persona HA_CONTO
      RETURN conto
""",

"""
LET unMeseFaStr = DATE_FORMAT(DATE_SUBTRACT(DATE_NOW(), 1, "month"), "%yyyy-%mm-%dd")
LET oggiStr = DATE_FORMAT(DATE_NOW(), "%yyyy-%mm-%dd")

FOR persona IN Persona
  // Conta le transazioni recenti in uscita da tutti i conti della persona
  LET transazioniRecentiCount = LENGTH(
    FOR ha_conto IN HA_CONTO
      FILTER ha_conto._from == persona._id
      FOR transazione IN TRANSAZIONE
        FILTER transazione._from == ha_conto._to
          AND transazione.data >= unMeseFaStr
          AND transazione.data <= oggiStr
        RETURN 1
  )

  FILTER transazioniRecentiCount > 13

  // Recupera la carta d'identità (primo match)
  LET carta = FIRST(
    FOR ha_carta IN HA_CARTA
      FILTER ha_carta._from == persona._id
      FOR cartaIdentita IN CartaIdentita
        FILTER cartaIdentita._id == ha_carta._to
        RETURN cartaIdentita
  )

  // Recupera la nazione (primo match) - lasciato invariato ma ancora non usato
  LET nazione = FIRST(
    FOR appartiene IN APPARTIENE_A
      FILTER appartiene._from == persona._id
      FOR n IN Nazione
        FILTER n._id == appartiene._to
        RETURN n
  )

  RETURN {
    persona: {
      nome: persona.nome,
      cognome: persona.cognome,
      codice_fiscale: persona.codice_fiscale,
      uuid: persona.uuid
    },
    numero_carta_identita: carta.numero
  }
"""
]

def connessione(uri, username, password):
    client = ArangoClient(hosts=uri)
    db = client.db(DB_NAME, username=username, password=password)  # Cambia db se serve
    return db

def esegui_query(db, query, bind_vars=None):
    cursor = db.aql.execute(query, bind_vars=bind_vars, stream=True)
    cursor.close()
    return None

def esegui_query_n_volte(uri, username, password, numero_query, n):
    query = queries[numero_query]
    filename = "tempi_query_" + str(numero_query + 1) + "_arangoDB_" + DB_NAME + ".csv"
    risultati = [["TIPO", "NUMERO QUERY", "TEMPO (ms)"]]

    db = connessione(uri, username, password)

    # Prima esecuzione non registrata
    esegui_query(db, query)

    for i in range(n):
        start_time = time.perf_counter()
        esegui_query(db, query)
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000
        risultati.append(["iterativa", numero_query+1, f"{elapsed_time:.3f}"])

    #db.connection.close()
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
