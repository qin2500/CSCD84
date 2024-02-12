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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the~
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

        if successorGameState.isWin():
            return 999999

        foodDist = [util.manhattanDistance(newPos, food) for food in newFood.asList()]
        minFood = 2 * min(foodDist) if len(foodDist)>0 else -1

        ghostDist = [util.manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        averageGhostDist = -1
        if len(ghostDist) > 0:
            averageGhostDist = sum(ghostDist)/len(ghostDist) + 0.0001

        nearByGhosts = 0
        for d in ghostDist:
            if d < 1:
                nearByGhosts += 1


        stopPenalty = 1 if action == Directions.STOP else 0



        return successorGameState.getScore() - (1/averageGhostDist) + (1/minFood) -stopPenalty - nearByGhosts

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        numAgents = gameState.getNumAgents()
        def minmax(state: GameState, depth, agentIndex):
            if depth == self.depth or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)
            
            if agentIndex ==  0:  # Pacman's turn (max node)
                legalActions = state.getLegalActions(agentIndex)
                maxValue = float('-inf')
                maxAction = None
                for action in legalActions:
                    nextState = state.generateSuccessor(agentIndex, action)
                    nextValue, nextAction = minmax(nextState, depth,  1)
                    if maxValue < nextValue:
                        maxValue = nextValue
                        maxAction = action
                return (maxValue, maxAction)
            
            else:  # Ghost's turn (min node)
                legalActions = state.getLegalActions(agentIndex)
                nextIndex = (agentIndex +  1) if not(agentIndex + 1 == gameState.getNumAgents()) else  0

                if nextIndex == 0:
                    depth += 1

                minValue = float('+inf')
                minAction = None
                for action in legalActions:
                    nextState = state.generateSuccessor(agentIndex, action)
                    nextValue, nextAction = minmax(nextState, depth, nextIndex)
                    if minValue > nextValue:
                        minValue = nextValue
                        minAction = action
                return (minValue, minAction)
                
        value, action = minmax(gameState,  0,  0)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        
        def minmax(state: GameState, depth, agentIndex, a, b):
            if depth == self.depth or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)
            
            if agentIndex ==  0:  # Pacman's turn (max node)
                legalActions = state.getLegalActions(agentIndex)
                maxValue = float('-inf')
                maxAction = None
                for action in legalActions:
                    nextState = state.generateSuccessor(agentIndex, action)
                    nextValue, nextAction = minmax(nextState, depth,  1, a, b)
                    if maxValue < nextValue:
                        maxValue = nextValue
                        maxAction = action
                    #Pruning
                    if maxValue > b: return (maxValue, maxAction)
                    a = max(a,maxValue)
                return (maxValue, maxAction)
            
            else:  # Ghost's turn (min node)
                legalActions = state.getLegalActions(agentIndex)
                nextIndex = (agentIndex +  1) if not(agentIndex + 1 == gameState.getNumAgents()) else  0

                if nextIndex == 0:
                    depth += 1

                minValue = float('+inf')
                minAction = None
                for action in legalActions:
                    nextState = state.generateSuccessor(agentIndex, action)
                    nextValue, nextAction = minmax(nextState, depth, nextIndex, a, b)
                    if minValue > nextValue:
                        minValue = nextValue
                        minAction = action
                    #Pruning
                    if minValue < a: return (minValue, minAction)
                    b = min(b,minValue)
                return (minValue, minAction)
                
        value, action = minmax(gameState,  0,  0, float('-inf'), float("inf"))
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def minmax(state: GameState, depth, agentIndex):
            if depth == self.depth or state.isWin() or state.isLose():
                return (self.evaluationFunction(state), None)
            
            if agentIndex ==  0:  # Pacman's turn (max node)
                legalActions = state.getLegalActions(agentIndex)
                maxValue = float('-inf')
                maxAction = None
                for action in legalActions:
                    nextState = state.generateSuccessor(agentIndex, action)
                    nextValue, nextAction = minmax(nextState, depth,  1)
                    if maxValue < nextValue:
                        maxValue = nextValue
                        maxAction = action
                return (maxValue, maxAction)
            
            else:  # Ghost's turn (min node)
                legalActions = state.getLegalActions(agentIndex)
                nextIndex = (agentIndex +  1) if not(agentIndex + 1 == gameState.getNumAgents()) else  0

                if nextIndex == 0:
                    depth += 1

                minValue = 0
                minAction = None
                for action in legalActions:
                    nextState = state.generateSuccessor(agentIndex, action)
                    nextValue = minmax(nextState, depth, nextIndex)[0]
                    minValue += nextValue/len(legalActions)
                return (minValue, minAction)
                
        value, action = minmax(gameState,  0,  0)
        return action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    caps = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    if currentGameState.isWin():
        return 999999

    foodDist = [util.manhattanDistance(pos, food) for food in food.asList()]
    minFood = 2 * min(foodDist) if len(foodDist)>0 else -1

    ghostDist = [util.manhattanDistance(pos, ghost.getPosition()) for ghost in ghostStates]
    averageGhostDist = -1
    if len(ghostDist) > 0:
        averageGhostDist = sum(ghostDist)/len(ghostDist) + 0.0001

    nearByGhosts = 0
    for d in ghostDist:
        if d < 1:
            nearByGhosts += 1



    return currentGameState.getScore() - (1/averageGhostDist) + (1/minFood) - nearByGhosts - len(caps)

# Abbreviation
better = betterEvaluationFunction
