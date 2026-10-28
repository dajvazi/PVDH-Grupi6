""" Pastrimi dhe strategjia për vlerat e zbrazëta.

Dalja: data/processed/importet_pastruara.csv
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.utils import lexo_raw, ruaj  # noqa: E402

RIEMERTIMI = {
    "MUAJI": "muaji",
    "Sasia": "sasia",
    "Vlera Mallrave": "vlera",
    "Netweight": "netweight",
    "Taksa Doganës": "taksa_doganes",
    "Taksa Akcizës": "taksa_akcizes",
    "Taksa TVSH-së": "taksa_tvsh",
}


def main():
    df = lexo_raw()

    # Ndarja e kolonave të përbëra "KOD - EMRI"
    df[["kodi_vendit", "emri_vendit"]] = df["Origjina"].str.split(" - ", n=1, expand=True)
    df[["kodi_hs10", "pershkrimi"]] = df["Kodi Tarifor"].str.split(" - ", n=1, expand=True)

    # Pastrimi i tekstit
    for kol in ["kodi_vendit", "emri_vendit", "kodi_hs10", "pershkrimi"]:
        df[kol] = df[kol].str.strip()
    df["pershkrimi"] = df["pershkrimi"].str.replace("?", "'", regex=False)
    df["emri_vendit"] = df["emri_vendit"].str.title()

    # Kodet që nuk janë shtete (XX = prodhime vendore, XY = mallra të denacionalizuara)
    df["eshte_shtet"] = (~df["kodi_vendit"].isin(["XX", "XY"])).astype(int)

    # Rreshtat me vlerë 0 nuk kanë kuptim ekonomik për analizën
    print("Rreshta me vlerë 0 që fshihen:", int((df["Vlera Mallrave"] == 0).sum()))
    df = df[df["Vlera Mallrave"] > 0]

    # VITI dhe Regjimi janë konstante; Origjina dhe Kodi Tarifor u zëvendësuan
    df = df.drop(columns=["VITI", "Regjimi", "Origjina", "Kodi Tarifor"]).rename(columns=RIEMERTIMI)

    # --- Vlerat e zbrazëta ---
    # Sasia mungon kur malli nuk ka njësi plotësuese, pra NaN = "nuk aplikohet".
    df["ka_sasi"] = df["sasia"].notna().astype(int)
    print(f"Sasia NaN: {df['sasia'].isna().mean():.1%}")

    # Krahasimi i 3 strategjive (për raportin)
    mbushje_zero = df["sasia"].fillna(0)
    mediana_hs = df.groupby("kodi_hs10")["sasia"].transform("median")
    mbushje_mediana = df["sasia"].fillna(mediana_hs)
    print("Strategjia 1 (fshirje e kolonës): humbet info për", df["ka_sasi"].sum(), "rreshta")
    print("Strategjia 2 (mbushje me 0): mesatarja", round(mbushje_zero.mean(), 2))
    print("Strategjia 3 (mediana sipas HS): mbeten NaN", int(mbushje_mediana.isna().sum()),
          "sepse shumë kode HS nuk kanë asnjë sasi")
    # Vendimi: ruhet sasia origjinale + flamuri ka_sasi, pa imputim.

    kolonat = ["muaji", "kodi_vendit", "emri_vendit", "eshte_shtet", "kodi_hs10", "pershkrimi",
               "sasia", "ka_sasi", "vlera", "netweight", "taksa_doganes", "taksa_akcizes", "taksa_tvsh"]
    ruaj(df[kolonat], "importet_pastruara.csv")


if __name__ == "__main__":
    main()