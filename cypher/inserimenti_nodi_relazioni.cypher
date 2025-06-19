// Importare nazioni con APOC per batch processing (MERGE per evitare duplicati)
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///nazioni.csv' AS row RETURN row",
  "MERGE (n:Nazione {nome: row.nome})
   ON CREATE SET n.uuid = row.uuid, n.tasso_inflazione = toFloat(row.tasso_inflazione), n.popolazione = toInteger(row.popolazione)",
  {batchSize: 1000, parallel: true}
);

// Importare banche con APOC (MERGE per evitare duplicati)
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///banche.csv' AS row RETURN row",
  "MERGE (b:Banca {nome: row.nome})
   ON CREATE SET b.uuid = row.uuid, b.anno_fondazione = toInteger(row.anno_fondazione), b.tipo = row.tipo, b.filiali = toInteger(row.filiali), 
   b.rating = row.rating, b.settore = row.settore",
  {batchSize: 1000, parallel: true}
);


// Importare persone con APOC (MERGE per garantire che vengano create solo nuove persone)
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///persone.csv' AS row RETURN row",
  "MERGE (p:Persona {codice_fiscale: row.codice_fiscale})
   ON CREATE SET p.uuid = row.uuid, p.nome = row.nome, p.cognome = row.cognome, p.eta = toInteger(row.eta)",
  {batchSize: 1000, parallel: true}
);

// Importare carte d'identità e creare relazione con la persona (crea relazione solo per persone senza carta)
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///carte_identita.csv' AS row RETURN row",
  "MATCH (p:Persona {codice_fiscale: row.codice_fiscale})
   WHERE NOT (p)-[:HA_CARTA]->()
   CREATE (p)-[:HA_CARTA]->(:CartaIdentita {uuid: row.uuid, numero: row.numero, ente_emittente: row.ente_emittente, 
   data_rilascio: row.data_rilascio, data_scadenza: row.data_scadenza})",
  {batchSize: 1000, parallel: true}
);


// Importare conti correnti con APOC (MERGE per verificare l'unicità dei conti)
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///conti_corrente.csv' AS row RETURN row",
  "MERGE (c:Conto {IBAN: row.IBAN})
   ON CREATE SET c.uuid = row.uuid, c.numero_conto = row.numero_conto, c.saldo = toFloat(row.saldo), c.tipo_conto = row.tipo_conto, 
   c.data_apertura = row.data_apertura, c.valuta = row.valuta, c.limite_prelievo = toFloat(row.limite_prelievo), 
   c.codice_fiscale = row.codice_fiscale",
  {batchSize: 1000, parallel: true}
);


// Collegare persone alle nazioni casualmente (solo per le persone che non hanno ancora una nazione)
MATCH (p:Persona)
WHERE NOT (p)-[:APPARTIENE_A]->(:Nazione)
WITH p
CALL {
  WITH p
  MATCH (n:Nazione)
  WITH n ORDER BY rand() LIMIT 1
  RETURN n AS nazioneCasuale
}
MERGE (p)-[:APPARTIENE_A]->(nazioneCasuale)
RETURN count(*) AS personeAggiornate;

// Collegare banche alle nazioni casualmente (solo per le banche senza nazione)
MATCH (b:Banca)
WHERE NOT (b)-[:SITUATA_IN]->(:Nazione)
WITH b
CALL {
  WITH b
  MATCH (n:Nazione)
  WITH n ORDER BY rand() LIMIT 1
  RETURN n AS nazioneCasuale
}
MERGE (b)-[:SITUATA_IN]->(nazioneCasuale)
RETURN count(*) AS bancheAggiornate;


// Collegare persone ai conti correnti usando codice fiscale (MERGE per evitare duplicazioni)
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///conti_corrente.csv' AS row RETURN row",
  "MATCH (p:Persona {codice_fiscale: row.codice_fiscale}) MATCH (c:Conto {IBAN: row.IBAN})
   MERGE (p)-[:HA_CONTO]->(c)",
  {batchSize: 1000, parallel: true}
);

// Collegare conti correnti alle banche casualmente (solo i conti senza banca)
CALL apoc.periodic.iterate(
  "MATCH (c:Conto) WHERE NOT (c)-[:AFFILIATO]->() MATCH (b:Banca) RETURN c, collect(b)[toInteger(rand() * SIZE(collect(b)))] AS banca",
  "CREATE (c)-[:AFFILIATO]->(banca)",
  {batchSize: 1000, parallel: true}
);

// Creare transazioni tra conti correnti
// Versione ottimizzata per database più grandi
CALL apoc.periodic.iterate(
  "
  MATCH (c1:Conto)
  WHERE NOT (c1)-[:TRANSAZIONE]->()
  RETURN c1
  ",
  "
  MATCH (c2:Conto)
  WHERE c1 <> c2
  WITH c1, COLLECT(c2) AS destinatari_possibili
  UNWIND range(1, toInteger(rand() * 16) + 5) AS i
  WITH c1, destinatari_possibili[toInteger(rand() * size(destinatari_possibili))] AS destinatario
  CREATE (c1)-[:TRANSAZIONE {
    importo: round(rand() * 5000, 2),
    data: date(datetime() - duration({days: toInteger(rand() * 365)}))
  }]->(destinatario)
  ",
  {batchSize: 100, parallel: false}
)