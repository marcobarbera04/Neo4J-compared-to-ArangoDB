# Neo4J-compared-to-ArangoDB

## Installation

Clone the repository
```bash
git clone https://github.com/marcobarbera04/Neo4J-compared-to-ArangoDB.git
```

Start the docker environment
```bash
cd docker
docker-compose -p neo4j-arangodb -f docker-compose.yml up -d
```

## Access the databases

ArangoDB: http://localhost:8529

Neo4j: http://localhost:7474

## Import dataset to neo4j

Move csv files to 'import' folder

Import persone:
```bash
LOAD CSV FROM 'file:///persone.csv' AS line
CREATE (:Persona {
  id: line[0],
  nome: line[1],
  cognome: line[2],
  paese: line[3],
  citta: line[4],
  email: line[5],
  telefono: line[6]
});
```
Import banche:
```bash
LOAD CSV FROM 'file:///banche.csv' AS line
CREATE (:Banca {
  id: line[0],
  nome: line[1],
  paese: line[2]
});
```

Import conti_bancari:
```bash
LOAD CSV FROM 'file:///conti_bancari.csv' AS line
CREATE (:ContoBancario {
  id: line[0],
  banca_id: line[1],
  persona_id: line[2],
  tipo: line[3]
});
```
Import transazioni:
```bash
LOAD CSV FROM 'file:///transazioni.csv' AS line
CREATE (:Transazione {
  id: line[0],
  importo: toFloat(line[1]),
  data: date(line[2]),
  origine: line[3],
  destinazione: line[4]
});
```

Import Relazione tra Persona e Conto Bancario:
```bash
LOAD CSV FROM 'file:///relazioni_ha_conto.csv' AS line
WITH trim(line[0]) AS personaId, trim(line[1]) AS contoId
MATCH (p:Persona {id: personaId})
MATCH (c:ContoBancario {id: contoId})
CREATE (p)-[:HA_CONTO]->(c);
```

Import Relazione tra Banca e Conto Bancario:
```bash
LOAD CSV FROM 'file:///relazioni_offre_conto.csv' AS line
WITH trim(line[0]) AS bancaId, trim(line[1]) AS contoId
MATCH (b:Banca {id: bancaId})
MATCH (c:ContoBancario {id: contoId})
CREATE (b)-[:OFFRE_CONTO]->(c);
```

Import Relazione tra Transazione e Persona:
```bash
LOAD CSV FROM 'file:///relazioni_effettuata_da.csv' AS line
WITH trim(line[0]) AS transId, trim(line[1]) AS personaId
MATCH (t:Transazione {id: transId})
MATCH (p:Persona {id: personaId})
CREATE (t)-[:EFFETTUATA_DA]->(p);
```

Import Relazione tra Transazione e Persona:
```bash
LOAD CSV FROM 'file:///relazioni_invia_a.csv' AS line
WITH trim(line[0]) AS transId, trim(line[1]) AS personaId
MATCH (t:Transazione {id: transId})
MATCH (p:Persona {id: personaId})
CREATE (t)-[:INVIA_A]->(p);
```

Import Relazione tra Transazioni per identificare connessioni:
```bash
LOAD CSV FROM 'file:///relazioni_collega.csv' AS line
WITH trim(line[0]) AS t1Id, trim(line[1]) AS t2Id
MATCH (t1:Transazione {id: t1Id})
MATCH (t2:Transazione {id: t2Id})
CREATE (t1)-[:COLLEGA]->(t2);
```