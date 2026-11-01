# PVDH-Grupi6: Importet e Kosovës 2025

Projekt për lëndën **Përgatitja dhe vizualizimi i të dhënave** (PVDH), Fakulteti i Inxhinierisë Elektrike dhe Kompjuterike, Universiteti i Prishtinës, studimet master 2026/27.

Projekti analizon të gjitha importet e Kosovës për vitin 2025 (janar–dhjetor), sipas vendit të origjinës dhe kodit tarifor.

## Tema dhe domeni

- **Domeni:** Tregtia e jashtme / ekonomia (të dhëna doganore)
- **Tema:** Importet e Kosovës 2025, sipas vendit të origjinës, kodit tarifor HS dhe taksave të paguara (doganë, akcizë, TVSH)
- **Pyetjet kryesore:** Nga cilat vende dhe kontinente importon Kosova më shumë? Cilat grupe mallrash dominojnë? Si ndryshojnë importet dhe taksat sipas muajve? Sa ndikon marrëveshja me BE-në dhe CEFTA-n në taksën doganore?

## Anëtarët e grupit dhe kontributi

| Anëtari | GitHub | Kontributi në fazën 1 |
|---|---|---|
| Bleron Baftiu | [@bleronbaftiu21](https://github.com/bleronbaftiu21) | Hapi 01 (mbledhja, tipet, kualiteti), hapi 02 (pastrimi, vlerat e zbrazëta), `src/utils.py` |
| Edison Ndou | [@edisonndou](https://github.com/edisonndou) | Hapi 03 (integrimi, agregimi, mostrimi), hapi 04 (krijimi i vetive) |
| Donart Ajvazi | [@dajvazi](https://github.com/dajvazi) | Hapi 05 (diskretizimi, binarizimi), hapi 06 (transformimi, reduktimi, PCA), `main.py`, README |

## Dataseti

| | |
|---|---|
| **Burimi** | Dogana e Kosovës, Open Data |
| **Skedari** | `data/raw/Open_DATA_Import_Janar-Dhjetor_2025.xlsx` |
| **Përmasat** | 254,870 rreshta × 11 kolona |
| **Periudha** | Janar–Dhjetor 2025 |

| Kolona | Përshkrimi | Tipi |
|---|---|---|
| VITI | Viti (2025) | Interval, diskret |
| MUAJI | Muaji (1–12) | Interval, diskret |
| Regjimi | Regjimi doganor (IM4) | Nominal |
| Origjina | Vendi i origjinës, "KOD - EMRI" | Nominal |
| Kodi Tarifor | Kodi HS10 dhe përshkrimi i mallit | Nominal, hierarkik |
| Sasia | Sasia në njësi plotësuese | Ratio, kontinual |
| Vlera Mallrave | Vlera e mallit (€) | Ratio, kontinual |
| Netweight | Pesha neto (kg) | Ratio, kontinual |
| Taksa Doganës / Akcizës / TVSH-së | Taksat e paguara (€) | Ratio, kontinual |

## Struktura e projektit

```
PVDH-Grupi6/
├── data/
│   ├── raw/                  # të dhënat origjinale (nuk ndryshohen)
│   ├── external/             # tabela ndihmëse: vendet.csv, kapitujt_hs.csv
│   └── processed/            # daljet e fazës 1 (krijohen me main.py, nuk ruhen në Git)
├── notebooks/
├── src/
│   ├── utils.py              # funksione të përbashkëta (lexo, ruaj, rrugët)
│   └── faza1_preprocesimi/
│       ├── 01_mbledhja_tipet_kualiteti.py
│       ├── 02_pastrimi_vlerat_zbrazeta.py
│       ├── 03_integrimi_agregimi_mostrimi.py
│       ├── 04_krijimi_vetive.py
│       ├── 05_diskretizimi_binarizimi.py
│       ├── 06_transformimi_reduktimi.py
│       └── main.py           # ekzekuton hapat 01–06 me radhë
└── requirements.txt
```

## Instalimi dhe ekzekutimi

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt

python src/faza1_preprocesimi/main.py
```

Ekzekutimi zgjat disa minuta. Të gjitha daljet ruhen në `data/processed/`. Çdo skriptë mund të ekzekutohet edhe veçmas, me kusht që të jenë ekzekutuar hapat para saj.

> Nëse ndryshoni kontinentet ose listat BE/CEFTA te skripta 03, fshini `data/external/vendet.csv` që të krijohet përsëri.

## Faza 1: Para-procesimi

| Hapi | Kërkesa e detyrës | Çfarë bëhet |
|---|---|---|
| **01** | Mbledhja, tipet, kualiteti | Leximi, tipet statistikore (nominal/ordinal/interval/ratio, diskret/kontinual), raporti i kualitetit (NaN, zerot, negativet, duplikatet, encoding-u, konsistenca e TVSH-së) |
| **02** | Pastrimi, vlerat e zbrazëta | Ndarja e kolonave "KOD - EMRI", pastrimi i tekstit, heqja e 9 rreshtave me vlerë 0, krahasimi i 3 strategjive për `Sasia` (68.8% NaN), me vendim: flamuri `ka_sasi` pa imputim |
| **03** | Integrimi, agregimi, mostrimi | Bashkimi me tabelat e vendeve (kontinenti, BE, CEFTA) dhe të seksioneve HS. Redundanca me korrelacion, kovariancë dhe test χ². Agregimi sipas muajit, vendit dhe kapitullit HS. Mostra e rastit (me dhe pa zëvendësim) dhe e shtresuar |
| **04** | Krijimi i vetive | `cmimi_per_kg`, `taksa_totale`, `norma_doganore`, `norma_taksave`, `pjesa_e_tvsh`, `tremujori`, `kodi_hs4` |
| **05** | Diskretizimi, binarizimi | Bin-a me frekuencë të barabartë dhe me gjerësi të barabartë, intervale doganore, zbutja me mesataren e bin-it, flamuj binarë, one-hot për kontinentin dhe tremujorin |
| **06** | Transformimi, reduktimi, zgjedhja e vetive | Transformimi log, z-score, min-max dhe decimal scaling. Largimi i vetive me variancë të ulët dhe i atyre redundante (\|r\| > 0.9). PCA |

### Daljet kryesore (`data/processed/`)

| Skedari | Përdorimi |
|---|---|
| `importet_final.csv` | Dataseti i plotë i përpunuar (72 kolona), **hyrja për fazën 2** |
| `importet_per_vizualizim.csv` | 23 kolona dhe kolona `data` (UTF-8), **hyrja për fazën 3** (Power BI / Tableau) |
| `kualiteti_raport.csv` | Raporti i kualitetit për çdo kolonë |
| `agregim_*.csv` | Agregimet sipas muajit, vendit, kapitullit HS dhe vend × muaj |
| `mostra_10*.csv` | Mostrat 10% |
| `integrimi_korrelacioni.csv`, `korrelacioni.csv` | Matricat e korrelacionit |
| `vetite_e_zgjedhura.txt`, `pca_varianca.csv` | Rezultatet e zgjedhjes së vetive dhe të PCA |
| `histogramet_log.png` | Shpërndarja e vlerës para dhe pas transformimit log |

### Rezultatet kryesore

- **Kualiteti:** 0 duplikate. NaN vetëm te `Sasia` (68.8%). Norma mediane e TVSH-së është 18%, e njëjtë me normën ligjore, pra të dhënat janë konsistente.
- **Vlera totale e importeve:** 7.0 miliardë €, me 1.95 miliardë € taksa.
- **Partnerët kryesorë:** Gjermania (14.3%), Turqia (13.3%), Kina (13.1%).
- **Sipas kontinentit:** Evropa 71.9%, Azia 22.5%.
- **Redundanca:** Vlera–TVSH r = 0.83, Akciza–TVSH r = 0.89. Testi χ² (BE × taksë doganore) = 12,408.6, p ≈ 0.
- **Zgjedhja e vetive:** hiqen `eshte_shtet` (variancë 0.0002) dhe `log_taksa_totale` (redundante).
- **PCA:** 10 komponentë ruajnë ≥ 95% të variancës nga 15 veti.

### Shënime për fazën 2

- Outlier-at **nuk janë hequr** në fazën 1, sepse detektimi i tyre është detyrë e fazës 2. Kolonat `z_*` janë gati për metodën statistikore (\|z\| > 3).
- `norma_taksave` ka vlera ekstreme (maksimumi 26,829), te mallrat me vlerë të deklaruar shumë të vogël. Është kandidat për "zbulime jo të sakta".

## Krahasimi me datasete të ngjashme

| Dataseti | Burimi | Ngjashmëria | Dallimi nga dataseti ynë |
|---|---|---|---|
| [Global Commodity Trade Statistics](https://www.kaggle.com/datasets/unitednations/global-commodity-trade-statistics) | Kaggle (UN Comtrade) | Tregti sipas vendit, mallit (HS) dhe vitit, me vlerë, peshë dhe sasi | Agregim vjetor për shumë vende; nuk ka taksa as muaj |
| [India Trade Data](https://www.kaggle.com/datasets/lakshyaag/india-trade-data) | Kaggle | Importet/eksportet e një vendi sipas vendit partner dhe kapitullit HS | Vetëm vlera (në milionë $), pa peshë, sasi dhe taksa |
| [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail) | UCI | Transaksione me vend, sasi, çmim dhe datë; vlera të zbrazëta dhe negative për pastrim | Shitje me pakicë të një kompanie, jo të dhëna doganore |

Dataseti ynë është më i detajuar se këto: ka nivel mujor, kod HS me 10 shifra dhe tri lloje taksash, gjë që lejon veti të reja si `norma_doganore` dhe `norma_taksave`. Problemet e kualitetit janë të ngjashme: `Sasia` mungon te 68.8% e rreshtave dhe disa përshkrime kanë karaktere të prishura nga encoding-u.

## Fazat e projektit

- [x] **Faza 1:** Para-procesimi (15%)
- [ ] **Faza 2:** Detektimi i përjashtuesve, mënjanimi i zbulimeve jo të sakta, eksplorimi (10%)
- [ ] **Faza 3:** Vizualizimi statik, interaktiv dhe shumëdimensional (Power BI / Tableau) (5%)

