// Importare nazioni con APOC per batch processing
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///nazioni.csv' AS row RETURN row",
  "CREATE (:Nazione {nome: row.nome, tasso_inflazione: toFloat(row.tasso_inflazione), popolazione: toInteger(row.popolazione)})",
  {batchSize: 1000, parallel: true}
);

// Importare banche con APOC
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///banche.csv' AS row RETURN row",
  "CREATE (:Banca {nome: row.nome, anno_fondazione: toInteger(row.anno_fondazione), tipo: row.tipo, filiali: toInteger(row.filiali), rating: row.rating, settore: row.settore})",
  {batchSize: 1000, parallel: true}
);

// Importare persone con APOC
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///persone.csv' AS row RETURN row",
  "CREATE (:Persona {id: row.id, nome: row.nome, cognome: row.cognome, eta: toInteger(row.eta), codice_fiscale: row.codice_fiscale})",
  {batchSize: 1000, parallel: true}
);

// Importare carte d'identità e creare relazione con la persona
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///carte_identita.csv' AS row RETURN row",
  "MATCH (p:Persona {codice_fiscale: row.codice_fiscale})
   CREATE (p)-[:HA_CARTA]->(:CartaIdentita {numero: row.numero, ente_emittente: row.ente_emittente, 
   data_rilascio: row.data_rilascio, data_scadenza: row.data_scadenza})",
  {batchSize: 1000, parallel: true}
);

// Importare conti correnti con APOC
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///conti_corrente.csv' AS row RETURN row",
  "CREATE (:Conto {numero_conto: row.numero_conto, saldo: toFloat(row.saldo), tipo_conto: row.tipo_conto, 
   data_apertura: row.data_apertura, IBAN: row.IBAN, valuta: row.valuta, limite_prelievo: toFloat(row.limite_prelievo), codice_fiscale: row.codice_fiscale})",
  {batchSize: 1000, parallel: true}
);

// Collegare persone alle nazioni casualmente
CALL apoc.periodic.iterate(
  "MATCH (p:Persona) WITH p MATCH (n:Nazione) WITH p, n ORDER BY rand() RETURN p, collect(n)[0] AS nazioneCasuale",
  "CREATE (p)-[:APPARTIENE_A]->(nazioneCasuale)",
  {batchSize: 1000, parallel: true}
);

// Collegare banche alle nazioni casualmente
CALL apoc.periodic.iterate(
  "MATCH (b:Banca) MATCH (n:Nazione) WITH b, n ORDER BY rand() RETURN b, collect(n)[0] AS nazioneScelta",
  "CREATE (b)-[:SITUATA_IN]->(nazioneScelta)",
  {batchSize: 1000, parallel: true}
);

// Collegare persone ai conti correnti usando codice fiscale
CALL apoc.periodic.iterate(
  "LOAD CSV WITH HEADERS FROM 'file:///conti_corrente.csv' AS row RETURN row",
  "MATCH (p:Persona {codice_fiscale: row.codice_fiscale}) MATCH (c:Conto {IBAN: row.IBAN})
   CREATE (p)-[:HA_CONTO]->(c)",
  {batchSize: 1000, parallel: true}
);

// Collegare conti correnti alle banche casualmente
CALL apoc.periodic.iterate(
  "MATCH (c:Conto), (b:Banca) RETURN c, collect(b)[toInteger(rand() * SIZE(collect(b)))] AS banca",
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
