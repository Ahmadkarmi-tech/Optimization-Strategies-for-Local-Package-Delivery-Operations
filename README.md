#  Package Delivery Optimization System

This project implements an intelligent system for optimizing local package delivery operations using Artificial Intelligence search algorithms. It focuses on minimizing total delivery distance while respecting vehicle capacity and package constraints.

---

##  Project Overview

The system simulates a delivery shop where:

**Each package has:**
-  Location `(x, y)`
-  Weight (kg)
-  Priority (1–5)

**Each vehicle has:**
-  Limited capacity (kg)

**The goal is to:**
Assign packages to vehicles and determine delivery routes that minimize total distance traveled.
Distance is calculated using the Euclidean formula.

---

##  Algorithms Implemented

The project provides two optimization techniques:

### 1. Genetic Algorithm (GA)
- Population-based optimization
- Uses:
  - Selection
  - Crossover
  - Mutation
- Evolves better delivery solutions over generations

### 2. Simulated Annealing (SA)
- Probabilistic optimization method
- Uses temperature-based search
- Accepts worse solutions early to escape local minima

---

##  Features

- Interactive GUI using Tkinter
- Choose between:
  - Genetic Algorithm
  - Simulated Annealing
- Custom input:
  - Number of vehicles
  - Vehicle capacities
  - Package details
- Displays:
  - Delivery routes
  - Distance per vehicle
  - Total distance

---

##  Problem Constraints

- Coordinates range: `0 ≤ x, y ≤ 100`
- Priority: `1 (highest) → 5 (lowest)`
- Vehicles must not exceed capacity
- Shop location: `(0, 0)`

---

##  Algorithm Parameters

### Simulated Annealing
| Parameter | Value |
|---|---|
| Initial Temperature | `1000` |
| Cooling Rate | `0.90 – 0.99` |
| Stopping Temperature | `1` |
| Iterations per temperature | `100` |

### Genetic Algorithm
| Parameter | Value |
|---|---|
| Population Size | `50 – 100` |
| Mutation Rate | `0.01 – 0.1` |
| Generations | `500` |

---

##  How to Run

1. Make sure Python is installed (3.x)
2. Run the script:

```bash
python main.py
```

3. Select algorithm from the GUI
4. Enter input data
5. Run optimization

---

##  Project Structure

```
├── main.py                  # Main application (GUI + algorithms)
└── README.md                # Project documentation
```

---

##  Output Example

- Vehicle assignments
- Ordered delivery route per vehicle
- Distance traveled per vehicle
- Final total distance

---

##  Objective

The main objective is to:
> Apply AI optimization techniques to solve a real-world logistics problem efficiently.

---

## References

### Project Files

* [ source code (main.py)](src/main.py)

##  Authors

 * **Ahmad karmi**
 * **Course:** Artificial Intelligence — ENCS3340
 * **Institution:** Birzeit University

---

##  License

This project is for educational purposes.
