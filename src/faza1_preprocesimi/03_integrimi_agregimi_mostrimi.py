"""Hapi 3 (Studenti B): integrimi, agregimi dhe mostrimi.

Hyrja:  data/processed/importet_pastruara.csv
Daljet: data/external/vendet.csv, data/external/kapitujt_hs.csv,
        data/processed/importet_integruara.csv, agregim_*.csv, mostra_*.csv
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils import EXTERNAL, lexo, ruaj  # noqa: E402

BE = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT",
      "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"}
CEFTA = {"AL", "BA", "MD", "ME", "MK", "XS"}  # + Kosova (vendi importues)
EVROPE_TJETER = {"CH", "NO", "IS", "LI", "GB", "UA", "BY", "RU", "TR", "AD", "MC", "SM", "VA",
                 "GI", "FO", "XC"}

# Seksionet e Nomenklaturës së Kombinuar sipas intervaleve të kapitujve
SEKSIONET_HS = [
    (1, 5, "I", "Kafshë të gjalla dhe produkte shtazore"),
    (6, 14, "II", "Produkte bimore"),
    (15, 15, "III", "Yndyrna dhe vajra"),
    (16, 24, "IV", "Ushqime të përpunuara, pije, duhan"),
    (25, 27, "V", "Produkte minerale dhe karburante"),
    (28, 38, "VI", "Produkte kimike"),
    (39, 40, "VII", "Plastikë dhe gomë"),
    (41, 43, "VIII", "Lëkurë"),
    (44, 46, "IX", "Dru"),
    (47, 49, "X", "Letër"),
    (50, 63, "XI", "Tekstile dhe veshje"),
    (64, 67, "XII", "Këpucë dhe kapele"),
    (68, 70, "XIII", "Gur, qeramikë, qelq"),
    (71, 71, "XIV", "Metale dhe gurë të çmuar"),
    (72, 83, "XV", "Metale bazë"),
    (84, 85, "XVI", "Makineri dhe pajisje elektrike"),
    (86, 89, "XVII", "Mjete transporti"),
    (90, 92, "XVIII", "Instrumente optike dhe mjekësore"),
    (93, 93, "XIX", "Armë dhe municion"),
    (94, 96, "XX", "Artikuj të ndryshëm"),
    (97, 99, "XXI", "Vepra arti"),
]


def nderto_tabelat_e_jashtme(df):
    """Krijon tabelat ndihmëse nëse nuk ekzistojnë. Studenti B plotëson kontinentet që mbeten 'TODO'."""
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    p_vendet = EXTERNAL / "vendet.csv"
    if not p_vendet.exists():
        v = df[["kodi_vendit", "emri_vendit"]].drop_duplicates().sort_values("kodi_vendit")
        v["nga_BE"] = v["kodi_vendit"].isin(BE).astype(int)
        v["nga_CEFTA"] = v["kodi_vendit"].isin(CEFTA).astype(int)
        evrope = v["kodi_vendit"].isin(BE | CEFTA | EVROPE_TJETER)
        v["kontinenti"] = evrope.map({True: "Evropë", False: "TODO"})
        v.loc[v["kodi_vendit"].isin(["XX", "XY"]), "kontinenti"] = "Jo-shtet"
        v.to_csv(p_vendet, index=False)
        print(f"  -> krijuar {p_vendet.name}; plotësoni kontinentet 'TODO'")

    p_hs = EXTERNAL / "kapitujt_hs.csv"
    if not p_hs.exists():
        rreshta = [{"kapitulli_hs": f"{k:02d}", "seksioni_hs": sek, "emri_seksionit": emri}
                   for a, b, sek, emri in SEKSIONET_HS for k in range(a, b + 1)]
        pd.DataFrame(rreshta).to_csv(p_hs, index=False)
        print(f"  -> krijuar {p_hs.name}")

    return (pd.read_csv(p_vendet, keep_default_na=False),
            pd.read_csv(p_hs, dtype={"kapitulli_hs": str}))


def main():
    df = lexo("importet_pastruara.csv")

    # --- Integrimi ---
    vendet, kapitujt = nderto_tabelat_e_jashtme(df)
    df["kapitulli_hs"] = df["kodi_hs10"].str[:2]
    n0 = len(df)
    df = df.merge(vendet.drop(columns="emri_vendit"), on="kodi_vendit", how="left")
    df = df.merge(kapitujt, on="kapitulli_hs", how="left")
    assert len(df) == n0, "merge nuk duhet të shtojë rreshta"
    ruaj(df, "importet_integruara.csv")

    # --- Agregimi ---
    shumat = {"vlera": "sum", "netweight": "sum", "taksa_doganes": "sum",
              "taksa_akcizes": "sum", "taksa_tvsh": "sum", "kodi_hs10": "nunique"}
    emrat = {"kodi_hs10": "nr_kodeve"}
    ruaj(df.groupby("muaji").agg(shumat).rename(columns=emrat).reset_index(), "agregim_muaji.csv")
    ruaj(df.groupby(["kodi_vendit", "kontinenti"]).agg(shumat).rename(columns=emrat)
         .sort_values("vlera", ascending=False).reset_index(), "agregim_vendi.csv")
    ruaj(df.groupby(["seksioni_hs", "emri_seksionit", "kapitulli_hs"]).agg(shumat).rename(columns=emrat)
         .reset_index(), "agregim_kapitulli_hs.csv")
    ruaj(df.pivot_table(index="kodi_vendit", columns="muaji", values="vlera", aggfunc="sum", fill_value=0)
         .reset_index(), "agregim_vendi_x_muaji.csv")

    # --- Mostrimi ---
    mostra = df.sample(frac=0.10, random_state=42)
    mostra_shtresuar = df.groupby("muaji").sample(frac=0.10, random_state=42)
    ruaj(mostra, "mostra_10.csv")
    ruaj(mostra_shtresuar, "mostra_10_shtresuar.csv")

    krahasimi = pd.DataFrame({
        "popullata": df[["vlera", "netweight", "taksa_tvsh"]].mean(),
        "mostra_rastit": mostra[["vlera", "netweight", "taksa_tvsh"]].mean(),
        "mostra_shtresuar": mostra_shtresuar[["vlera", "netweight", "taksa_tvsh"]].mean(),
    })
    print("Krahasimi i mesatareve:\n", krahasimi.round(1))


if __name__ == "__main__":
    main()
