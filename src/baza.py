import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="solarni_paneli",
    user="postgres",
    password=""
)

# Citanje svih tabela u DataFrame
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

conn.close()