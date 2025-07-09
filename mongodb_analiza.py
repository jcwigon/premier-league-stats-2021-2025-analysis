from pymongo import MongoClient
import pandas as pd

# 🔌 Połączenie z lokalną bazą MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PremierLeague"]
kolekcja = db["mecze"]

# 🧾 Przykład 1: Wynik meczu Arsenal vs Liverpool, sezon 2024/2025
mecz = kolekcja.find_one({
    "HomeTeam": "Arsenal",
    "AwayTeam": "Liverpool",
    "Sezon": "2024/2025"
})
if mecz:
    print("➡️ Wynik meczu Arsenal - Liverpool (2024/2025):")
    print(f"{mecz['HomeTeam']} {mecz['FTHG']} : {mecz['FTAG']} {mecz['AwayTeam']}")
    print("➡️ Kartki:")
    print(f"Żółte: {mecz['HomeTeam']} - {mecz['HY']}, {mecz['AwayTeam']} - {mecz['AY']}")
    print(f"Czerwone: {mecz['HomeTeam']} - {mecz['HR']}, {mecz['AwayTeam']} - {mecz['AR']}")
    print()

# 🧾 Przykład 2: Wynik + faule w meczu Man City vs Man United, sezon 2023/2024
mecz2 = kolekcja.find_one({
    "HomeTeam": "Man City",
    "AwayTeam": "Man United",
    "Sezon": "2023/2024"
})
if mecz2:
    print("➡️ Wynik meczu Man City - Man United (2023/2024):")
    print(f"{mecz2['HomeTeam']} {mecz2['FTHG']} : {mecz2['FTAG']} {mecz2['AwayTeam']}")
    print(f"Faule: {mecz2['HomeTeam']} - {mecz2['HF']}, {mecz2['AwayTeam']} - {mecz2['AF']}")
    print()

# 🧾 Przykład 3: Najwięcej celnych strzałów – sezon 2022/2023
wszystkie = list(kolekcja.find({"Sezon": "2022/2023"}))
df = pd.DataFrame(wszystkie)

if "HST" in df.columns and "AST" in df.columns:
    df["HST"] = pd.to_numeric(df["HST"], errors="coerce")
    df["AST"] = pd.to_numeric(df["AST"], errors="coerce")

    suma_dom = df.groupby("HomeTeam")["HST"].sum()
    suma_wyj = df.groupby("AwayTeam")["AST"].sum()
    suma_celnych = suma_dom.add(suma_wyj, fill_value=0)

    top_team = suma_celnych.idxmax()
    top_value = int(suma_celnych.max())

    print("➡️ Celne strzały (2022/2023):")
    print(f"W sezonie 22/23 w Premier League najwięcej strzałów celnych oddała drużyna {top_team} – {top_value} strzałów.")
    print()

# 📊 Ogólna analiza na wszystkich danych z MongoDB
wszystkie_dane = list(kolekcja.find({}))
dane_mongo = pd.DataFrame(wszystkie_dane)

# 🔢 Średnia goli na mecz
dane_mongo["Gole"] = dane_mongo["FTHG"] + dane_mongo["FTAG"]
print("➡️ Średnia liczba goli na mecz:", dane_mongo["Gole"].mean())
print()

# 🔁 Najczęściej występujące wyniki
dane_mongo["Wynik"] = dane_mongo["FTHG"].astype(str) + "-" + dane_mongo["FTAG"].astype(str)
print("➡️ Najczęściej występujące wyniki:")
print(dane_mongo["Wynik"].value_counts().head())
print()

# 🏠 Najwięcej wygranych u siebie (po liczbie goli u siebie)
print("➡️ Najwięcej goli strzelonych u siebie:")
print(dane_mongo.groupby("HomeTeam")["FTHG"].sum().sort_values(ascending=False).head())
print()

# ✅ Zakończenie
print("✅ To była przykładowa analiza danych z wykorzystaniem bazy NoSQL (MongoDB).")
print("   Pokazuje alternatywne podejście do analizy – zamiast CSV + Pandas, dane są w bazie danych.")
