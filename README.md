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
- [&#10004;] **Geometric Engine**
  - [&#10004;] Calculation of *Free Distance* ($d_{lib}$) in $O(1)$ time, given the coordinate delta.
  - [&#10004;] Extraction of Type 1 paths (*Context*).
  - [&#10004;] Extraction of Type 2 paths (*Complement*).
- [&#10004;] **SHORTESTPATH Solver (Pathfinder)**
  - [&#10004;] Dynamic identification of *Frontiers*.
  - [&#10004;] Recursive exploration based on landmark sequences.
- [ ] **Benchmarking Suite**
  - [ ] Automated analysis.
  - [ ] Metrics extraction (No. of frontiers explored, computation times, pruning hit rate).

---

## System Architecture

The architecture follows the `src-layout` standard to ensure maximum modularity and isolate business logic. Click on the individual modules for detailed technical documentation.

- `octanav/`
    - `docs/` - Global documentation
    - `src/` - Core library
        - [`map_generator/`](src/map_generator/README.md) - Grid model and procedural obstacles
        - [`navigator/`](src/navigator/README.md) - Geometric engine, dlib, Context & Complement
        - [`map_visualizer/`](src/map_visualizer/README.md) - UI layer (CLI and PyQt6)
        - `main.py` - CLI and Batch Runner
    - `tests/` - Support the testing and the analysis of the app
    - `data/` - Input datasets and result dumps
    - `requirements.txt` - Dependencies
    - `README.md` - This page
    
---

## Technical Details

*(This section is intended to track engineering decisions)*

- **Grid Representation and Obstacle Generation**
  - **High Cohesion (Information Expert):** The `Grid` class holds exclusive responsibility for managing spatial data and boundary validation (via the `is_valid_coordinate()` method). This approach centralizes safety and prevents exceptions (`IndexError`), allowing generation algorithms (which operate on the grid) to ignore bounds checking and focus solely on placement logic.
  - **Open/Closed Architecture (Strategy Pattern):** The obstacle generation logic is decoupled from the map structure via the `ObstacleStrategy` interface. This ensures high extensibility: adding new obstacle formations does not require any changes to the core grid code.
  - **Information Hiding (Law of Demeter):** Grid internal structures (like the 2D matrix) are strictly encapsulated. External modules (UI Visualizer, Pathfinders) query cell states exclusively via `Grid.is_traversable(x, y)`, ensuring loose coupling and allowing future refactoring of the grid's underlying data structure without breaking other modules.
  - **Algorithmic Optimizations and Data Structures:**
    - **Directional Mapping with Hash Tables:** The calculation of expansion directions (for both orthogonal and diagonal moves) has been implemented using dictionaries (e.g., `directions = {0: (0, -1), ...}`). This choice replaces long chains of conditional statements (`if-elif`), guaranteeing constant $O(1)$ access times and significantly improving code readability and maintainability.
    - **Local Collision Detection (Sets):** In Random Walk-based obstacles (e.g., `AgglomerateObstacle`), a `set` is used to keep track of locally occupied coordinates. By leveraging Python's hash table-based implementation of sets, the existence check (`if next_cell not in cells_selected`) occurs in average $O(1)$ time. This optimization prevents redundant overwriting of cells, avoiding stalls or unnecessary calculations during obstacle growth.

- **Pathfinding Engine & Geometric Analysis**
  - **Strategy and Facade Patterns:** Path calculation rules (Type 1 and Type 2 paths) are modularized using the `IPathStrategy` interface, adhering to the Open-Closed principle and preventing "God Object" anti-patterns. The `Navigator` class acts as a Facade, providing a unified, high-level API to orchestrate the underlying engines and grid analyzers.
  - **Immutable Value Objects:** The `Coordinate` model is implemented as a frozen dataclass (`@dataclass(frozen=True)`). Making spatial coordinates strictly immutable and hashable allows them to be used efficiently as dictionary keys and inserted into mathematical `set` collections (used for *Context* and *Complement* areas).

- **Search Optimization**
  - **Memoization (Dynamic Programming):** The `PathEngine` implements a caching mechanism (`dict[(Origin, Destination), FreePathResult]`) to store previously evaluated paths and distances. This is critical during the *Context* and *Complement* analysis phase (which requires scanning the entire map): redundant path evaluations are bypassed via $O(1)$ cache hits, drastically reducing the computational overhead.


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