"""Hapi 5 (Studenti C): diskretizimi dhe binarizimi.

Hyrja:  data/processed/importet_me_veti.csv
Dalja:  data/processed/importet_diskretizuara.csv
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils import lexo, ruaj  # noqa: E402


def main():
    df = lexo("importet_me_veti.csv")

    # --- Diskretizimi ---
    # Sipas kuartileve (frekuencë e barabartë)
    df["kategoria_vleres"] = pd.qcut(df["vlera"], q=4,
                                     labels=["e vogël", "mesatare", "e madhe", "shumë e madhe"])
    print(df["kategoria_vleres"].value_counts().sort_index())
    ruaj(df, "importet_diskretizuara.csv")


if __name__ == "__main__":
    main()