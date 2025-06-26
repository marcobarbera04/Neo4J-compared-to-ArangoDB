// Crea nuovi constraint solo su uuid
CREATE CONSTRAINT unique_nazione_uuid IF NOT EXISTS
FOR (n:Nazione) REQUIRE n.uuid IS UNIQUE;

CREATE CONSTRAINT unique_banca_uuid IF NOT EXISTS
FOR (b:Banca) REQUIRE b.uuid IS UNIQUE;

CREATE CONSTRAINT unique_persona_uuid IF NOT EXISTS
FOR (p:Persona) REQUIRE p.uuid IS UNIQUE;

CREATE CONSTRAINT unique_conto_uuid IF NOT EXISTS
FOR (c:Conto) REQUIRE c.uuid IS UNIQUE;

CREATE CONSTRAINT unique_carta_uuid IF NOT EXISTS
FOR (ci:CartaIdentita) REQUIRE ci.uuid IS UNIQUE;