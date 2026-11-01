"""Hapi 6: transformimi, reduktimi i dimensionit, zgjedhja e nënbashkësisë së vetive.

Hyrja:  data/processed/importet_diskretizuara.csv
Daljet: data/processed/importet_final.csv, importet_per_vizualizim.csv, pca_varianca.csv,
        korrelacioni.csv, vetite_e_zgjedhura.txt, histogramet_log.png
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

sys.path.append(str(Path(__file__).resolve().parents[2]))
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
    # Decimal scaling: v / 10^j, ku j është numri më i vogël që max|v'| < 1
    for k in NUMERIKE:
        j = int(np.floor(np.log10(df[k].abs().max()))) + 1
        df[f"ds_{k}"] = df[k] / 10 ** j

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

    # 1) Largimi i vetive binare pothuajse konstante (variancë p(1-p) < 0.01, pra < ~1% njësha)
    binare = ["ka_sasi", "ka_akcize", "ka_dogane", "nga_BE", "nga_CEFTA", "eshte_shtet"]
    vt = VarianceThreshold(threshold=0.01).fit(X[binare])
    hiqen = [k for k, mbahet in zip(binare, vt.get_support()) if not mbahet]
    pas_variances = [k for k in kandidate if k not in hiqen]
    print("Variancat e vetive binare:", dict(zip(binare, vt.variances_.round(4))))
    print("Hiqen (variancë < 0.01):", hiqen)

    # 2) Largimi i vetive redundante: nga çdo çift me |r| > 0.9 mbahet e para
    korr = X[pas_variances].corr().abs()
    ruaj(korr.round(3).reset_index(), "korrelacioni.csv")
    siper = korr.where(np.triu(np.ones(korr.shape, dtype=bool), k=1))
    redundante = [k for k in siper.columns if (siper[k] > 0.9).any()]
    zgjedhura = [k for k in pas_variances if k not in redundante]
    print("Hiqen (redundante, |r| > 0.9):", redundante)
    (PROCESSED / "vetite_e_zgjedhura.txt").write_text("\n".join(zgjedhura), encoding="utf-8")

    # 3) PCA (vetëm numerike, pas standardizimit)
    pca = PCA().fit(StandardScaler().fit_transform(X[zgjedhura]))
    varianca = pd.DataFrame({
        "komponenti": [f"PC{i + 1}" for i in range(pca.n_components_)],
        "varianca": pca.explained_variance_ratio_.round(4),
        "kumulative": pca.explained_variance_ratio_.cumsum().round(4),
    })
    ruaj(varianca, "pca_varianca.csv")
    k95 = int((varianca["kumulative"] < 0.95).sum()) + 1
    print(f"PCA: {k95} komponentë ruajnë ≥95% të variancës nga {len(zgjedhura)} veti")

    ruaj(df, "importet_final.csv")

    # Skedar më i lehtë për vizualizim në Power BI / Tableau (faza 3)
    kolonat_viz = ["muaji", "tremujori", "kodi_vendit", "emri_vendit", "kontinenti", "nga_BE", "nga_CEFTA",
                   "seksioni_hs", "emri_seksionit", "kapitulli_hs", "kodi_hs4", "kodi_hs10", "pershkrimi",
                   "vlera", "netweight", "taksa_doganes", "taksa_akcizes", "taksa_tvsh", "taksa_totale",
                   "cmimi_per_kg", "kategoria_vleres", "intervali_doganor"]
    viz = df[kolonat_viz].copy()
    viz["data"] = pd.to_datetime("2025-" + viz["muaji"].astype(str) + "-01")
    viz.to_csv(PROCESSED / "importet_per_vizualizim.csv", index=False, encoding="utf-8-sig")
    print(f"  -> ruajtur importet_per_vizualizim.csv: {viz.shape[0]:,} rreshta x {viz.shape[1]} kolona")


if __name__ == "__main__":
    main()