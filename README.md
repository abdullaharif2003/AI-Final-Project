# 🧠 AI Solver for 2048

An intelligent agent designed to solve the popular puzzle game **2048** using heuristic-based algorithms and AI search strategies.

---

## 📌 Overview

This project explores the use of heuristic algorithms and AI techniques to build an **automated 2048 game solver**. The primary goal is to evaluate the effectiveness of different heuristics and decision-making strategies in achieving high tile scores in the game.

---

## 🛠️ Implementation Details

The solver is developed in **Python**, using:

* `NumPy` for array operations
* A custom-built `Grid` class to manage the game state
* Heuristic scoring combined with AI algorithms to select the optimal move at each step

---

### ⚙️ Operational Logic

1. **Grid Initialization**
   A 4x4 game grid is initialized (default size), mimicking the classic 2048 board.

2. **Move Prediction**
   The `next_move_predictor()` function evaluates all possible moves — **up**, **down**, **left**, **right** — by simulating them on a copy of the grid and scoring each resulting state.

3. **Heuristic Scoring System**
   The scoring function evaluates each move using:

   * **Snake Pattern Heuristic**: Encourages high-value tiles to remain in a snake-like order.
   * **Adjacent Tile Matching**: Rewards merging possibilities by identifying similar adjacent tiles.
   * **Empty Tile Bonus**: Prioritizes moves that keep the grid spacious for future combinations.

4. **Expectimax Algorithm (Optional Extension)**
   The design supports the integration of the **Expectimax** search algorithm for deeper move simulation, incorporating both deterministic tile merges and probabilistic tile spawns.

---

## 🧪 Heuristics in Action

| Heuristic Name      | Description                                                               |
| ------------------- | ------------------------------------------------------------------------- |
| Snake Pattern Score | Rewards strategic placement of high tiles in a continuous snake-like flow |
| Adjacent Tile Score | Encourages clustering of mergeable tiles to maximize future combinations  |
| Empty Tile Bonus    | Prioritizes game states with more free spaces to avoid early game over    |

---

## 📊 Results

The solver was tested across multiple games, showing a **significant improvement** in performance compared to random or greedy move strategies.


## ✅ Conclusion

This project successfully demonstrates how **heuristic-based AI** can be effectively applied to solve puzzle games like 2048. Its modular structure allows future extensions such as:

* Deeper search algorithms (Expectimax, Minimax)
* Reinforcement Learning
* Neural Network integration

> 🔄 Whether you're just experimenting or aiming to beat your high score, this solver is a powerful AI toolkit for mastering 2048!
