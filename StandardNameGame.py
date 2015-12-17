# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 08:38:50 2015

@author: Devon Brackbill

Simulations for Committed Minorities in the Standard Name Game.

Question: "In a population where everyone uses norm B,
what fraction of the population needs to be committed to a new norm A
to sway the majority to adopt this new minority convention?"

Answer: ~10%

With 2 norms, there are 2 fixed points in the system that vary as a function
of the proportion of the population that are committed agents.
There is a phase transition from a regime where there is virtually no adoption
when there is less than ~10% committed agents to a regime where there is
universal adoption above this threshold.

The model is based on agents who are just trying to coordinate
and who have an interaction strategy described in Baronchelli et al. 2006
"""

from __future__ import division
import random
import os
import pandas as pd
import sys

class SNGAgent():
    '''
    each Agent can speak() to another agent by choosing a random word from
    its memory, unless it's a robot. Robots always play the same name.
    Robot = committed agent.
    
    PARAMS:
    id = unique id number for each agent
    memory = vector of unique memories
    is_robot = whether agent is committed to the new norm
    '''
    def __init__(self, id, memory=[], is_robot = False):
        if type(memory) is not list:
            raise NameError('memory obj must be a list')
        self.id = id
        self.memory = memory
        self.is_robot = is_robot
        
    def speak(self):
        if self.is_robot:
            word = 'A'
        else:
            word = random.choice(self.memory)
        return word
        
class SNGHerd():
    '''
    a Herd is a list of agents
    
    PARAMS:
    popSize = number of Agents in the Herd
    prop_CM = proportion of population that is committed to the new norm Agent
    (e.g., a robot)
    '''

    def __init__(self, popSize, prop_CM=0):
        
        self.herd = []
        self.prop_CM = prop_CM
        self.popSize = popSize
        self.num_CM = round(self.prop_CM*self.popSize)
        
        '''add agents'''
        for i in range(0,self.popSize):
            if (i < self.num_CM):
                self.herd.append(SNGAgent(i, memory=['A'], is_robot = True))
            else:
                self.herd.append(SNGAgent(i, memory=['B'], is_robot = False))
        
    def Interact(self):
        '''
        An Interact() event occurs in a homogeneously mixing population.
        First, a speaker speak()'s
        Then, a hearer checks its memory for a match
        If a match, both hearer and speaker trim memory to that word only.
        Else, hearer adds word to memory.
        '''
        speaker_num = random.randrange(start=0, stop=self.popSize,step=1)
        hearer_num = random.randrange(start=0, stop=self.popSize,step=1)
        # make sure speaker != hearer
        while speaker_num == hearer_num:
            hearer_num = random.randrange(start=0, stop=self.popSize,step=1)
        
        speaker = self.herd[speaker_num]
        hearer = self.herd[hearer_num]
        
        word = speaker.speak()
 
        if word in hearer.memory:
            speaker.memory = [word]
            hearer.memory = [word]
        else:
            hearer.memory.append(word)
        
        if hearer.is_robot:
            hearer.memory = ['A']
            
        # ensure memories have unique sets 
        # (mostly a leftover from running sims with >2 norms in the population)
        speaker.memory = list(set(speaker.memory))
        hearer.memory = list(set(hearer.memory))
        
        return (word)
        
def CMSim(n, proportion_cm, num_rounds=100):
    '''
    A CMSim() makes a Herd Interact() and keeps track of its history.
    
    OUTPUT: A dataframe with the following columns:
        num_interactions: number of iterations the Herd experienced
        proportionA: proportion of final n interactions that involved speaking norm A
        proportionB: ...and speaking norm B
        popSize: the size of the Herd
        maxMemory: a dummy indicator to compare with simulations from a separate model (not included here)
        prop_CM: proportion who were committed agents (e.g., robots) in the population
    
    PARAMS:
    n = population size
    proportion_cm = proportion of population that is committed (e.g., a robot)
    num_rounds = maximum number of 'rounds' to run (a 'round' = n interactions),
        so this parameter means run n*num_rounds total interactions among agents.
    '''
    history = []
    iterations = 0

    the_herd = SNGHerd(popSize = n, prop_CM = proportion_cm)
    
    while True:
        iterations += 1
        play = the_herd.Interact()

        history.append(play)
        
        # end if max interactions reached
        if iterations > num_rounds*the_herd.popSize:
            break
        
        # end if group converges on a norm
        if iterations % n == 0:
            if history[-the_herd.popSize:].count('A')/ the_herd.popSize == 1:
                break

    proportionA = history[-the_herd.popSize:].count('A') / the_herd.popSize
    proportionB = 1-proportionA
    output = {'num_interactions': iterations,
              'proportionA': proportionA,
              'proportionB': proportionB,
              'popSize' : the_herd.popSize,
              'maxMemory': 999,   # dummy indicator to compare with simulations in a separate model
              'prop_CM' : the_herd.prop_CM}              
    return (output)

def main(argv):
    '''
    The command line version to run many CMSim()'s
    
    The output is a dataframe object that lists the results of the simulations
    The function appends to the output file as it runs, so it is possible to
        copy this file to a separate directory and open it to view the results
        while the simulator is running.
    Note, this constant appending slows performance, but I usually run this on
        multiple machines (e.g., 100 of the cheapest instances on Digital Ocean)
        and just collect the data from all the machines until I have the number of 
        simulations I want.
        
    
    PARAMS TO COMMAND LINE:
    [1] = popSize = population size
    [2] = num_sims = number of simulations per parameter
    [3] = FILE_NUM = file number to append to output name (useful if running across
        many computers)
    [4] = PATH_TO_OUTPUT = output location to save results
    '''
    
    if len(argv)!=5:
        raise ValueError('Invoke with: python StandardNameGame.py <population size> <number of simulations> <file number> <output path>')
        
    popSize = int(argv[1])
    num_sims = int(argv[2])
    '''new method for naming filenums directly in cmd line call'''
    FILE_NUM = int(argv[3])
    PATH_TO_OUTPUT  = argv[4]

    # change this as desired to run different ranges of proportion CM
    prop_CM = range(5, 31)
    prop_CMs = [x / 100 for x in prop_CM]
    
    counter = 0
    for sim in range(0,num_sims):
        for prop_CM in prop_CMs:
            # adjust this counter b/c it can get annoying (maybe adjust this automatically based on population size and num_sims?)
            if counter % 100 == 0 :
                print '%d simulations complete' % counter
            
            results = CMSim(popSize, prop_CM)
            results = [results]
                           
            counter +=1
            
            to_send = pd.DataFrame.from_dict(results)
            
            if counter == 1:
                SAVE_NAME = PATH_TO_OUTPUT + '/SNGSimulations' + str(FILE_NUM) + '.csv'
                to_send.to_csv(SAVE_NAME)
            else:
                to_send.to_csv(SAVE_NAME, mode='a', header=False)
        
if __name__ == "__main__":
   main(sys.argv)