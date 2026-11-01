"""Hapi 5: diskretizimi dhe binarizimi.

Hyrja:  data/processed/importet_me_veti.csv
Dalja:  data/processed/importet_diskretizuara.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.utils import lexo, ruaj  # noqa: E402


def main():
    df = lexo("importet_me_veti.csv")

    # --- Diskretizimi ---
    # Sipas kuartileve (frekuencë e barabartë)
    df["kategoria_vleres"] = pd.qcut(df["vlera"], q=4,
                                     labels=["e vogël", "mesatare", "e madhe", "shumë e madhe"])
    # Sipas intervaleve me kuptim (gjerësi e caktuar nga domeni)
    df["intervali_doganor"] = pd.cut(df["norma_doganore"], bins=[-0.001, 0, 0.05, 0.10, float("inf")],
                                     labels=["0%", "0-5%", "5-10%", ">10%"])
    # Me gjerësi të barabartë (equal-width) mbi log(vlera), për krahasim me qcut
    df["bin_gjeresi"] = pd.cut(np.log1p(df["vlera"]), bins=4,
                               labels=["e vogël", "mesatare", "e madhe", "shumë e madhe"])
    print("Frekuencë e barabartë (qcut):\n", df["kategoria_vleres"].value_counts().sort_index())
    print("Gjerësi e barabartë (cut):\n", df["bin_gjeresi"].value_counts().sort_index())
    print(df["intervali_doganor"].value_counts().sort_index())

    # Zbutja (smoothing) me mesataren e bin-it
    df["vlera_zbutur"] = df.groupby("kategoria_vleres", observed=True)["vlera"].transform("mean")

    # --- Binarizimi ---
    df["ka_akcize"] = (df["taksa_akcizes"] > 0).astype(int)
    df["ka_dogane"] = (df["taksa_doganes"] > 0).astype(int)
    # ka_sasi, nga_BE, nga_CEFTA, eshte_shtet janë krijuar në hapat 2 dhe 3

    # One-hot encoding për kolonat nominale me pak kategori
    # (join në vend të get_dummies(df, ...) që të ruhen edhe kolonat origjinale për fazat 2 dhe 3)
    df = df.join(pd.get_dummies(df[["kontinenti", "tremujori"]], columns=["kontinenti", "tremujori"],
                                prefix=["kont", "tm"], dtype=int))

    ruaj(df, "importet_diskretizuara.csv")


if __name__ == "__main__":
    main()