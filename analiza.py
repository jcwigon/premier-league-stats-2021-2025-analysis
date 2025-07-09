import pandas as pd
import os

class AnalyzerMultiSeason:
    def __init__(self, folder_path, pliki_csv):
        self.folder_path = folder_path
        self.pliki_csv = pliki_csv
        self.df = None

    def wczytaj_wszystkie_dane(self):
        frames = []
        for plik in self.pliki_csv:
            sezon = plik.replace(".csv", "").replace("E0_", "")  # np. "21_22"
            pelna_sciezka = os.path.join(self.folder_path, plik)
            df = pd.read_csv(pelna_sciezka)
            df["Sezon"] = sezon
            frames.append(df)
        self.df = pd.concat(frames, ignore_index=True)
        print(f"✅ Załadowano {len(self.df)} meczów z {len(self.pliki_csv)} plików.")
        return self.df

    def dodaj_kolumne_zwyciezca(self):
        if self.df is None:
            print("⚠️ Najpierw załaduj dane!")
            return
        def zwyciezca(row):
            if row["FTHG"] > row["FTAG"]:
                return "Home"
            elif row["FTAG"] > row["FTHG"]:
                return "Away"
            else:
                return "Draw"
        self.df["Zwyciezca"] = self.df.apply(zwyciezca, axis=1)
        print("🏆 Dodano kolumnę 'Zwyciezca'.")

