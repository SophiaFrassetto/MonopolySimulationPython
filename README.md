# MonopolySimulationPython
A simple simulation of a board game better known as Monopoly.

## How to Execute
```
python simulation.py
```
- ### args:
    - ```--simulations``` : Total simulations. default: 300
  
    - ```--reward ```: Reward for player passed in first board position. default: 100
  
    - ```--money``` : Initial money. default: 300
  
    - ```--max_rounds``` : Max rounds. default: 1000
  
    - ```--max_workers``` : Max workers for threads. default: 8

## Example return

```
    Total simulations: 300
    Total rounds finish with Time Out: 229
    Average of rounds: 770
    impulsive win: 82 / 27.33% | lose: 218 / 72.67%
    demanding win: 73 / 24.33% | lose: 227 / 75.67%
    cautious win: 72 / 24.0% | lose: 228 / 76.0%
    aleatory win: 73 / 24.33% | lose: 227 / 75.67%
    impulsive most win with 82 / 27.33%
```
