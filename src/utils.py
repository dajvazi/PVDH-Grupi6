"""Funksione të përbashkëta për të gjitha skriptet e projektit."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Open_DATA_Import_Janar-Dhjetor_2025.xlsx"
EXTERNAL = ROOT / "data" / "external"
PROCESSED = ROOT / "data" / "processed"

KOLONAT_NUMERIKE = [
    "sasia", "vlera", "netweight",
    "taksa_doganes", "taksa_akcizes", "taksa_tvsh",
]


def lexo_raw() -> pd.DataFrame:
    """Lexon Excel-in origjinal. Kodi Tarifor lexohet si tekst që të ruhen zerot në fillim."""
    return pd.read_excel(RAW, dtype={"Kodi Tarifor": str})


def lexo(emri: str) -> pd.DataFrame:
    return pd.read_csv(PROCESSED / emri, dtype={"kodi_hs10": str, "kodi_hs4": str, "kapitulli_hs": str})


def ruaj(df: pd.DataFrame, emri: str) -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / emri, index=False)
    print(f"  -> ruajtur {emri}: {df.shape[0]:,} rreshta x {df.shape[1]} kolona")