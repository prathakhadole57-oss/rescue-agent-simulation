# 🚑 Rescue Agent Simulation

A Python-based grid world simulation that compares three different AI agent strategies for rescuing patients in an urban environment with obstacles (cars). The agents navigate a 5x5 grid, avoid obstacles, and attempt to rescue all four patients within 50 steps.

## 🎯 Features

- **Three intelligent agent types**:
  - 🤖 **Simple Reflex Agent** – Random movement, no memory
  - 🧠 **Model‑Based Reflex Agent** – Remembers visited cells to avoid re‑exploration
  - 🎯 **Goal‑Based Agent** – Uses Manhattan distance to find and move toward the nearest patient

- **Dynamic environment** – Patients and obstacles are randomly placed at the start
- **Interactive menu** – Choose which agent to run (each runs once)
- **Visual simulation** – Real‑time grid animation with stats panel
- **Completion page** – Confirmation after all agents have finished
- **Performance dashboard** – Final comparison of steps, rescued patients, and efficiency

## 📦 Requirements

- Python 3.7+
- `matplotlib` (for graphics and dashboard)

Install dependencies:

```bash
pip install matplotlib
