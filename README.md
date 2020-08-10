# A different SuperMario
same old story, Mario looking for mushrooms, but this time on a 2d table searching based on LRTA* algorithm!

## LRTA* algorithm
This algorithm is like the hill-climbing algorithm with the advantage of memory.
For each state we assign a value(H(s)) that best estimates the cost of the path that leads to goal.
This value is first initiated by the heuristic of that state and then is enhanced during the algorithm.
In other words, the agent updates this value for its previous state as it moves to another state.
Eventually it chooses the best action based on estimated costs for the next step.

## simple GUI
this GUI was implemented for a better sense of mario's situation(mario is the blue square)


<img src="https://github.com/pariyamd/A-different-SuperMario/blob/master/board.png" alt="drawing" width="300"/>
<img src="https://github.com/pariyamd/A-different-SuperMario/blob/master/finished_display.png" alt="drawing" width="300"/>
