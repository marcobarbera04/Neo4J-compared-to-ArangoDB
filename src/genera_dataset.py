import csv
import random
import datetime
from faker import Faker
from pathlib import Path

fake = Faker('it_IT')

# Directory output
output_dir = Path("import")
output_dir.mkdir(exist_ok=True)

NUM_PERSONE = 27125
NUM_CARTE = NUM_PERSONE  # Ora il numero di carte è uguale al numero di persone
NUM_CONTI = 45000
NUM_NAZIONI = 45
NUM_BANCHE = 180

def genera_nazioni():
    nazioni = []
    nazioni_generate = set()
    
    while len(nazioni) < NUM_NAZIONI:
        nome_nazione = fake.country()
        if nome_nazione not in nazioni_generate:
            nazioni_generate.add(nome_nazione)
            nazioni.append({
                'uuid': fake.uuid4(),
                'nome': nome_nazione,
                'tasso_inflazione': round(random.uniform(0.5, 10.0), 2),
                'popolazione': random.randint(500_000, 100_000_000)
            })
    return nazioni

def genera_banche():
    tipi = ["Pubblica", "Privata", "Digitale"]
    settori = ["Retail", "Corporate", "Investimenti"]
    banche = []
    for _ in range(NUM_BANCHE):
        banche.append({
            'uuid': fake.uuid4(),
            'nome': f"Banca {fake.company()}",
            'anno_fondazione': random.randint(1850, 2022),
            'tipo': random.choice(tipi),
            'filiali': random.randint(5, 500),
            'rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC']),
            'settore': random.choice(settori)
        })
    return banche

def genera_persone():
    persone = []
    for _ in range(NUM_PERSONE):
        data_nascita = fake.date_of_birth(minimum_age=18, maximum_age=85)
        eta = datetime.date.today().year - data_nascita.year
        persone.append({
            'uuid': fake.uuid4(),
            'nome': fake.first_name(),
            'cognome': fake.last_name(),
            'sesso': random.choice(['M', 'F']),
            'data_nascita': data_nascita.isoformat(),
            'eta': eta,
            'telefono': fake.phone_number(),
            'email': fake.email(),
            'codice_fiscale': fake.ssn(),
            'occupazione': fake.job()
        })
    return persone

def genera_carte_identita(persone):
    carte = []
    num_carte_totali = len(persone)  # Ora è uguale al numero di persone

    # Creiamo la lista di numeri univoci per il 70% delle carte
    num_carte_uniche = int(num_carte_totali * 0.7)  
    numeri_carte_unici = [fake.bothify(text='??######') for _ in range(num_carte_uniche)]

    # Selezioniamo il 30% di questi numeri e li assegnamo ad altre carte (ogni numero viene duplicato una volta)
    numeri_carte_duplicati = random.sample(numeri_carte_unici, num_carte_totali - num_carte_uniche)

    # Creiamo la lista finale di numeri di carte
    numeri_carte = numeri_carte_unici + numeri_carte_duplicati
    random.shuffle(numeri_carte)  # Mescoliamo per ottenere una distribuzione più naturale

    # Assegniamo i numeri di carta alle persone
    for persona, numero_carta in zip(persone, numeri_carte):
        rilascio = fake.date_between(start_date='-10y', end_date='-1y')
        scadenza = fake.date_between(start_date='today', end_date='+10y')
        carte.append({
            'uuid': fake.uuid4(),
            'codice_fiscale': persona['codice_fiscale'],
            'numero': numero_carta,  # Ora ogni numero duplicato è presente al massimo in due carte
            'data_rilascio': rilascio.isoformat(),
            'data_scadenza': scadenza.isoformat(),
            'ente_emittente': f"Comune di {fake.city()}"
        })
    return carte

def genera_conti_corrente(persone):
    tipi_conto = ["Personale", "Business", "Risparmio", "Investimento"]
    valute = ["EUR", "USD", "GBP", "CHF"]
    conti = []
    for _ in range(NUM_CONTI):
        persona = random.choice(persone)  # Assegna un conto a una persona casualmente
        apertura = fake.date_between(start_date='-10y', end_date='-1y')
        chiusura = fake.date_between(start_date='-1y', end_date='today') if random.random() < 0.1 else ''
        conti.append({
            'uuid': fake.uuid4(),
            'numero_conto': fake.random_number(digits=8, fix_len=True),
            'saldo': round(random.uniform(-5000, 50000), 2),
            'tipo_conto': random.choice(tipi_conto),
            'data_apertura': apertura.isoformat(),
            'data_chiusura': chiusura.isoformat() if chiusura else '',
            'IBAN': fake.iban(),
            'valuta': random.choice(valute),
            'limite_prelievo': round(random.uniform(100, 2000), 2),
            'codice_fiscale': persona["codice_fiscale"]  # Collega il conto a una persona
        })
    return conti

def salva_csv(filename, data, headers):
    filepath = output_dir / filename
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"Salvato {filename} ({len(data)} record)")

def main():
    nazioni = genera_nazioni()
    banche = genera_banche()
    persone = genera_persone()
    carte = genera_carte_identita(persone)
    conti = genera_conti_corrente(persone)

    salva_csv("nazioni.csv", nazioni, nazioni[0].keys())
    salva_csv("banche.csv", banche, banche[0].keys())
    salva_csv("persone.csv", persone, persone[0].keys())
    salva_csv("carte_identita.csv", carte, carte[0].keys())
    salva_csv("conti_corrente.csv", conti, conti[0].keys())

if __name__ == "__main__":
    main()
