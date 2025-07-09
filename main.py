import os
import numpy as np
import pandas as pd
from analiza import AnalyzerMultiSeason
from statystyki import StatystykiSezonu
from wizualizacje import (
    wykres_srednia_goli,
    wykres_faule_kartki,
    wykres_udzial_wygranych,
    wykres_srednia_strzalow,
    wykres_celnosc,
    wykres_celnosc_druzyn,
    wykres_strzaly_druzyn,
    wykres_gole_druzyn_na_sezon,
    wykres_xg_top10
)

# 📂 Wczytaj dane z folderu
folder_path = "C:/Moje/Python proj"
pliki_csv = [plik for plik in os.listdir(folder_path) if plik.endswith(".csv")]

# 🔄 Wczytaj dane i dodaj kolumnę 'Zwyciezca'
analyzer = AnalyzerMultiSeason(folder_path, pliki_csv)
df_all = analyzer.wczytaj_wszystkie_dane()
analyzer.dodaj_kolumne_zwyciezca()

# 📊 Obiekt klasy z analizami
stat = StatystykiSezonu(df_all)

# === ANALIZY TEKSTOWE ===
print("➡️ Średnia liczba goli w sezonie:")
print(stat.srednia_goli_per_sezon(), "\n")
print("-" * 80)

print("➡️ Średnia liczba fauli i kartek:")
print(stat.analiza_faul_kartki(), "\n")
print("-" * 80)

print("➡️ Udział zwycięstw gospodarzy, remisów i gości:")
print(stat.udzial_wygranych_home_away(), "\n")
print("-" * 80)

print("➡️ Średnia liczba strzałów:")
print(stat.srednia_strzalow(), "\n")
print("-" * 80)

print("➡️ Skuteczność strzałów (gole/strzały):")
print(stat.skutecznosc_strzalow(), "\n")
print("-" * 80)

print("➡️ Strzały i skuteczność drużyn:")
print(stat.statystyki_strzalow_druzyn(), "\n")
print("-" * 80)

print("➡️ Liczba goli strzelonych przez drużyny w każdym sezonie:")
print(stat.gole_druzyn_na_sezon(), "\n")
print("-" * 80)

print("➡️ Uproszczony wskaźnik xG na sezon:")
print(stat.xg_per_season(), "\n")
print("-" * 80)

# === WIZUALIZACJE ===

# 1. Średnia goli na sezon
df_gole = stat.srednia_goli_per_sezon()
wykres_srednia_goli(df_gole)
print("\n" + "="*100 + "\n")

# 2. Faule i kartki
df_faul_kartki = stat.analiza_faul_kartki()
wykres_faule_kartki(df_faul_kartki)
print("\n" + "="*100 + "\n")

# 3. Udział zwycięstw
df_udzial = stat.udzial_wygranych_home_away()
wykres_udzial_wygranych(df_udzial)
print("\n" + "="*100 + "\n")

# 4. Średnia liczba strzałów
df_srednia_strzalow = stat.srednia_strzalow()
lista_strzalow = df_srednia_strzalow["Średnia"].astype(float).tolist()
wykres_srednia_strzalow(lista_strzalow)
print("\n" + "="*100 + "\n")

# 5. Skuteczność strzałów
seria_celnosc = stat.skutecznosc_strzalow()
if isinstance(seria_celnosc, pd.Series):
    lista_celnosc = seria_celnosc.astype(float).tolist()
elif isinstance(seria_celnosc, pd.DataFrame) and "Celność [%]" in seria_celnosc.columns:
    lista_celnosc = seria_celnosc["Celność [%]"].astype(float).tolist()
else:
    raise ValueError("Nieoczekiwany format danych dla skuteczności strzałów.")
wykres_celnosc(lista_celnosc)
print("\n" + "="*100 + "\n")

# 6. Strzały i celność drużyn
df_druzyny_strzaly = stat.statystyki_strzalow_druzyn()
wykres_strzaly_druzyn(df_druzyny_strzaly)
print("\n" + "="*100 + "\n")
wykres_celnosc_druzyn(df_druzyny_strzaly)
print("\n" + "="*100 + "\n")

# 7. Gole drużyn na sezon
df_gole_sezon = stat.gole_druzyn_na_sezon()
wykres_gole_druzyn_na_sezon(df_gole_sezon)
print("\n" + "="*100 + "\n")

# 8. xG
df_xg_szeroko = stat.xg_per_season()
wykres_xg_top10(df_xg_szeroko)
print("\n" + "="*100 + "\n")
