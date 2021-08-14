import pygame
import os
import random
import neat

from Bird import *
from Pipe import *
from Base import *

WIN_WIDTH = 600
WIN_HEIGHT = 800
score = 0

pygame.display.set_caption("AI Learns to play Flappy Bird")
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(birds, pipes, base):
    global win

    win.blit(bg_img, (0,0))
    
    for bird in birds:
        bird.draw(win)

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    
    draw_score()
   
    pygame.display.update()

def draw_score():
    global win
    global score

    scoreText = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(scoreText, (WIN_WIDTH - 10 - scoreText.get_width(), 10))
 

def eval_genomes(genomes, config):

    global win
    global score

    BIRD_START_X = 230
    BIRD_START_Y = 350
    PIPE_START_Y = 600

    clock = pygame.time.Clock()
    run = True
    score = 0
    shouldAddPipe = False

    birds = []
    nets = []
    genomes_copy = []

    pipes = [Pipe(PIPE_START_Y)]
    base = Base(WIN_HEIGHT)

    for _, genome in genomes:

        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        nets.append(net)
        birds.append(Bird(BIRD_START_X, BIRD_START_Y))
        genomes_copy.append(genome)

    while run:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if len(birds) == 0:
            run = False
            break

        pipeIdx = calculatePipeAheadIdx(birds, pipes)

        moveBirds(birds, genomes_copy, nets, pipes, pipeIdx)
        
        checkForCollisions(pipes, birds, genomes_copy, nets)

        shouldAddPipe = shouldAddNewPipe(pipes, birds)
    
        killBirdsOutOfScreenBounds(birds, nets, genomes_copy, base)

        removePipeOutOfScreenBounds(pipes)

        addPipe(genomes, pipes, shouldAddPipe)

        if shouldAddPipe:
            shouldAddPipe = False

        for pipe in pipes:
            pipe.move()

        base.move()

        draw_window(birds, pipes, base)

def addPipe(genomes, pipes, shouldAddPipe):
    if shouldAddPipe:
        for _ , genome in genomes:
            genome.fitness += 5
        pipes.append(Pipe(600))

def shouldAddNewPipe(pipes, birds):
    global score
    add_pipe = False
    for pipe in pipes:
        for birdIdx, bird in enumerate(birds):
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                score += 1
    return add_pipe

def checkForCollisions(pipes, birds, genomes_copy, nets):
    for pipe in pipes:    
        for birdIdx, bird in enumerate(birds):
            if pipe.collide(bird):
                genomes_copy[birdIdx].fitness -= 1
                birds.pop(birdIdx)
                nets.pop(birdIdx)
                genomes_copy.pop(birdIdx)

def removePipeOutOfScreenBounds(pipes):
    toRemove = []
    for pipe in pipes:
        if pipe.x + pipe.WIDTH < 0:
            toRemove.append(pipe)
    for pipe in toRemove:
        pipes.remove(pipe)

def killBirdsOutOfScreenBounds(birds, nets, genomes_copy, base):
    for birdIdx, bird in enumerate(birds):
        if bird.y + bird.img.get_height() >= base.y or bird.y < 0:
            birds.pop(birdIdx)
            nets.pop(birdIdx)
            genomes_copy.pop(birdIdx)

def calculatePipeAheadIdx(birds, pipes):
        pipeIdx = 0

        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipeIdx = 1

        return pipeIdx

def moveBirds(birds, genomes_copy, nets, pipes, pipeIdx):

    for birdIdx, bird in enumerate(birds):
            
        genomes_copy[birdIdx].fitness += 0.1
        bird.move()
        
        output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipeIdx].height), abs(bird.y - pipes[pipeIdx].bottom)))


        if output[0] > 0.5:
            bird.jump()

    
def run(config_file):
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    #Create population
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)