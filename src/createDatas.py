import pandas as pd
from faker import Faker
import random

# Inizializza Faker
faker = Faker()
Faker.seed(42)  # Per risultati riproducibili

# Creazione delle liste per i dati**
persone = []
banche = []
conti_bancari = []
transazioni = []
relazioni_ha_conto = []
relazioni_offre_conto = []
relazioni_effettuata_da = []
relazioni_invia_a = []
relazioni_collega = []

# Generazione delle Banche**
for i in range(5):  # Numero di banche
    banche.append([f"B{i+1}", faker.company(), faker.country()])

# Generazione delle Persone e Conti Bancari**
for i in range(20):  # Numero di persone
    persona_id = f"P{i+1}"
    persone.append([persona_id, faker.first_name(), faker.last_name(), faker.country(), faker.city(), faker.email(), faker.phone_number()])
    
    # Assegna conti bancari alla persona con banche diverse
    num_conti = random.randint(1, 3)
    for _ in range(num_conti):
        conto_id = f"C{len(conti_bancari) + 1}"
        banca_id = random.choice(banche)[0]
        tipo_conto = random.choice(["Corrente", "Risparmio"])
        conti_bancari.append([conto_id, banca_id, persona_id, tipo_conto])
        relazioni_ha_conto.append([persona_id, conto_id])
        relazioni_offre_conto.append([banca_id, conto_id])

# Generazione delle Transazioni**
for i in range(50):  # Numero di transazioni
    transazione_id = f"T{i+1}"
    importo = round(random.uniform(100, 10000), 2)
    data_transazione = faker.date_this_year()
    origine = random.choice(persone)[0]
    destinazione = random.choice([p[0] for p in persone if p[0] != origine])
    
    transazioni.append([transazione_id, importo, data_transazione, origine, destinazione])
    relazioni_effettuata_da.append([transazione_id, origine])
    relazioni_invia_a.append([transazione_id, destinazione])

# Generazione delle relazioni tra transazioni**
for _ in range(10):
    t1 = random.choice(transazioni)[0]
    t2 = random.choice([t[0] for t in transazioni if t[0] != t1])
    relazioni_collega.append([t1, t2])

# Salvataggio in CSV**
datasets = {
    "persone.csv": persone,
    "banche.csv": banche,
    "conti_bancari.csv": conti_bancari,
    "transazioni.csv": transazioni,
    "relazioni_ha_conto.csv": relazioni_ha_conto,
    "relazioni_offre_conto.csv": relazioni_offre_conto,
    "relazioni_effettuata_da.csv": relazioni_effettuata_da,
    "relazioni_invia_a.csv": relazioni_invia_a,
    "relazioni_collega.csv": relazioni_collega
}

for filename, data in datasets.items():
    df = pd.DataFrame(data)
    df.to_csv(f"../import/{filename}", index=False, header=False)

print("Dati generati e salvati in formato CSV con successo!")