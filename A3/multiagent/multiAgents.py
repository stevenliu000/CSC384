# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        '''
        print "getsocre():", successorGameState.getScore()
        print "newPos:,", newPos
        print "newFood:",newFood 
        print "newGhostStates:", newGhostStates
        print "scaredtimes:",newScaredTimes
        '''

        score = 0

        # determine terminal states
        if successorGameState.isWin():
          return 10000000
        if successorGameState.isLose():
          return -10000000

        # adding getScore()
        score += successorGameState.getScore()

        # score from food
        for x, valuex in enumerate(newFood):
          for y, valuey in enumerate(valuex):
            if valuey == True:
              score += 1/(abs(newPos[0]-x)+abs(newPos[1]-y)+random.random())

        # score from ghosts
        newGhostPosition = successorGameState.getGhostPositions()
        for i in newGhostPosition:
          dist = abs(newPos[0]-i[0])+abs(newPos[1]-i[1])
          if newScaredTimes[0] >= 5:
            score += 2/dist
          else:
            if dist == 2:
              score -= 100000
            if dist <= 3:
              score -= 3/dist

        # score from capsule
        newCapsules = currentGameState.getCapsules()
        for i in newCapsules:
          score += 2.5/(abs(newPos[0]-i[0])+abs(newPos[1]-i[1])+random.random())

        # prevent stoping
        if action == Directions.STOP:
          score -= 100

        #return successorGameState.getScore()
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.DFMiniMax(gameState, 0, self.depth)[0]
      
    def DFMiniMax(self, curGameState, agentIndex, curDepth):
      if curDepth == 0 or curGameState.isWin() or curGameState.isLose():
        return Directions.STOP, self.evaluationFunction(curGameState)

      actions = curGameState.getLegalActions(agentIndex)

      # Max Node
      if agentIndex == 0:
        BEST = -10000000000
        for action in actions:
          dummy, V = self.DFMiniMax(curGameState.generateSuccessor(agentIndex, action), agentIndex+1, curDepth)
          if V > BEST:
            Action = action
            BEST = V

      # Min Node
      else:
        BEST = 100000000000
        for action  in actions:
          if agentIndex == curGameState.getNumAgents() - 1:
            dummy, V = self.DFMiniMax(curGameState.generateSuccessor(agentIndex,action), 0, curDepth-1)
          else:
            dummy, V = self.DFMiniMax(curGameState.generateSuccessor(agentIndex,action), agentIndex+1, curDepth)
          if V < BEST:
            Action = action
            BEST = V

      return Action, BEST


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBeta(gameState, 0, self.depth, -100000000000, 100000000000)[0]


    def AlphaBeta(self, curGameState, agentIndex, curDepth, Alpha, Beta):
      if curDepth == 0 or curGameState.isWin() or curGameState.isLose():
        return Directions.STOP, self.evaluationFunction(curGameState), self.evaluationFunction(curGameState)

      actions = curGameState.getLegalActions(agentIndex)

      # Max Node
      if agentIndex == 0:
        BEST = -10000000000
        for action in actions:
          dummy, V, alpha = self.AlphaBeta(curGameState.generateSuccessor(agentIndex, action), agentIndex+1, curDepth, Alpha, Beta)
          Alpha = max(Alpha, alpha)
          if V > BEST:
            Action = action
            BEST = V
          if Beta <= Alpha:
            break
        return Action, BEST, Alpha

      # Min Node
      else:
        BEST = 100000000000
        for action  in actions:
          if agentIndex == curGameState.getNumAgents() - 1:
            dummy, V, beta = self.AlphaBeta(curGameState.generateSuccessor(agentIndex,action), 0, curDepth-1, Alpha, Beta)
          else:
            dummy, V, beta = self.AlphaBeta(curGameState.generateSuccessor(agentIndex,action), agentIndex+1, curDepth, Alpha, Beta)
          Beta = min(Beta, beta)
          if V < BEST:
            Action = action
            BEST = V
          if Beta <= Alpha:
            break
        return Action, BEST, Beta


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.Expectimax(gameState, 0, self.depth)[0]

    def Expectimax(self, curGameState, agentIndex, curDepth):
      Action = Directions.STOP

      if curDepth == 0 or curGameState.isWin() or curGameState.isLose():
        return Action, self.evaluationFunction(curGameState)

      actions = curGameState.getLegalActions(agentIndex)

      # Max Node
      if agentIndex == 0:
        BEST = -10000000000
        for action in actions:
          dummy, V = self.Expectimax(curGameState.generateSuccessor(agentIndex, action), agentIndex+1, curDepth)
          if V > BEST:
            Action = action
            BEST = V

      # Min Node
      else:
        BEST = 0
        for action  in actions:
          if agentIndex == curGameState.getNumAgents() - 1:
            dummy, V = self.Expectimax(curGameState.generateSuccessor(agentIndex,action), 0, curDepth-1)
          else:
            dummy, V = self.Expectimax(curGameState.generateSuccessor(agentIndex,action), agentIndex+1, curDepth)
          BEST += V
        BEST = float(BEST)/float(len(actions))

      return Action, BEST


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      score is calculated by:
        1. cuurent score
          - add the current score of the currentGameState
        2. score from food
          - calculate the manhanttan distance between every food and Pacman, but I add some random to get out of some "local minimum"
          - add 1/distance to score to award the closer distance between food and Pacman
          - minus 1 for every food to penalize the state of "not-eating-food"
        3. score form ghosts
          - calculate the manhanttan distance between every ghost and Pacman, but I add some random to get out of some "local minimum"
          - if the ghost's scaredtime is larger than 5, which means Pacman can safely eat it and earn points: so add 2/distance to score to award the closer distance between scared ghost and Pacman.
          - if the distance between ghosts and Pacman is less than 3, Pacman will have chance to loss if Pacman plays poorly. So minus 3/distance to penalize the closer distance between Pacman and ghosts.
        4. score from capsules
          - calculate the manhanttan distance between every capsule and Pacman, but I add some random to get out of some "local minimum"
          - add 2.5/distance to score to award the closer distance between capsule and Pacman
          - minus 2.4 for every food to penalize the state of "not-eating-capsule"
    """
    "*** YOUR CODE HERE ***"
    score = 0

    food = currentGameState.getFood()
    position = currentGameState.getPacmanPosition()
    ghostPositions = currentGameState.getGhostPositions()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsules = currentGameState.getCapsules()

    
    if currentGameState.isWin():
      return 10000000
    if currentGameState.isLose():
      return -10000000
    

    # adding getScore()
    score += currentGameState.getScore()

    # score from food
    for x, valuex in enumerate(food):
      for y, valuey in enumerate(valuex):
        if valuey == True:
          score += 1/(abs(position[0]-x)+abs(position[1]-y)+random.random())
          score -= 1

    # score from ghosts
    for i in ghostPositions:
      dist = abs(position[0]-i[0])+abs(position[1]-i[1]+random.random())
      if scaredTimes[0] >= 5:
        score += 3/dist
      else:
        if dist == 2:
          score -= 100000
        if dist <= 3:
          score -= 3/dist

    # score from capsules
    for i in capsules:
      score += 2.5/(abs(position[0]-i[0])+abs(position[1]-i[1])+random.random())
      score -= 2.4

    return score
    

# Abbreviation
better = betterEvaluationFunction

