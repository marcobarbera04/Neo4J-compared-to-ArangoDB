// Creazione dei constraint
CREATE CONSTRAINT unique_nazione_name IF NOT EXISTS
FOR (n:Nazione) REQUIRE n.name IS UNIQUE;

CREATE CONSTRAINT unique_banca_name IF NOT EXISTS
FOR (b:Banca) REQUIRE b.name IS UNIQUE;

CREATE CONSTRAINT unique_persona_name IF NOT EXISTS
FOR (p:Persona) REQUIRE p.name IS UNIQUE;

CREATE CONSTRAINT unique_conto_name IF NOT EXISTS
FOR (c:Conto) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT unique_carta_name IF NOT EXISTS
FOR (ci:CartaIdentita) REQUIRE ci.name IS UNIQUE;

// Creazione degli indici per migliorare le prestazioni delle query
CREATE INDEX nazione_name_index IF NOT EXISTS
FOR (n:Nazione) ON (n.name);

CREATE INDEX banca_name_index IF NOT EXISTS
FOR (b:Banca) ON (b.name);

CREATE INDEX persona_name_index IF NOT EXISTS
FOR (p:Persona) ON (p.name);

CREATE INDEX conto_name_index IF NOT EXISTS
FOR (c:Conto) ON (c.name);

CREATE INDEX carta_name_index IF NOT EXISTS
FOR (ci:CartaIdentita) ON (ci.name);

// Creazione di indici sulle proprietà delle relazioni
CREATE INDEX relazione_appartiene_a_index IF NOT EXISTS
FOR ()-[r:APPARTIENE_A]-() ON (r.name);

CREATE INDEX relazione_situata_in_index IF NOT EXISTS
FOR ()-[r:SITUATA_IN]-() ON (r.name);

CREATE INDEX relazione_ha_conto_index IF NOT EXISTS
FOR ()-[r:HA_CONTO]-() ON (r.name);

CREATE INDEX relazione_transazione_index IF NOT EXISTS
FOR ()-[r:TRANSAZIONE]-() ON (r.name);

CREATE INDEX relazione_affiliato_index IF NOT EXISTS
FOR ()-[r:AFFILIATO]-() ON (r.name);

CREATE INDEX relazione_ha_carta_index IF NOT EXISTS
FOR ()-[r:HA_CARTA]-() ON (r.name);