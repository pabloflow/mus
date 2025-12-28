# MusEngine & CFR Agent 🃏

### Game Theory applied to the Spanish card game *Mus* using Counterfactual Regret Minimization

---

## 🔬 Abstract

This project serves as my **Bachelor's Thesis (TFG)** in Computer Engineering.

The goal is to develop a complete engine for the Spanish card game **Mus** and implement a **superhuman AI agent**.

Unlike Chess or Go (perfect-information games), Mus involves:
- Hidden information  
- Bluffing  
- Partner signaling  

To tackle this, I implement **Counterfactual Regret Minimization (CFR)** — the same algorithmic foundation used by **Libratus** and **Pluribus** to solve professional Poker.

---

## 🧩 The Challenge: Imperfect Information

Mus presents unique challenges for AI systems:

- **Hidden Information**: Players do not know opponents' cards  
- **Signaling**: Partners communicate via secret signals (*señas*)  
- **Bluffing**: Betting requires reasoning under uncertainty  

Traditional Minimax-based algorithms fail in this setting.  
This project explores **Nash Equilibrium approximations** in large, imperfect-information game trees.

---

## 🛠 Project Structure

Current modular architecture designed for scalability:

```bash
/mus-ai-engine
├── assets/          # Graphical resources (board, card sprites)
├── game/            # Core Game Logic (the "Brain")
│   ├── cards.py     # Card definitions and deck management
│   ├── engine.py    # State machine handling game phases (Descartes, Apuestas)
│   ├── evaluator.py # Hand strength evaluation (Grande, Chica, Pares, Juego)
│   └── players.py   # Player classes and action interfaces
├── ui/              # Visualization layer
│   └── window.py    # Pygame rendering loop
└── ai/              # (In Progress) CFR and Regret Matching implementation
```

## 🗺 Roadmap

- [x] Core Engine: Deck generation, hand distribution, basic rules
- [x] Hand Evaluator: Winner determination for "Grande", "Chica", "Pares", and "Juego"
- [x] UI Prototype: Basic visualization using Pygame
- [ ] Game Loop: Full 1v1 state machine implementation
- [ ] Abstraction: Simplifying the game tree to make it computationally solvable
- [ ] CFR Agent: Implementing the regret minimization algorithm
- [ ] 4-Player Integration: Scaling the model to team play

## 📦 Requirements

- Python 3.10+
- Pygame (for visualization)
- NumPy (for matrix operations in the AI)

## 🚀 Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/pabloflow/mus.git
   ```

2. Run the graphical interface (WIP):

   ```bash
   python main.py
   ```

---

*Bachelor's Thesis Project by Pablo Flores.*  
*Exploring the intersection of Game Theory and Software Engineering.*
