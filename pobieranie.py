import os
import pandas as pd

class Downloader:
    def __init__(self, sciezka_folderu):
        self.folder = sciezka_folderu

    def lista_csv(self):
        return sorted([
            f for f in os.listdir(self.folder)
            if f.endswith(".csv")
        ])

    def pelna_sciezka(self, plik_csv):
        return os.path.join(self.folder, plik_csv)

    def czy_istnieje(self, plik_csv):
        return os.path.exists(self.pelna_sciezka(plik_csv))


# ⬇️ Ta funkcja MUSI być poza klasą, żeby można ją było importować:
def wczytaj_dane_z_folderu(folder_path):
    
    all_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    df_all = []

    for file in all_files:
        path = os.path.join(folder_path, file)
        df = pd.read_csv(path)

        # Sezon na podstawie nazwy pliku
        sezon = os.path.splitext(file)[0].replace("Premier League ", "").replace("-", "_").replace(" ", "_")
        df["Sezon"] = sezon

        df_all.append(df)

    return pd.concat(df_all, ignore_index=True)
