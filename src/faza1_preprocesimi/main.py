"""Ekzekuton hapat e fazës 1 me radhë: python src/faza1_preprocesimi/main.py"""
import runpy
from pathlib import Path

HAPAT = [
    "01_mbledhja_tipet_kualiteti.py",
    "02_pastrimi_vlerat_zbrazeta.py",
    '03_integrimi_agregimi_mostrimi.py',
    '04_krijimi_vetive.py',
    '05_diskretizimi_binarizimi.py',
    '06_transformimi_reduktimi.py',
]

if __name__ == "__main__":
    dosja = Path(__file__).resolve().parent
    for hapi in HAPAT:
        print(f"\n===== {hapi} =====")
        runpy.run_path(str(dosja / hapi), run_name="__main__")