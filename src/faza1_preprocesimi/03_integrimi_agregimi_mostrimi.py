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