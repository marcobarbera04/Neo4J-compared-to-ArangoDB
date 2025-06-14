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
NUM_CARTE = 25250
NUM_CONTI = 45000
NUM_NAZIONI = 45
NUM_BANCHE = 180

def genera_nazioni():
    nazioni = []
    for _ in range(NUM_NAZIONI):
        nazioni.append({
            'nome': fake.country(),
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
            'id': fake.uuid4(),
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
    for persona in persone:
        rilascio = fake.date_between(start_date='-10y', end_date='-1y')
        scadenza = fake.date_between(start_date='today', end_date='+10y')
        carte.append({
            'codice_fiscale': persona['codice_fiscale'],
            'numero': fake.bothify(text='??######'),
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
