import pandas as pd
import numpy as np

class StatystykiSezonu:
    def __init__(self, df):
        self.df = df.copy()

    def srednia_goli_per_sezon(self):
        if 'FTHG' not in self.df or 'FTAG' not in self.df:
            print("❌ Brakuje kolumn FTHG lub FTAG.")
            return None
        
        self.df["Gole_razem"] = self.df["FTHG"] + self.df["FTAG"]
        srednie = self.df.groupby("Sezon")["Gole_razem"].mean().round(2)
        print("⚽ Średnia liczba goli na mecz w każdym sezonie:")
        print(srednie)
        return srednie

    def analiza_faul_kartki(self):
        if not all(col in self.df.columns for col in ['HF', 'AF', 'HY', 'AY', 'HR', 'AR']):
            print("❌ Brakuje kolumn do analizy sędziowania.")
            return None

        print("🧑‍⚖️ Analiza fauli i kartek (gospodarze vs goście):")

        dane = {
            "Średnie faule": {
                "Home": round(self.df["HF"].mean(), 2),
                "Away": round(self.df["AF"].mean(), 2)
            },
            "Żółte kartki": {
                "Home": round(self.df["HY"].mean(), 2),
                "Away": round(self.df["AY"].mean(), 2)
            },
            "Czerwone kartki": {
                "Home": round(self.df["HR"].mean(), 3),
                "Away": round(self.df["AR"].mean(), 3)
            }
        }

        df_porownanie = pd.DataFrame(dane).T
        print(df_porownanie)
        return df_porownanie

    def udzial_wygranych_home_away(self):
        if "Zwyciezca" not in self.df.columns:
            print("❌ Brakuje kolumny 'Zwyciezca'. Najpierw ją dodaj.")
            return None

        print("📊 Udział wygranych: Gospodarz vs Gość vs Remis")

        udzialy = self.df["Zwyciezca"].value_counts(normalize=True) * 100
        udzialy = udzialy.round(2).rename("Udział [%]")

        df_udzial = udzialy.reset_index().rename(columns={"index": "Wynik"})
        print(df_udzial)
        return df_udzial

    def srednia_strzalow(self):
        if not all(col in self.df.columns for col in ['HS', 'AS']):
            print("❌ Brakuje kolumn 'HS' lub 'AS'.")
            return None

        print("🎯 Średnia liczba strzałów na mecz:")

        srednie = {
            "Strzały gospodarzy": round(self.df['HS'].mean(), 2),
            "Strzały gości": round(self.df['AS'].mean(), 2)
        }

        df_srednie = pd.DataFrame(srednie.items(), columns=["Rodzaj", "Średnia"])
        print(df_srednie)
        return df_srednie

    def skutecznosc_strzalow(self):
        if not all(col in self.df.columns for col in ['HS', 'HST', 'AS', 'AST']):
            print("❌ Brakuje kolumn do obliczenia celności strzałów.")
            return None

        print("🥅 Skuteczność (celność) strzałów:")

        df_copy = self.df[(self.df["HS"] > 0) & (self.df["AS"] > 0)].copy()
        df_copy["Celność Home"] = df_copy["HST"] / df_copy["HS"]
        df_copy["Celność Away"] = df_copy["AST"] / df_copy["AS"]

        cel_home = round(df_copy["Celność Home"].mean() * 100, 2)
        cel_away = round(df_copy["Celność Away"].mean() * 100, 2)

        df_celnosc = pd.DataFrame({
            "Drużyna": ["Gospodarze", "Goście"],
            "Celność [%]": [cel_home, cel_away]
        })

        print(df_celnosc)
        return df_celnosc

    def statystyki_strzalow_druzyn(self):
        print("📊 Analiza strzałów i celności dla każdej drużyny (dom/wyjazd)")

        df = self.df.copy()
        wyniki = []

        teams = pd.concat([df["HomeTeam"], df["AwayTeam"]]).unique()

        for team in teams:
            dom = df[df["HomeTeam"] == team]
            sr_strzaly_dom = dom["HS"].mean()
            sr_celnosc_dom = (dom["HST"] / dom["HS"]).replace([np.inf, -np.inf], np.nan).dropna().mean()

            wyj = df[df["AwayTeam"] == team]
            sr_strzaly_wyj = wyj["AS"].mean()
            sr_celnosc_wyj = (wyj["AST"] / wyj["AS"]).replace([np.inf, -np.inf], np.nan).dropna().mean()

            wyniki.append({
                "Drużyna": team,
                "Sr. strzały (dom)": round(sr_strzaly_dom, 2),
                "Sr. celność (dom)": round(sr_celnosc_dom * 100, 2) if pd.notnull(sr_celnosc_dom) else None,
                "Sr. strzały (wyjazd)": round(sr_strzaly_wyj, 2),
                "Sr. celność (wyjazd)": round(sr_celnosc_wyj * 100, 2) if pd.notnull(sr_celnosc_wyj) else None,
            })

        df_wyniki = pd.DataFrame(wyniki).sort_values("Drużyna").reset_index(drop=True)
        print(df_wyniki)
        return df_wyniki

    def gole_druzyn_na_sezon(self):
        df = self.df.copy()
        gole = []

        sezony = df["Sezon"].unique()
        for sezon in sezony:
            df_sezon = df[df["Sezon"] == sezon]

            gole_home = df_sezon.groupby("HomeTeam")["FTHG"].sum().reset_index()
            gole_home.columns = ["Druzyna", "Gole_dom"]

            gole_away = df_sezon.groupby("AwayTeam")["FTAG"].sum().reset_index()
            gole_away.columns = ["Druzyna", "Gole_wyj"]

            suma = pd.merge(gole_home, gole_away, on="Druzyna", how="outer").fillna(0)
            suma["Gole_razem"] = suma["Gole_dom"] + suma["Gole_wyj"]
            suma["Sezon"] = sezon

            gole.append(suma[["Druzyna", "Sezon", "Gole_razem"]])

        df_gole = pd.concat(gole, ignore_index=True)
        df_gole_szeroko = df_gole.pivot_table(
            index="Druzyna",
            columns="Sezon",
            values="Gole_razem",
            fill_value=0
        ).reset_index()

        ostatni_sezon = sorted(df["Sezon"].unique())[-1]
        df_gole_szeroko = df_gole_szeroko.sort_values(by=ostatni_sezon, ascending=False).reset_index(drop=True)
        df_gole_szeroko.insert(0, "Lp.", range(1, len(df_gole_szeroko) + 1))

        return df_gole_szeroko

    def xg_per_season(self):
        df = self.df.copy()

        df = df[(df['HST'] > 0) & (df['AST'] > 0)]
        skutecznosc_home = (df["FTHG"] / df["HST"]).mean()
        skutecznosc_away = (df["FTAG"] / df["AST"]).mean()
        sr_skutecznosc = (skutecznosc_home + skutecznosc_away) / 2

        wyniki = []
        sezony = df["Sezon"].unique()
        teams = pd.concat([df["HomeTeam"], df["AwayTeam"]]).unique()

        for sezon in sezony:
            df_sezon = df[df["Sezon"] == sezon]
            for team in teams:
                mecze_dom = df_sezon[df_sezon["HomeTeam"] == team]
                mecze_wyj = df_sezon[df_sezon["AwayTeam"] == team]

                n_matches = len(mecze_dom) + len(mecze_wyj)

                celne_dom = mecze_dom["HST"].sum()
                celne_wyj = mecze_wyj["AST"].sum()
                suma_celnych = celne_dom + celne_wyj

                if n_matches > 0:
                    sr_celne_na_mecz = suma_celnych / n_matches
                    xg = sr_celne_na_mecz * sr_skutecznosc * n_matches
                else:
                    xg = 0

                wyniki.append({
                    "Drużyna": team,
                    "Sezon": sezon,
                    "xG (szacowane)": round(xg, 2)
                })

        df_xg = pd.DataFrame(wyniki)
        df_xg_szeroko = df_xg.pivot_table(index="Drużyna", columns="Sezon", values="xG (szacowane)", fill_value=0).reset_index()
        ostatni_sezon = sorted(df["Sezon"].unique())[-1]
        df_xg_szeroko = df_xg_szeroko.sort_values(by=ostatni_sezon, ascending=False).reset_index(drop=True)
        df_xg_szeroko.insert(0, "Lp.", range(1, len(df_xg_szeroko) + 1))

        return df_xg_szeroko

    def xg_per_season(self):
            
        df = self.df.copy()
        df = df[(df['HST'] > 0) & (df['AST'] > 0)]

        skutecznosc_home = (df["FTHG"] / df["HST"]).mean()
        skutecznosc_away = (df["FTAG"] / df["AST"]).mean()
        sr_skutecznosc = (skutecznosc_home + skutecznosc_away) / 2

        wyniki = []
        sezony = df["Sezon"].unique()
        teams = pd.concat([df["HomeTeam"], df["AwayTeam"]]).unique()

        for sezon in sezony:
            df_sezon = df[df["Sezon"] == sezon]
            for team in teams:
                hst_team = df_sezon[df_sezon["HomeTeam"] == team]["HST"].sum()
                ast_team = df_sezon[df_sezon["AwayTeam"] == team]["AST"].sum()
                strzaly_celne = hst_team + ast_team
                xg = round(strzaly_celne * sr_skutecznosc, 2)
                wyniki.append({
                    "Drużyna": team,
                    "Sezon": sezon,
                    "xG (szacowane)": xg
                })

        df_xg = pd.DataFrame(wyniki)
        df_xg_szeroko = df_xg.pivot_table(index="Drużyna", columns="Sezon", values="xG (szacowane)", fill_value=0).reset_index()
        ostatni_sezon = sorted(df["Sezon"].unique())[-1]
        df_xg_szeroko = df_xg_szeroko.sort_values(by=ostatni_sezon, ascending=False).reset_index(drop=True)
        df_xg_szeroko.insert(0, "Lp.", range(1, len(df_xg_szeroko) + 1))

        return df_xg_szeroko






