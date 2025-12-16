# AI and Games Projects - Robotics & Strategy

Two academic projects implementing AI strategies for autonomous robots and strategic board games.

## Repository Overview

This repository contains two distinct projects developed for the AI and Games course (LU3IN025) at Sorbonne University:

1. **Paint Wars** - Multi-agent robotics competition
2. **Quoridor** - Strategic board game with pathfinding

---

## Project 1: Paint Wars

### Description

A competitive multi-agent robotics simulation where two teams of 8 robots (red team vs blue team) compete to control an arena divided into cells. A cell belongs to the team that visited it last. The team controlling the most cells after 2000 iterations wins.

This is a competitive variation of the classic **multi-agent patrolling problem** in robotics.

### Game Mechanics

- **Teams**: 8 robots per team (red vs blue)
- **Objective**: Control the maximum number of cells
- **Time limit**: 2000 iterations
- **Arena**: 5 different maze configurations
- **Victory**: Team with most cells at time limit

### Key Features

#### Behavioral Architecture
- **Braitenberg-style behaviors**: Reactive control based on sensor inputs
- **Genetic algorithm optimized behaviors**: Evolved controllers from TP2
- **Subsumption architecture**: Layered behavioral control system
- **Multiple behavior modules**:
  - Random exploration (`subsomption_alea.py`)
  - Wall following (`subsomption_suivre_mur.py`)
  - Patrol patterns (`subsomption_patrouille.py`)
  - Enemy avoidance (`subsomption_ennemy.py`)
  - Combined strategies (`subsomption_combine.py`)

#### Sensor-Based Control
- **Translation speed**: Forward/backward movement
- **Rotation speed**: Left/right turning
- **Sensor inputs**: Distance sensors, team detection, position data
- **No memory, no communication**: Pure reactive behaviors

#### Tournament System
- **Arena selector**: 5 different maze configurations
- **Starting position inversion**: Ensures fairness
- **Automated tournaments**: `go_tournament` script for batch testing
- **Performance tracking**: CSV data generation and plotting tools

### Technical Implementation

#### Main Files
- `paintwars.py`: Main simulator loop
- `paintwars_team_challenger.py`: Your team implementation
- `paintwars_team_champion.py`: Default opponent (reference implementation)
- `paintwars_config.py`: Configuration (arena, teams, speed)
- `paintwars_arena.py`: Arena definitions

#### Behavioral Modules
- `comportement.py`: Core behavior definitions
- `subsomption_*.py`: Individual behavior layers
- `optimisation.py`: Genetic algorithm optimization

#### Analysis Tools
- `multiplotCSV/`: Performance visualization toolkit
- CSV data export for statistical analysis

### Usage

```bash
# Run with default config
python paintwars.py

# Run with specific parameters
python paintwars.py <arena_num> <invert_positions> <speed>
# Example: Arena 3, inverted positions, fast mode
python paintwars.py 3 True 1

# Run full tournament
./go_tournament
```

**Speed modes**:
- `0`: Normal speed (with display)
- `1`: Fast mode
- `2`: Very fast (no display)

### Strategy Requirements

Teams must implement in `paintwars_team_challenger.py`:

```python
def get_team_name():
    return "Your Team Name"

def step(robotId, sensors):
    # Input: robot ID and sensor data
    # Output: (translation_speed, rotation_speed)
    return translation, rotation
```

**Constraints**:
- All logic must be in the `step()` function
- No memory between steps
- No inter-robot communication
- Only sensor data available

---

## Project 2: Quoridor

### Description

A strategic board game implementation inspired by Quoridor. Players race to cross the board while strategically placing walls to block opponents. First player to reach the opposite side wins.

### Game Rules

#### Movement
- Move one cell per turn (up, down, left, right - no diagonals)
- Players do not block each other (can occupy same cell)

#### Wall Placement
- Walls consist of 2 cells (horizontal or vertical)
- Walls placed directly on cells (not between them)
- Cannot place walls on starting rows
- **Critical rule**: Cannot place walls that completely block any player's path to their goal

#### Victory Condition
- First player to reach any cell on the opponent's starting row wins

