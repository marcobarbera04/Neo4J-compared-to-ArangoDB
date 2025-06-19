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