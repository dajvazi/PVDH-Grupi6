"""Hapi 6: transformimi, reduktimi i dimensionit, zgjedhja e nënbashkësisë së vetive.

Hyrja:  data/processed/importet_diskretizuara.csv
Daljet: data/processed/importet_final.csv, pca_varianca.csv, korrelacioni.csv,
        vetite_e_zgjedhura.txt, histogramet_log.png
"""
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import MinMaxScaler, StandardScaler

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils import PROCESSED, lexo, ruaj  # noqa: E402

NUMERIKE = ["vlera", "netweight", "taksa_doganes", "taksa_akcizes", "taksa_tvsh",
            "taksa_totale", "cmimi_per_kg"]

def main():
    df = lexo("importet_diskretizuara.csv")

    # --- Transformimi ---
    for kol in NUMERIKE:
        df[f"log_{kol}"] = np.log1p(df[kol])
    log_kol = [f"log_{k}" for k in NUMERIKE]
    df[[f"z_{k}" for k in NUMERIKE]] = StandardScaler().fit_transform(df[log_kol])
    df[[f"mm_{k}" for k in NUMERIKE]] = MinMaxScaler().fit_transform(df[log_kol])

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].hist(df["vlera"], bins=50)
    ax[0].set_title("Vlera (€) para transformimit")
    ax[1].hist(df["log_vlera"], bins=50)
    ax[1].set_title("log1p(Vlera) pas transformimit")
    fig.tight_layout()
    fig.savefig(PROCESSED / "histogramet_log.png", dpi=120)

    # --- Reduktimi i dimensionit ---
    kandidate = log_kol + ["norma_doganore", "norma_taksave", "pjesa_e_tvsh", "ka_sasi",
                           "ka_akcize", "ka_dogane", "nga_BE", "nga_CEFTA", "eshte_shtet", "muaji"]
    X = df[kandidate]

if __name__ == "__main__":
    main()