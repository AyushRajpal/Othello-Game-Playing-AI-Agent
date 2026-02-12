\# Othello (Reversi) AI Agent — Minimax + Alpha–Beta



An AI agent for \*\*Othello/Reversi\*\* that selects moves using \*\*minimax search with alpha–beta pruning\*\* and a heuristic evaluation function.



\*\*Performance:\*\* ~\*\*85% win rate\*\* in internal testing over \*\*100+ games\*\* (results depend on opponent strength, rules, and time settings).



---



\## Highlights

\- \*\*Minimax + Alpha–Beta pruning\*\* for efficient game-tree search

\- \*\*Time-aware depth selection\*\* (search depth adapts based on remaining time)

\- Heuristic combines:

&nbsp; - disc difference \*(my discs − opponent discs)\*

&nbsp; - edge stability scoring



---



\## Input / Output (File-Based)



This agent reads from `input.txt` and writes the chosen move to `output.txt`.



\### `input.txt` format

1\. Line 1: player symbol (`X` or `O`)

2\. Line 2: two numbers: `<your\_time> <opponent\_time>`

3\. Next 12 lines: the \*\*12×12 board\*\* using:

&nbsp;  - `X` for X discs

&nbsp;  - `O` for O discs

&nbsp;  - `.` for empty cells



\### `output.txt`

One move coordinate like `a1`, `b7`, etc.



Columns: `a`..`l`  

Rows: `1`..`12`



---



\## How to Run

```bash

python othello\_agent.py



