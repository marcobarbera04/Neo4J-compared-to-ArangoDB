// [1]
MATCH (p:Persona)
WHERE p.eta >= 25 AND p.eta <= 50
  AND (p.nome STARTS WITH 'A' OR p.nome STARTS WITH 'M')
RETURN p

// [2]
MATCH (c:Conto)
WHERE (c.tipo_conto = "Investimento" OR c.tipo_conto = "Personale")
  AND (c.valuta = "USD" OR c.valuta = "EUR")
  AND c.limite_prelievo > 1000
  AND c.saldo > 45000
  AND date(c.data_apertura) >= date() - duration('P13M')
RETURN c

// [3]
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

// [4]
WITH date() AS oggi, date() - duration({months: 1}) AS un_mese_fa
MATCH (p:Persona)-[:HA_CONTO]->(c:Conto)-[t:TRANSAZIONE]->()
WHERE t.data >= un_mese_fa AND t.data <= oggi
WITH p, count(t) AS totale_transazioni_ultimo_mese
WHERE totale_transazioni_ultimo_mese > 13

OPTIONAL MATCH (p)-[:APPARTIENE_A]->(n:Nazione)
OPTIONAL MATCH (p)-[:HA_CARTA]->(ci:CartaIdentita)

RETURN p, n.nome AS nazionalita, ci.numero AS numero_carta_identita, totale_transazioni_ultimo_mese