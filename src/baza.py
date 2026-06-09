# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="solarni_paneli",
    user="postgres",
    password=""
)

cur = conn.cursor()

# ===== CITANJE SVIH TABELA U DATAFRAME =====

df_vlasnik = pd.read_sql("SELECT * FROM vlasnik", conn)
df_objekat = pd.read_sql("SELECT * FROM objekat", conn)
df_panel = pd.read_sql("SELECT * FROM solarni_panel", conn)
df_ocitavanje = pd.read_sql("SELECT * FROM ocitavanje", conn)
df_odrzavanje = pd.read_sql("SELECT * FROM odrzavanje", conn)

print("=== VLASNICI ===")
print(df_vlasnik)
print("\n=== OBJEKTI ===")
print(df_objekat)
print("\n=== SOLARNI PANELI ===")
print(df_panel)
print("\n=== OCITAVANJA ===")
print(df_ocitavanje)
print("\n=== ODRZAVANJA ===")
print(df_odrzavanje)

# ===== CRUD OPERACIJE =====

# CREATE
cur.execute("""
INSERT INTO vlasnik (ime, prezime, email, telefon, adresa)
VALUES ('Nikola', 'Djordjevic', 'nikola@gmail.com', '0691234567', 'Beograd, Terazije 10')
""")
conn.commit()
print("\n=== CREATE - DODAN NOV VLASNIK ===")
df = pd.read_sql("SELECT * FROM vlasnik", conn)
print(df)

# UPDATE
cur.execute("""
UPDATE vlasnik SET email = 'nikola.novi@gmail.com' WHERE ime = 'Nikola'
""")
conn.commit()
print("\n=== UPDATE - AZURIRAN EMAIL ===")
df = pd.read_sql("SELECT * FROM vlasnik WHERE ime = 'Nikola'", conn)
print(df)

# DELETE
cur.execute("DELETE FROM vlasnik WHERE ime = 'Nikola'")
conn.commit()
print("\n=== DELETE - OBRISAN VLASNIK ===")
df = pd.read_sql("SELECT * FROM vlasnik", conn)
print(df)

# ===== JOIN UPITI =====

print("\n=== UPIT 1 - Vlasnici i njihovi objekti ===")
df = pd.read_sql("""
SELECT v.ime, v.prezime, o.naziv, o.tip
FROM vlasnik v
JOIN objekat o ON v.vlasnik_id = o.vlasnik_id
""", conn)
print(df)

print("\n=== UPIT 2 - Objekti i njihovi paneli ===")
df = pd.read_sql("""
SELECT o.naziv, p.model, p.snaga_kw, p.status
FROM objekat o
JOIN solarni_panel p ON o.objekat_id = p.objekat_id
""", conn)
print(df)

print("\n=== UPIT 3 - Aktivni paneli sa vlasnikom ===")
df = pd.read_sql("""
SELECT v.ime, v.prezime, p.model, p.status
FROM vlasnik v
JOIN objekat o ON v.vlasnik_id = o.vlasnik_id
JOIN solarni_panel p ON o.objekat_id = p.objekat_id
WHERE p.status = 'aktivan'
""", conn)
print(df)

print("\n=== UPIT 4 - Odrzavanja skuplja od 500 ===")
df = pd.read_sql("""
SELECT v.ime, v.prezime, p.model, od.tip_servisa, od.troskovi
FROM vlasnik v
JOIN objekat o ON v.vlasnik_id = o.vlasnik_id
JOIN solarni_panel p ON o.objekat_id = p.objekat_id
JOIN odrzavanje od ON p.panel_id = od.panel_id
WHERE od.troskovi > 500
""", conn)
print(df)

print("\n=== UPIT 5 - Paneli sa proizvodnjom vecom od 30 kwh ===")
df = pd.read_sql("""
SELECT v.ime, v.prezime, p.model, oc.proizvedena_energija_kwh
FROM vlasnik v
JOIN objekat o ON v.vlasnik_id = o.vlasnik_id
JOIN solarni_panel p ON o.objekat_id = p.objekat_id
JOIN ocitavanje oc ON p.panel_id = oc.panel_id
WHERE oc.proizvedena_energija_kwh > 30
""", conn)
print(df)

print("\n=== UPIT 6 - Stambeni objekti sa panelima ===")
df = pd.read_sql("""
SELECT o.naziv, o.tip, p.model, p.snaga_kw
FROM objekat o
JOIN solarni_panel p ON o.objekat_id = p.objekat_id
WHERE o.tip = 'stambeni'
""", conn)
print(df)

print("\n=== UPIT 7 - Ukupna snaga panela po vlasniku ===")
df = pd.read_sql("""
SELECT v.ime, v.prezime, SUM(p.snaga_kw) as ukupna_snaga
FROM vlasnik v
JOIN objekat o ON v.vlasnik_id = o.vlasnik_id
JOIN solarni_panel p ON o.objekat_id = p.objekat_id
GROUP BY v.ime, v.prezime
""", conn)
print(df)

print("\n=== UPIT 8 - Paneli instalirani nakon 2020 ===")
df = pd.read_sql("""
SELECT v.ime, v.prezime, p.model, p.datum_instalacije
FROM vlasnik v
JOIN objekat o ON v.vlasnik_id = o.vlasnik_id
JOIN solarni_panel p ON o.objekat_id = p.objekat_id
WHERE p.datum_instalacije > '2020-01-01'
""", conn)
print(df)

print("\n=== UPIT 9 - Prosjecna temperatura po panelu ===")
df = pd.read_sql("""
SELECT p.model, AVG(oc.temperatura_c) as prosjecna_temp
FROM solarni_panel p
JOIN ocitavanje oc ON p.panel_id = oc.panel_id
GROUP BY p.model
""", conn)
print(df)

print("\n=== UPIT 10 - Paneli sa snagom vecom od 10 kw i vlasnik ===")
df = pd.read_sql("""
SELECT v.ime, v.prezime, p.model, p.snaga_kw, o.naziv
FROM vlasnik v
JOIN objekat o ON v.vlasnik_id = o.vlasnik_id
JOIN solarni_panel p ON o.objekat_id = p.objekat_id
WHERE p.snaga_kw > 10
""", conn)
print(df)

cur.close()
conn.close()
