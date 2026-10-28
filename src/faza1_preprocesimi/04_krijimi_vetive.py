"""Hapi 4 (Studenti B): krijimi i vetive të reja.

Hyrja:  data/processed/importet_integruara.csv
Dalja:  data/processed/importet_me_veti.csv
"""
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.utils import lexo, ruaj  # noqa: E402