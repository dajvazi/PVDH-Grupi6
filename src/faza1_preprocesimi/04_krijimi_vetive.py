"""Hapi 4 (Studenti B): krijimi i vetive të reja.

Hyrja:  data/processed/importet_integruara.csv
Dalja:  data/processed/importet_me_veti.csv
"""
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils import lexo, ruaj  # noqa: E402


def main():
    df = lexo("importet_integruara.csv")

    df["kodi_hs4"] = df["kodi_hs10"].str[:4]
    df["tremujori"] = (df["muaji"] - 1) // 3 + 1
    df["cmimi_per_kg"] = df["vlera"] / df["netweight"]
    df["taksa_totale"] = df["taksa_doganes"] + df["taksa_akcizes"] + df["taksa_tvsh"]
    df["norma_doganore"] = df["taksa_doganes"] / df["vlera"]
    df["norma_taksave"] = df["taksa_totale"] / df["vlera"]
    df["pjesa_e_tvsh"] = np.where(df["taksa_totale"] > 0, df["taksa_tvsh"] / df["taksa_totale"], 0)

    print(df[["cmimi_per_kg", "taksa_totale", "norma_doganore", "norma_taksave"]].describe().round(3))
    ruaj(df, "importet_me_veti.csv")


if __name__ == "__main__":
    main()
