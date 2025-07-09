# mongo_utworz_baze.py
from pymongo import MongoClient
import pandas as pd
import os

# 🔗 Połącz z lokalnym serwerem MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 🧱 Stwórz bazę i kolekcję
db = client["PremierLeague"]
kolekcja = db["mecze"]

# 📂 Lista plików CSV z danymi meczowymi i odpowiadające im sezony
pliki = [
    ("E0_21_22.csv", "2021/2022"),
    ("E0_22_23.csv", "2022/2023"),
    ("E0_23_24.csv", "2023/2024"),
    ("E0_24_25.csv", "2024/2025")
]

# 🔁 Import danych tylko jeśli kolekcja jest pusta
if kolekcja.count_documents({}) == 0:
    print("⏳ Importowanie danych do MongoDB...")

    for plik, sezon in pliki:
        if os.path.exists(plik):
            df = pd.read_csv(plik)
            df["Sezon"] = sezon
            dane_json = df.to_dict(orient="records")
            kolekcja.insert_many(dane_json)
            print(f"✅ Wstawiono dane z {plik} (Sezon: {sezon})")
        else:
            print(f"⚠️ Plik {plik} nie został znaleziony!")

    print("✅ Import zakończony.")
else:
    print("ℹ️ Dane już istnieją w bazie. Import pominięty.")
