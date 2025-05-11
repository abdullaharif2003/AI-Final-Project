AI-Final-Project
This repository contains the final project for our Artificial Intelligence course, including the proposal, video demonstration, source code, and final report.

AI Solver for 2048
Introduction
This project implements an AI-based solver for the popular puzzle game 2048 using the Expectimax algorithm combined with carefully designed heuristics. The solver is designed to play the game intelligently by evaluating possible future states and selecting optimal moves.

Implementation Details
The project is written in Python and relies on the numpy library for numerical operations. The AI is encapsulated in a Solver class which interacts with a custom Grid class to simulate the game environment.

Core Components
Expectimax Algorithm: Simulates possible moves by both the player and the game environment (tile spawns) to predict the most rewarding paths.

Heuristics: Multiple scoring heuristics are used to evaluate the quality of a game state:

Snake pattern alignment

Tile adjacency

Number of empty tiles

Maximum tile value

Monotonicity of rows and columns

Move Prediction Logic
Move Simulation: For each possible direction (w, s, a, d), a move is simulated.

Grid Evaluation: The resulting grid is scored using a depth-1 Expectimax evaluation.

Fallback Strategy: If no legal move improves the state, a simpler heuristic score is used to choose the best fallback move.

Heuristic Breakdown
Snake Pattern Heuristic: Encourages placing larger tiles in a snake-like pattern (top-left to bottom-right or transposed).

Adjacent Matching Heuristic: Rewards states with more identical adjacent tiles, increasing merge opportunities.

Empty Tile Count: Prefers game states with more empty cells to allow flexibility.

Max Tile Heuristic: Encourages states with higher tile values.

Monotonicity Bonus: Adds bonus scores for rows and columns that are consistently increasing or decreasing.

Features
Uses depth-limited Expectimax to balance computational efficiency with strategic foresight.

Highly modular design allowing further enhancement with deeper search or different evaluation strategies.

Integration with a graphical Grid interface (pygame display).

Falls back to simpler heuristics when Expectimax doesn't yield a viable move.

Usage
To run the solver, simply execute the main Python script (typically after initializing the grid):

python game.py
Ensure all dependencies are installed, including numpy and pygame.

Conclusion
This AI solver effectively demonstrates how combining probabilistic planning (Expectimax) with domain-specific heuristics can solve complex games like 2048. The modular design allows future integration with deeper search, learning-based approaches, or advanced optimizations.
