<div align="center">
  <p align="center">
    <img src="assets/logo.png" width="300" alt="App Logo">
</p>
  <h1>OctaNav</h1>
  <p><strong>Un motore di pathfinding avanzato per gridmap 8-connected, basato sull'esplorazione ricorsiva delle frontiere.</strong></p>

  <p>
    <a href="#"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version"></a>
    <a href="#"><img src="https://img.shields.io/badge/status-in%20development-orange.svg" alt="Status"></a>
    <a href="#"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
  </p>
</div>

---

## Informazioni sul Progetto

**OctaNav** è un sistema sperimentale di *pathfinding* ottimizzato per spazi bidimensionali (griglie) dotati di ostacoli. A differenza dei classici algoritmi basati sulla scansione nodo-per-nodo (come A* o Dijkstra in versione base), OctaNav sfrutta concetti geometrici avanzati: calcola i *cammini liberi*, determina il *contesto* e il *complemento* di un'origine, ed esplora lo spazio ricorsivamente saltando attraverso *landmark* situati sulle frontiere visibili.

Il sistema gestisce movimenti cardinali (costo $1$) e diagonali (costo $\sqrt{2}$) ed è equipaggiato con un generatore procedurale di ostacoli per il benchmarking.

---

## Core Features & Roadmap

- [ ] **Generatore di Ambienti**
  - [ ] Creazione procedurale di ostacoli casuali (con densità e dimensioni configurabili).
- [ ] **Motore Geometrico**
  - [ ] Calcolo della *Distanza Libera* ($d_{lib}$) in tempo $O(1)$ noto il delta coordinate.
  - [ ] Estrazione dei cammini di Tipo 1 (*Contesto*).
  - [ ] Estrazione dei cammini di Tipo 2 (*Complemento*).
- [ ] **Risolutore CAMMINOMIN (Pathfinder)**
  - [ ] Identificazione dinamica delle *Frontiere*.
  - [ ] Esplorazione ricorsiva basata su sequenze di landmark.
  - [ ] Implementazione euristiche di pruning (riduzione dello spazio di ricerca).
- [ ] **Benchmarking Suite**
  - [ ] Analisi automatizzata.
  - [ ] Estrazione metriche (N° frontiere esplorate, tempi di calcolo, hit rate del pruning).

---

## Architettura del Sistema

L'architettura segue lo standard `src-layout` per garantire la massima modularità e isolare la logica di business.

```text
octanav/
├── .vscode/                # Impostazione dell'ambiente
├── docs/                   # Documentazione
├── src/                    # Core library
│   ├── ...                 # Moduli
│   └── main.py             # CLI e Batch Runner
├── tests/                  # Unit tests (pytest) per garantire la solidità del core
├── data/                   # Dataset di input e dump dei risultati
├── requirements.txt        # Dipendenze (es. numpy, pytest)
├── env.example             # Esempio di file env da configurare nel progetto
└── README.md               # Questa pagina
```

---

## Dettagli Tecnici

*(Questa sezione è pensata per tracciare le scelte ingegneristiche)*

- **Rappresentazione della Griglia**
- **Ottimizzazione Ricerca**
- **Pruning (Euristiche)**

---

## Guida all'Installazione

L'applicativo è progettato per funzionare in modalità batch/CLI, senza interfacce grafiche pesanti, garantendo la massima velocità durante le misurazioni di performance.

### Setup Rapido
```bash
# Clona la repository
git clone [https://github.com/](https://github.com/)[TUO-NOME]/OctaNav.git
cd OctaNav

# Inizializza l'ambiente virtuale
python -m venv .venv
# Attivazione (Windows): .venv\Scripts\activate
# Attivazione (Unix): source .venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt
```

### Esecuzione
```bash
# [Da completare: Inserire qui i comandi di avvio]
# Esempio:
# python src/main.py run --grid-size 100x100 --density 0.3 --output data/results.json
```

---

## Maintainers

- **Marco Lizza**

<div align="center">
  <p><br><em>Distribuito sotto licenza MIT. Per scopi accademici e di ricerca. Vedi il file `LICENSE` per maggiori dettagli.</em></p>
</div>