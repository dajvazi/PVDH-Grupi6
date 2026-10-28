"""Mbledhja e të dhënave, definimi i tipeve, kualiteti.

Dalja: data/processed/kualiteti_raport.csv
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.utils import lexo_raw, ruaj  # noqa: E402

TIPET_STATISTIKORE = {
    "VITI": "Ordinal (konstant)",
    "MUAJI": "Ordinal / kohor",
    "Regjimi": "Nominal (konstant)",
    "Origjina": "Nominal",
    "Kodi Tarifor": "Nominal (hierarkik)",
    "Sasia": "Numerik (raport)",
    "Vlera Mallrave": "Numerik (raport)",
    "Netweight": "Numerik (raport)",
    "Taksa Doganës": "Numerik (raport)",
    "Taksa Akcizës": "Numerik (raport)",
    "Taksa TVSH-së": "Numerik (raport)",
}


def main():
    df = lexo_raw()
    print(f"Dataseti: {df.shape[0]:,} rreshta x {df.shape[1]} kolona")

    raport = []
    for kol in df.columns:
        s = df[kol]
        numerik = s.dtype.kind in "if"
        raport.append({
            "kolona": kol,
            "tipi_pandas": str(s.dtype),
            "tipi_statistikor": TIPET_STATISTIKORE.get(kol, ""),
            "vlera_unike": s.nunique(),
            "nan": int(s.isna().sum()),
            "nan_%": round(s.isna().mean() * 100, 2),
            "zero_%": round((s == 0).mean() * 100, 2) if numerik else None,
            "negative": int((s < 0).sum()) if numerik else None,
            "min": s.min() if numerik else None,
            "mediana": s.median() if numerik else None,
            "max": s.max() if numerik else None,
        })
    ruaj(pd.DataFrame(raport), "kualiteti_raport.csv")

    print("Duplikatë të plotë:", df.duplicated().sum())
    print("Duplikatë në çelësin (MUAJI, Origjina, Kodi Tarifor):",
          df.duplicated(["MUAJI", "Origjina", "Kodi Tarifor"]).sum())
    print("Përshkrime me problem encoding-u ('?'):",
          df["Kodi Tarifor"].str.contains("?", regex=False).sum())
    print("Origjina jo-shtete:",
          df.loc[df["Origjina"].str.startswith(("XX", "XY")), "Origjina"].unique().tolist())

    # Kontroll konsistence: TVSH ~ 18% e (vlera + dogana + akciza)
    baza = df["Vlera Mallrave"] + df["Taksa Doganës"] + df["Taksa Akcizës"]
    norma = (df["Taksa TVSH-së"] / baza).where(baza > 0)
    print("Norma mediane e TVSH-së:", round(norma.median(), 3))

if __name__ == "__main__":
    main()