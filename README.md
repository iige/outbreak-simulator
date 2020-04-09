# Outbreak / Social Distancing Simulator

A Monte Carlo simulation of the effects of Social Distancing during an Outbreak.

## Getting Started

### Install required packages
```
pip install -r requirements.txt
```

### Configure Your Parameters
Configure experiment parameters in [simulator.py](./simulator.py)

* **N**: Grid Size (N x N) 
* **M**: Initial Population Size
* **X**: % Of initial population that is infected
* **S**: % Of initial population that is stationary
* **Pm**: Mobility
* **Pd**: Death Rate of Virus
* **K**: Mean Infection Duration (Currently Exponentially Distributed)
* **Runs** : Number of runs for the Monte Carlo Simulations

### Run the simulation
Change svals in [simulator.py](./simulator.py) to experiment with multiple values for the **S** parameter.

Run:
```
python simulator.py
```
Statistics for each value of svals will be printed to stdout.  

Histograms and plots will be automatically saved as .svg files in the directory that the simulation is run in. 


