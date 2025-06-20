// Cercare tutte le persone tra i 25 e 50 anni con il nome che inizia per A o M per lo scopo di conoscere il cliente (know your customer).
MATCH (p:Persona)
WHERE p.eta >= 25 AND p.eta <= 50
AND (p.nome STARTS WITH "A" OR p.nome STARTS WITH "M")
RETURN p;

// Cercare le persone che hanno più di 5 conti bancari associati, a banche diverse.
MATCH (p:Persona)-[:HA_CONTO]->(c:Conto)-[:AFFILIATO]->(b:Banca)
WITH p, COLLECT(DISTINCT b) AS banche
WHERE SIZE(banche) > 5
RETURN p;

// Per vedere effettivamente vedere le relazioni tra persone -> conti -> banche
MATCH (p:Persona)-[r:HA_CONTO]->(c:Conto)-[r2:AFFILIATO]->(b:Banca)
RETURN p, r, c, r2, b LIMIT 500;

// Cercare tutti i conti correnti di persone che hanno carta d’identità con numero uguale ma ente emittente diverso, di nazionalità Fiji (possibile paradiso fiscale)
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

// Cercare le persone che sono state coinvolte in almeno 15 transazioni nell'arco di 1 mese per tutti i conti bancari associati a quella persona e mostrare la carta d’identità e la nazione.
WITH date() AS oggi, date() - duration({months: 1}) AS un_mese_fa
MATCH (p:Persona)-[:HA_CONTO]->(c:Conto)-[t:TRANSAZIONE]->()
WHERE t.data >= un_mese_fa AND t.data <= oggi
WITH p, count(t) AS totale_transazioni_ultimo_mese
WHERE totale_transazioni_ultimo_mese > 13

OPTIONAL MATCH (p)-[:APPARTIENE_A]->(n:Nazione)
OPTIONAL MATCH (p)-[:HA_CARTA]->(ci:CartaIdentita)

RETURN p, n.nome AS nazionalita, ci.numero AS numero_carta_identita, totale_transazioni_ultimo_mese
ORDER BY totale_transazioni_ultimo_mese DESC