# PVDH-Grupi6

## Struktura

```
data/raw/         # te dhenat origjinale
data/processed/   # te dhenat e pastruara
notebooks/        # Jupyter notebooks
src/              # kodi Python
```

## Konfigurimi (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nese PowerShell e bllokon aktivizimin:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Ekzekutimi

```powershell
python src/main.py
jupyter notebook
```
