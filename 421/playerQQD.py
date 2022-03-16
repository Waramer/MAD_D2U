#!env python3
"""
# Our Q learner applied on 421

Group: DELEZENNE Quentin

"""
import random
import matplotlib.pyplot as plt
import numpy as np
import json

# MAIN: 

def main() :
    import game421 as game

    averages=[]

    gameEngine= game.Engine()
    player= PlayerQ()
    numberOfGames= 1000
    numberOfEpisodes = 200
    rewards= gameEngine.start( player, numberOfGames )

    # Import Q values from JSON
    try:
        print("Trying to import Q Values from 'data.json' ... ")
        with open('data.json') as json_file:
            player.qvalues = json.load(json_file)
        print("Import succeeded")
    except:
        print("'data.json' file doesn't exist ")

    # Learning
    for episod in range(1,numberOfEpisodes+1) :
        rewards= gameEngine.start( player, numberOfGames )
        print("Episode "+str(episod)+", average: "+str( sum(rewards)/len(rewards)))
        averages.append(sum(rewards)/len(rewards))

    # testing
    print("I want to win !")
    player.epsilon = 0.0
    rewardsF = gameEngine.start( player,10000)
    averageF = sum(rewardsF)/len(rewardsF)
    print("Average: "+str(averageF))

    # Export in Q Values in JSON
    with open('data.json', 'w') as fp:
        json.dump(player.qvalues, fp,  indent=4)
    print("Q Values exported in JSON")

    # Affichage
    plt.plot(np.linspace(1,numberOfEpisodes,numberOfEpisodes),averages,color='b')
    plt.scatter([numberOfEpisodes+1],[averageF],color='r')
    plt.show()

    # Print average Q Values for each state :
    # print( player.qvalues['9-1-1-1'] )
    # for st in player.qvalues :
    #     avg = 0
    #     for action,qval in player.qvalues[st].items():
    #         avg += qval
    #     avg = avg/len(player.qvalues[st])
    #     print( st +": "+ str(avg) )

# ACTIONS: 

actions= []
for a1 in ['keep', 'roll']:
    for a2 in ['keep', 'roll']:
        for a3 in ['keep', 'roll']:
            actions.append( a1+'-'+a2+'-'+a3 )

# Q LEARNER: 

class PlayerQ() :
    def __init__(self,alpha=0.1,epsilon=0.1,gamma=1.0):
        self.results= []
        # Q Learning code and constants
        self.qvalues= {}
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
    
    # State Machine :
    def stateStr(self):
        s= str(self.turn)
        for d in self.dices :
            s += '-' + str(d)
        return s

    # AI interface :
    def wakeUp(self, numberOfPlayers, playerId, tabletop):
        self.scores= [ 0 for i in range(numberOfPlayers) ]
        self.id= playerId
        self.model= tabletop
        self.turn= 9
        self.dices= [1, 1, 1]
        self.action= 'roll-roll-roll'
        # ==== Q Learning code ====
        self.state = self.stateStr()
        self.lastState = self.state
        if self.state not in self.qvalues.keys() :
            self.qvalues[self.state]= { "keep-keep-keep":0.0, "roll-keep-keep":0.0, "keep-rollkeep":0.0, "roll-roll-keep":0.0, "keep-keep-roll":0.0, "roll-keep-roll":0.0, "keep-roll-roll":0.0, "roll-roll-roll":0.0 }

    def perceive(self, turn, scores, pieces):
        self.reward= scores[ self.id ] - self.scores[ self.id ]
        self.scores= scores
        self.turn= turn
        self.dices= pieces
        # ==== Q Learning code ====
        # Memorize
        self.lastState = self.state
        # Actual State
        self.state = self.stateStr()
        if self.state not in self.qvalues.keys() :
            self.qvalues[self.state]= { "keep-keep-keep":0.0, "roll-keep-keep":0.0, "keep-roll-keep":0.0, "roll-roll-keep":0.0, "keep-keep-roll":0.0, "roll-keep-roll":0.0, "keep-roll-roll":0.0, "roll-roll-roll":0.0 }
        # Update Q value of last state
        self.updateQ()

    def updateQ(self):
        self.qvalues[self.lastState][self.action]=(1-self.alpha)*self.qvalues[self.lastState][self.action]+self.alpha*(self.reward+self.gamma*self.maxQ(self.state))

    def maxQ(self,state):
        return self.qvalues[state][max(self.qvalues[state], key=self.qvalues[state].get)]

    def decide(self):
        decision = random.uniform(0, 1)
        # ==== Q Learning code ====
        # Exploration
        if decision <= self.epsilon :
            self.action = random.choice(actions)
        # Exploitation
        else :
            self.action = self.selectBestAction()
        # print( f'state: { self.stateStr() }, action: { self.action }')
        return self.action
    
    def selectBestAction(self):
        return max(self.qvalues[self.state], key=self.qvalues[self.state].get)
    
    def sleep(self, result):
        self.results.append(result)


# SCRIPT EXECUSION: 
if __name__ == '__main__':
    print("Let's go !!!")
    main()
