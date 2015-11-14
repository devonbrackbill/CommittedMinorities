#CommittedMinorities 

Simulator for committed minorities in the Naming Game.

Answers the question:
"What fraction of a population needs to be committed to sway a majority to adopt a new, minority convention?"

Answer: ~10%

The Naming Game is a model of convention formation from [Baronchelli et al](http://iopscience.iop.org/1742-5468/2006/06/P06014 "Naming Game"). It has been used to study the effect of network structure on convention formation. Some important findings are [here](https://sites.google.com/site/andreabaronchelli/naming_game).

The simulations here are based on research from [Xie et al.](http://journals.aps.org/pre/abstract/10.1103/PhysRevE.84.011130)

#To Run
To execute these simulations, place the .py files in a common directory. Then, from the command line:

````
python StandardNameGame.py <population size> <number of simulations> <file number> <output path>
````

Outputs a csv file that shows the results.