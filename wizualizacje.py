import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def wykres_srednia_goli(df_gole):
    df_gole = df_gole.reset_index()
    df_gole.columns = ["Sezon", "Średnia goli"]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df_gole["Sezon"], df_gole["Średnia goli"], color="skyblue", edgecolor="black")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')
    plt.title("Średnia liczba goli na mecz w sezonie", fontsize=16)
    plt.xlabel("Sezon", fontsize=12)
    plt.ylabel("Gole na mecz", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def wykres_faule_kartki(df_kartki):
    kategorie = df_kartki.index.tolist()
    home = df_kartki["Home"].values
    away = df_kartki["Away"].values
    x = np.arange(len(kategorie))
    width = 0.35
    plt.figure(figsize=(10, 6))
    bars1 = plt.bar(x - width/2, home, width, label='Gospodarz', color='lightcoral')
    bars2 = plt.bar(x + width/2, away, width, label='Gość', color='steelblue')
    for bars in [bars1, bars2]:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')
    plt.xticks(x, kategorie)
    plt.ylabel("Średnia liczba")
    plt.title("Faule i kartki – gospodarze vs goście")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def wykres_udzial_wygranych(df_udzial):
    labels = df_udzial["Zwyciezca"].tolist()
    sizes = df_udzial["Udział [%]"].tolist()
    colors = ["lightgreen", "skyblue", "orange"]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors, wedgeprops={"edgecolor": "white"})
    plt.title("Udział wyników: Gospodarz vs Gość vs Remis")
    plt.axis("equal")
    plt.show()

def wykres_srednia_strzalow(srednia_strzalow):
    druzyny = ["Gospodarze", "Goście"]
    plt.figure(figsize=(8, 6))
    bars = plt.bar(druzyny, srednia_strzalow, color=["lightcoral", "steelblue"])
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, f"{yval:.2f}", ha="center", fontsize=11)
    plt.title("Średnia liczba strzałów na mecz – Gospodarze vs Goście")
    plt.ylabel("Liczba strzałów")
    plt.ylim(0, max(srednia_strzalow) + 3)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

def wykres_celnosc(celnosc):
    druzyny = ["Gospodarze", "Goście"]
    plt.figure(figsize=(8, 6))
    bars = plt.bar(druzyny, celnosc, color=["salmon", "skyblue"])
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.3, f"{yval:.2f}%", ha="center", fontsize=11)
    plt.title("Skuteczność (celność) strzałów – Gospodarze vs Goście")
    plt.ylabel("Celność [%]")
    plt.ylim(0, max(celnosc) + 5)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

def wykres_celnosc_druzyn(df_druzyny_strzaly):
    df_celnosc_sorted = df_druzyny_strzaly.sort_values(by="Sr. celność (dom)", ascending=False)
    druzyny = df_celnosc_sorted["Drużyna"]
    celnosc_dom = df_celnosc_sorted["Sr. celność (dom)"]
    celnosc_wyjazd = df_celnosc_sorted["Sr. celność (wyjazd)"]
    x = np.arange(len(druzyny))
    width = 0.35
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(x - width/2, celnosc_dom, width, label="Dom", color="green")
    ax.bar(x + width/2, celnosc_wyjazd, width, label="Wyjazd", color="orange")
    ax.set_title("Skuteczność strzałów: Dom vs Wyjazd (procent celnych)")
    ax.set_xlabel("Drużyna")
    ax.set_ylabel("Celność [%]")
    ax.set_xticks(x)
    ax.set_xticklabels(druzyny, rotation=45, ha="right")
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def wykres_strzaly_druzyn(df_druzyny_strzaly):
    df_strzaly_sorted = df_druzyny_strzaly.sort_values(by="Sr. strzały (dom)", ascending=False)
    druzyny = df_strzaly_sorted["Drużyna"]
    strzaly_dom = df_strzaly_sorted["Sr. strzały (dom)"]
    strzaly_wyjazd = df_strzaly_sorted["Sr. strzały (wyjazd)"]
    x = np.arange(len(druzyny))
    width = 0.35
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(x - width/2, strzaly_dom, width, label="Dom", color="steelblue")
    ax.bar(x + width/2, strzaly_wyjazd, width, label="Wyjazd", color="salmon")
    ax.set_title("Średnia liczba strzałów: Dom vs Wyjazd")
    ax.set_xlabel("Drużyna")
    ax.set_ylabel("Średnia liczba strzałów")
    ax.set_xticks(x)
    ax.set_xticklabels(druzyny, rotation=45, ha="right")
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def wykres_xg_top10(df_xg_szeroko):
    ostatni_sezon = df_xg_szeroko.columns[-1]
    df_top10 = df_xg_szeroko.head(10).copy()
    df_long = df_top10.melt(id_vars=["Lp.", "Drużyna"], var_name="Sezon", value_name="xG")
    df_long = df_long[df_long["Sezon"].str.contains("_")]
    plt.figure(figsize=(12, 6))
    for druzyna in df_long["Drużyna"].unique():
        dane = df_long[df_long["Drużyna"] == druzyna]
        plt.plot(dane["Sezon"], dane["xG"], marker="o", label=druzyna)
    plt.title("xG (szacowane) w sezonach – TOP 10 drużyn", fontsize=14)
    plt.xlabel("Sezon")
    plt.ylabel("xG (szacowane)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

def wykres_gole_druzyn_na_sezon(df_gole_sezon):
    df_plot = df_gole_sezon.copy()
    sezony = [col for col in df_plot.columns if col not in ["Lp.", "Druzyna"]]
    for sezon in sezony:
        plt.figure(figsize=(14, 6))
        df_sorted = df_plot.sort_values(by=sezon, ascending=False)
        plt.bar(df_sorted["Druzyna"], df_sorted[sezon], color="skyblue", edgecolor="black")
        plt.title(f"Liczba goli strzelonych przez drużyny – sezon {sezon}", fontsize=14)
        plt.xlabel("Drużyna")
        plt.ylabel("Liczba goli")
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()