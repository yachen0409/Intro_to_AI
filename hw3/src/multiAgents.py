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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        def minmaxagent(agent, depth, state):
            # if win or lose or reach deepest depth -> return value
            if state.isWin() or state.isLose() or depth > self.depth:
                return self.evaluationFunction(state)
            scores = []
            # get what agent can do now
            actions = state.getLegalActions(agent) 
            # evaluate every actions that the current agent can do
            for action in actions:
                nextstate = state.getNextState(agent, action)
                if (agent+1 == state.getNumAgents()):       #if PACMAN and GHOSTS has moved
                    scores.append(minmaxagent(0, depth+1, nextstate))
                else:
                    scores.append(minmaxagent(agent+1, depth, nextstate))
            if agent == 0:              # PACMAN = MAX
                if depth == 1:          # if it is first round
                    return scores
                else:
                    temp_score = max(scores)
            else:                       # GHOSTS = MIN
                temp_score = min(scores)
            
            return temp_score

        PACMAN = 0
        legalactions = gameState.getLegalActions(PACMAN)
        # start the recursion with PACMAN and the depth 1
        scores = minmaxagent(PACMAN, 1, gameState)
        # get max evaluation value and find its index
        maxscore = max(scores)
        indices = []
        for index in range(len(scores)):
            if scores[index] == maxscore:
                indices.append(index)
        chosendindex = random.choice(indices)
        return legalactions[chosendindex]
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        def alphabetaagent(agent, depth, state, alpha, beta):
            # if win or lose or reach deepest depth -> return value
            if state.isWin() or state.isLose() or depth > self.depth:
                return self.evaluationFunction(state)
            scores = []
            # get what agent can do now
            actions = state.getLegalActions(agent) 
            # evaluate every actions that the current agent can do
            for action in actions:
                nextstate = state.getNextState(agent, action)
                if (agent+1 == state.getNumAgents()):       # if PACMAN and GHOSTS has moved
                    temp_score = alphabetaagent(0, depth+1, nextstate, alpha, beta)
                    scores.append(temp_score)
                else:
                    temp_score = alphabetaagent(agent+1, depth, nextstate, alpha, beta)
                    scores.append(temp_score)
                # alpha beta pruning part
                if agent == 0:              
                    if temp_score > beta:
                        return temp_score
                    alpha = max(alpha, temp_score)
                else:                       
                    if temp_score < alpha:
                        return temp_score
                    beta = min(beta, temp_score)
            if agent == 0:              #PACMAN = MAX
                if depth == 1:          #First round
                    return scores
                else:
                    temp_score = max(scores)
            else:                       #GHOSTS = MIN
                temp_score = min(scores)
            return temp_score

        PACMAN = 0
        legalactions = gameState.getLegalActions(PACMAN)
        # alpha and beta initialization
        alpha, beta = -1000000, 1000000     
        # start the recursion with PACMAN and the depth 1
        scores = alphabetaagent(PACMAN, 1, gameState, alpha, beta)
        # get max evaluation value and find its index
        maxscore = max(scores)
        indices = []
        for index in range(len(scores)):
            if scores[index] == maxscore:
                indices.append(index)
        chosendindex = random.choice(indices)
        return legalactions[chosendindex]
        # raise NotImplementedError("To be implemented")
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        def expectimaxagent(agent, depth, state):
            # if win or lose or reach deepest depth -> return value
            if state.isWin() or state.isLose() or depth > self.depth:
                return self.evaluationFunction(state)
            scores = []
            # get what agent can do now
            actions = state.getLegalActions(agent) 
            # evaluate every actions that the current agent can do
            for action in actions:
                nextstate = state.getNextState(agent, action)
                if (agent+1 == state.getNumAgents()):       #if PACMAN and GHOSTS has moved
                    scores.append(expectimaxagent(0, depth+1, nextstate))
                else:
                    scores.append(expectimaxagent(agent+1, depth, nextstate))
            if agent == 0:              # PACMAN = MAX
                if depth == 1:          # First round
                    return scores
                else:
                    temp_score = max(scores)
            else:                       #GHOSTS
                temp_score = float(sum(scores)/len(scores))    #expectimax calculate
            return temp_score

        PACMAN = 0
        legalactions = gameState.getLegalActions(PACMAN)
        # start the recursion with PACMAN and the depth 1
        scores = expectimaxagent(PACMAN, 1, gameState)
        # get max evaluation value and find its index
        maxscore = max(scores)
        indices = []
        for index in range(len(scores)):
            if scores[index] == maxscore:
                indices.append(index)
        chosendindex = random.choice(indices)
        return legalactions[chosendindex]
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    curscore = currentGameState.getScore()  #get current score
    pacmanpos = currentGameState.getPacmanPosition()    #get pacman position
    ghostpos = currentGameState.getGhostPositions()     #get ghosts position
    foodlist = currentGameState.getFood().asList()      #get food list
    foodnum = len(foodlist)
    capsulelist = currentGameState.getCapsules()        #get capsule list
    capsulenum = len(capsulelist)
    closestfood = 1
    closestcapsule = 1

    # calculate distances from pacman to all food and capsule
    fooddis= [manhattanDistance(pacmanpos, foodpos) for foodpos in foodlist]
    capsuledis= [manhattanDistance(pacmanpos, capsulepos) for capsulepos in capsulelist]

    # Find min food_distance and capsule_distance
    if len(foodlist) > 0:
        closestfood = min(fooddis)
    if len(capsulelist) > 0:
        closestcapsule = min(capsuledis)
    # Find distances from pacman to ghosts
    for position in ghostpos:
        ghostdis = manhattanDistance(pacmanpos, position)
        # If ghost is close to pacman, escape from ghosts first
        # by resetting the value of closestfood and closestcapsule
        if ghostdis < 3:
            closestfood = 99999
            closestcapsule= 99999
    # if closest capsule distance is bigger than closest food distance
    # Go for food first by resetting closestcapsule 
    if closestcapsule > closestfood:
        closestcapsule= 99999
    # if closest capsule distance is smaller than closest food distance
    # Go for food first by resetting closestfood 
    else:
        closestfood= 99999
    # set evaluation features and their weights 
    features = [1.0/closestfood, 1.0/closestcapsule, curscore, foodnum, capsulenum]
    weights = [1, 1, 50, -1, -1]
    # Linear combination of features
    return sum([feature * weight for feature, weight in zip(features, weights)])
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
