# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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

    newScore = successorGameState.getScore()
    for ghost in newGhostStates :
      dToGhost = manhattanDistance(newPos, ghost.getPosition())
      if ghost.scaredTimer > 0:
        if dToGhost > 0 :
          newScore -= 5/(dToGhost*dToGhost)
        else :
          newScore -= 10
      else :
        if dToGhost > 0 :
          newScore -= 10/(dToGhost*dToGhost)
        else :
          newScore -= 100

    nearestFood = 1000000
    for food in newFood.asList() :
      if manhattanDistance(newPos, food) < nearestFood:
        nearestFood = manhattanDistance(newPos, food)
    newScore += 10/nearestFood

    if action == "STOP":
      newScore -= 1

    return newScore

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    def minimax(gameState, depth, agent) :
      if gameState.isWin() or gameState.isLose() :
        return self.evaluationFunction(gameState)
      
      agent %= gameState.getNumAgents()
      if agent == gameState.getNumAgents()-1 and depth == self.depth :
        return self.evaluationFunction(gameState)
      if agent == 0 :
        return max(minimax(gameState.generateSuccessor(agent, action), depth + 1, agent + 1) for action in gameState.getLegalActions(agent))
      else :
        return min(minimax(gameState.generateSuccessor(agent, action), depth, agent + 1) for action in gameState.getLegalActions(agent))

    return max(gameState.getLegalActions(0), key = lambda action : minimax(gameState.generateSuccessor(0, action), 0, 1))

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    alpha = float("-inf")
    beta = float("inf")
    def alphaBeta(gameState, depth, agent, alpha, beta) :
      if gameState.isWin() or gameState.isLose() :
        return self.evaluationFunction(gameState) 
      agent %= gameState.getNumAgents()
      if agent == gameState.getNumAgents() - 1 and depth == self.depth :
        return self.evaluationFunction(gameState)
      
      if agent == 0 :
        val = maxVal(gameState, depth, agent, alpha, beta)
        return val
      else :
        val = minVal(gameState, depth, agent, alpha, beta)
        return val

    def maxVal(gameState, depth, agent, alpha, beta) :
      val = float("-inf")
      for action in gameState.getLegalActions(agent) :
        val =  max(val, alphaBeta(gameState.generateSuccessor(agent, action), depth + 1, agent + 1, alpha, beta))
        if val >= beta : return val
        alpha = max (val, alpha)
      return val

    def minVal(gameState, depth, agent, alpha, beta) :
      val = float("inf")
      for action in gameState.getLegalActions(agent) :
        val = min(val, alphaBeta(gameState.generateSuccessor(agent, action), depth, agent + 1, alpha, beta))
        if val <= alpha : return val
        beta = min (val, beta)
      return val

    val = float("-inf")
    action = Directions.WEST
    for nxtAction in gameState.getLegalActions(0) :
      nxtVal = alphaBeta(gameState.generateSuccessor(0, nxtAction), 0, 1, alpha, beta)
      if nxtVal >= val :
        val = nxtVal
        action = nxtAction
      if val >= beta : return action
      alpha = max(val, alpha)
    return action
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
    def expectimax(gameState, depth, agent) :
      if gameState.isWin() or gameState.isLose() or depth == self.depth :
        return self.evaluationFunction(gameState)
      
      agent %= gameState.getNumAgents()
      if agent == 0 :
        return max(expectimax(gameState.generateSuccessor(agent, action), depth + 1, agent + 1) for action in gameState.getLegalActions(agent))
      else :
        return mean(expectimax(gameState.generateSuccessor(agent, action), depth, agent + 1) for action in gameState.getLegalActions(agent))
    
    def mean(vals) :
      sum = 0
      count = 0
      for val in vals :
        sum += val
        count += 1
      return sum / count 
    
    return max(gameState.getLegalActions(0), key = lambda action : expectimax(gameState.generateSuccessor(0, action), 0, 1))

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  pos = currentGameState.getPacmanPosition()
  foods = currentGameState.getFood()
  ghosts = currentGameState.getGhostStates()
  score = currentGameState.getScore()

  for ghost in ghosts :
    dToGhost = manhattanDistance(pos, ghost.getPosition())
    if ghost.scaredTimer > 0:
      if dToGhost > 0 :
        score -= 5/(dToGhost*dToGhost)
      else :
        score -= 10
    else :
      if dToGhost > 0 :
        score -= 10/(dToGhost*dToGhost)
      else :
        score -= 100

  nearestFood = 1000000
  for food in foods.asList() :
    if manhattanDistance(pos, food) < nearestFood:
      nearestFood = manhattanDistance(pos, food)
  score += 10/nearestFood

  return score






# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