### Key Features

#### Pathfinding with A*
- Shortest path calculation to goal line
- Heuristic-based search from `search` module
- Dynamic replanning when walls are placed

#### Strategy Implementation
Multiple AI strategies implemented:

1. **Random Strategy** (Week 1)
   - Random choice between moving and placing walls
   - Legal wall placement verification
   - Shortest path to random goal cell

2. **Minimax Strategy** (Weeks 2-3)
   - Game tree search with evaluation function
   - Alpha-beta pruning for efficiency
   - Depth-limited search

3. **Monte Carlo Tree Search (MCTS)** (Weeks 2-3)
   - Statistical sampling of game outcomes
   - UCB1 selection policy
   - Simulation rollouts

4. **Heuristic-Based Strategy** (Weeks 2-3)
   - Blocking opponent paths
   - Maintaining own path options
   - Phase-specific tactics (opening, midgame, endgame)

#### Game Phases
- **Opening**: Focus on wall placement strategy
- **Midgame**: Balance between blocking and advancing
- **Endgame**: Race to goal when path is clear

### Technical Implementation

#### Modules

**pySpriteWorld** (Graphics Engine)
- Sprite-based rendering with Pygame
- Map editor support (Tiled .json format)
- Layer system: `joueur` (players), `ramassable` (walls)
- Provided maps: `quoridorMap` (standard), miniature map (testing)

**search** (Pathfinding)
- A* algorithm implementation
- Grid-based problem formulation
- Heuristic functions for optimization

#### Core Files
- `src/main.py`: Game loop and main logic
- `src/pySpriteWorld/`: Graphics and sprite management
- `src/search/`: Pathfinding algorithms
  - `grid2D.py`: 2D grid representation
  - `probleme.py`: Problem definitions for search

### Usage

```bash
cd projet-quoridor-gr1_tahir_aired-main/src
python main.py
```

### Map Customization

Edit maps with [Tiled Map Editor](https://www.mapeditor.org/):
1. Create/edit `.json` map files
2. Configure player count and wall count
3. Update map name in `main.py` init function

---

## Technical Stack

### Paint Wars
- **Simulator**: Roborobo4
- **Language**: Python 3.9
- **Libraries**: NumPy, Matplotlib, CSV processing
- **Platform**: Linux, macOS, Windows (via VirtualBox)

### Quoridor
- **Graphics**: Pygame via pySpriteWorld
- **Pathfinding**: Custom search module (A*)
- **Map Editor**: Tiled (optional)
- **Language**: Python 3.x

## Installation

### Paint Wars

```bash
# Install Roborobo4 simulator
git clone https://github.com/nekonaute/roborobo4/
cd roborobo4
# Follow installation instructions in README

# Create conda environment
conda create -n roborobo python=3.9
conda activate roborobo

# Install dependencies
pip install numpy matplotlib pandas
```

### Quoridor

```bash
# Install Pygame
pip install pygame

# Install dependencies
pip install numpy
```

## Academic Context

**Course**: LU3IN025 - AI and Games (Autonomous Robotics)

**Institution**: Sorbonne University, L3 Computer Science

**Topics Covered**:
- Reactive behaviors (Braitenberg vehicles)
- Subsumption architecture
- Genetic algorithms for behavior optimization
- Multi-agent coordination
- Pathfinding algorithms (A*)
- Game tree search (Minimax, MCTS)
- Strategic planning and decision-making

## Evaluation

### Paint Wars
- 15-minute live demonstration
- Tournament against champion team on known + unknown arenas
- Code explanation and Q&A
- Inter-group tournament

### Quoridor
- Strategy comparison (4 weeks)
- Multiple AI implementations
- Performance analysis report (Markdown)
- Oral presentation and defense

## Credits

**Developers**: Aans TAHIR, AIRED Matthias

**Course Instructors**: Sorbonne University AI and Games faculty

**Frameworks**:
- Roborobo4 by Nicolas Bredeche
- pySpriteWorld by Yann Chevaleyre

## License

Academic Project - Sorbonne University 2023-2024
