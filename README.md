# AI-learns-to-play-Flappy-Birds

Here is the source code for a Python project that implements a machine learning algorithm in the Flappy Bird video game using neural networks and a genetic algorithm. 

All code is written in Python using [Pygame](https://www.pygame.org/news) and [NEAT](https://neat-python.readthedocs.io/en/latest/) for genetic algorithm implementation.

![Flappy Bird Screenshot](https://github.com/matisandacz/AI-learns-to-play-Flappy-Birds/tree/main/imgs/flappyBirds.PNG "Flappy Birds")

## Neural Network Architecture

To play the game, each unit (bird) has its own neural network consisted of several layers. All of them have 2 layers in common:
1. an input layer with 2 neurons presenting what a bird sees:
     
     ```
     1) height difference between the bird and the closest top Pipe
     2) height difference between the bird and the closest bottom Pipe
     ```
     
2. an output layer with 1 neuron used to provide an action as follows:
     
     ```
    if output > 0.5 then flap else do nothing
     ```
## The Main Concept of Machine Learning

The main concept of machine learning implemented in this program is based on the neuro-evolution form. It uses evolutionary algorithms such as a genetic algorithm to train artificial neural networks. Here are the main steps:

1. create a new population of 50 units (birds) with a **random neural network** 
2. let all units play the game simultaneously by using their own neural networks
3. for each unit calculate its **fitness** function to measure its quality as:

    ```
    fitness = total travelled distance * 0.1 + 5 * number of pillars
    ```
4. when all units are killed, evaluate the current population to the next one using **genetic algorithm operators** (selection, crossover and mutation) as follows:

    ```
    Complete
    ```
    
5. go back to the step 2

## Implementation

### flappyBirds.py
The entire game logic is implemented in **flappyBirds.py** file.

### Base.py
Class to represent the moving floor.

### Bird.py
class to represent a Bird sprite.

### Pipe.py
Class to represent a moving barrier. This contains a top and bottom sprite.

### config-feedforward.txt

configuration file to modify neuroevolution algorithm parameters.
