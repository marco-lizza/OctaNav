<div align="center">
  <p align="center">
    <img src="assets/logo.png" width="300" alt="App Logo">
</p>
  <h1>OctaNav</h1>
  <p><strong>An advanced pathfinding engine for 8-connected grid maps, based on recursive frontier exploration.</strong></p>

  <p>
    <a href="#"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version"></a>
    <a href="#"><img src="https://img.shields.io/badge/status-in%20development-orange.svg" alt="Status"></a>
    <a href="#"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
  </p>
</div>

---

## About the Project

**OctaNav** is an experimental pathfinding system optimized for two-dimensional spaces (grids) equipped with obstacles. Unlike classic algorithms based on node-by-node scanning (like basic A* or Dijkstra), OctaNav leverages advanced geometric concepts: it calculates *free paths*, determines the *context* and *complement* of an origin, and explores the space recursively by jumping through *landmarks* located on visible frontiers.

The system handles cardinal movements (cost $1$) and diagonal movements (cost $\sqrt{2}$) and comes equipped with a procedural obstacle generator for benchmarking.

---

## Core Features & Roadmap

- [&#10004;] **Environment Generator**
  - [&#10004;] Procedural creation of random obstacles (with configurable density and dimensions).
- [ ] **Geometric Engine**
  - [ ] Calculation of *Free Distance* ($d_{lib}$) in $O(1)$ time, given the coordinate delta.
  - [ ] Extraction of Type 1 paths (*Context*).
  - [ ] Extraction of Type 2 paths (*Complement*).
- [ ] **SHORTESTPATH Solver (Pathfinder)**
  - [ ] Dynamic identification of *Frontiers*.
  - [ ] Recursive exploration based on landmark sequences.
  - [ ] Implementation of pruning heuristics (search space reduction).
- [ ] **Benchmarking Suite**
  - [ ] Automated analysis.
  - [ ] Metrics extraction (No. of frontiers explored, computation times, pruning hit rate).

---

## System Architecture

The architecture follows the `src-layout` standard to ensure maximum modularity and isolate business logic.

    octanav/
    ├── .vscode/                # Environment setup
    ├── docs/                   # Documentation
    ├── src/                    # Core library
    │   ├── ...                 # Modules
    │   └── main.py             # CLI and Batch Runner
    ├── tests/                  # Unit tests (pytest) to ensure core robustness
    ├── data/                   # Input datasets and result dumps
    ├── requirements.txt        # Dependencies (e.g., numpy, pytest)
    ├── env.example             # Example env file to configure in the project
    └── README.md               # This page

---

## Technical Details

*(This section is intended to track engineering decisions)*

- **Grid Representation and Obstacle Generation**
  - **High Cohesion (Information Expert):** The `Grid` class holds exclusive responsibility for managing spatial data and boundary validation (via the `is_valid_coordinate()` method). This approach centralizes safety and prevents exceptions (`IndexError`), allowing generation algorithms (which operate on the grid) to ignore bounds checking and focus solely on placement logic.
  - **Open/Closed Architecture (Strategy Pattern):** The obstacle generation logic is decoupled from the map structure via the `ObstacleStrategy` interface. This ensures high extensibility: adding new obstacle formations does not require any changes to the core grid code.
  - **Algorithmic Optimizations and Data Structures:**
    - **Directional Mapping with Hash Tables:** The calculation of expansion directions (for both orthogonal and diagonal moves) has been implemented using dictionaries (e.g., `directions = {0: (0, -1), ...}`). This choice replaces long chains of conditional statements (`if-elif`), guaranteeing constant $O(1)$ access times and significantly improving code readability and maintainability.
    - **Local Collision Detection (Sets):** In Random Walk-based obstacles (e.g., `AgglomerateObstacle`), a `set` is used to keep track of locally occupied coordinates. By leveraging Python's hash table-based implementation of sets, the existence check (`if next_cell not in cells_selected`) occurs in average $O(1)$ time. This optimization prevents redundant overwriting of cells, avoiding stalls or unnecessary calculations during obstacle growth.
- **Search Optimization**
- **Pruning (Heuristics)**

---

## Installation Guide

The application is designed to run in batch/CLI mode, without heavy graphical interfaces, ensuring maximum speed during performance measurements.

### Quick Setup

    # Clone the repository
    git clone https://github.com/[YOUR-NAME]/OctaNav.git
    cd OctaNav
    
    # Initialize the virtual environment
    python -m venv .venv
    # Activation (Windows): .venv\Scripts\activate
    # Activation (Unix): source .venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt


### Execution

    # [To do: Insert startup commands here]
    # Example:
    # python src/main.py run --grid-size 100x100 --density 0.3 --output data/results.json


---

## Maintainers

- **Marco Lizza**

<div align="center">
  <p><br><em>Distributed under the MIT License. For academic and research purposes. See the `LICENSE` file for more details.</em></p>
</div>