// Esporta persone
CALL apoc.export.json.query(
  "MATCH (n:Persona) RETURN n",
  "file:///export/persona.json",
  {useTypes: true, stream: false}
);

// Esporta banche
CALL apoc.export.json.query(
  "MATCH (n:Banca) RETURN n",
  "file:///export/banche.json",
  {useTypes: true, stream: false}
);

// Esporta carte d'identita
CALL apoc.export.json.query(
  "MATCH (n:CartaIdentita) RETURN n",
  "file:///export/carte_identita.json",
  {useTypes: true, stream: false}
);

// Esporta nazioni
CALL apoc.export.json.query(
  "MATCH (n:Nazione) RETURN n",
  "file:///export/nazione.json",
  {useTypes: true, stream: false}
);

// Esporta conti
CALL apoc.export.json.query(
  "MATCH (n:Conto) RETURN n",
  "file:///export/conti.json",
  {useTypes: true, stream: false}
);

// Esporta relazioni HA_CONTO
CALL apoc.export.json.query(
  "MATCH ()-[r:HA_CONTO]->() RETURN r",
  "file:///export/HA_CONTO.json",
  {useTypes: true, stream: false}
);

// Esporta relazioni TRANSAZIONE
CALL apoc.export.json.query(
  "MATCH ()-[r:TRANSAZIONE]->() RETURN r",
  "file:///export/TRANSAZIONE.json",
  {useTypes: true, stream: false}
);

// Esporta relazioni AFFILIATO
CALL apoc.export.json.query(
  "MATCH ()-[r:AFFILIATO]->() RETURN r",
  "file:///export/AFFILIATO.json",
  {useTypes: true, stream: false}
);

// Esporta relazioni APPARTIENE_A
CALL apoc.export.json.query(
  "MATCH ()-[r:APPARTIENE_A]->() RETURN r",
  "file:///export/APPARTIENE_A.json",
  {useTypes: true, stream: false}
);

// Esporta relazioni HA_CARTA
CALL apoc.export.json.query(
  "MATCH ()-[r:HA_CARTA]->() RETURN r",
  "file:///export/HA_CARTA.json",
  {useTypes: true, stream: false}
);

// Esporta relazioni SITUATA_IN
CALL apoc.export.json.query(
  "MATCH ()-[r:SITUATA_IN]->() RETURN r",
  "file:///export/SITUATA_IN.json",
  {useTypes: true, stream: false}
);
