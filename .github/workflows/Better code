from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from game import Actions
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
        
        distances = 0.0
        result = 0.0
        foodList = newFood.asList()
        ghostLocation = [each.getPosition() for each in newGhostStates]

        if len(foodList) < len(currentGameState.getFood().asList()):
            result += 100
        if newPos in ghostLocation:
            result -= 1000
        if len(foodList):
            result += 5/(0.1+manhattanDistance(newPos, min(foodList)) )
        for i in range(len(foodList)):
            distances += 2/(0.1+manhattanDistance(newPos, foodList[i]))
        result += distances
        for i in range(len(ghostLocation)):
            result -= 1/(0.1+manhattanDistance(newPos, ghostLocation[i]))
        for times in newScaredTimes:
            result += 100*times
        return result

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
##    def __init__(self, evalFn = 'betterEvaluationFunction', depth = '2'):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        self.agentnum = gameState.getNumAgents()
        def maxval(state, depth, agentid=0):
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state)
            v = -float("inf")
            for each in state.getLegalActions(agentid):
                v = max(v, minval(state.generateSuccessor(agentid, each),depth,agentid+1))
            return v

        def minval(state, depth, agentid=1):
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state)
            v = float("inf")
            for each in state.getLegalActions(agentid):
                if agentid != self.agentnum-1:
                    v = min(v, minval(state.generateSuccessor(agentid, each), depth,agentid+1))
                else:                 
                    v = min(v, maxval(state.generateSuccessor(agentid, each), depth-1,0))
            return v

        actions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, each) for each in actions] 
        mins = [minval(each, self.depth, 1) for each in successors]
##        print(max(mins))
        return actions[mins.index(max(mins))]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.agentnum = gameState.getNumAgents()
        def maxval(state, depth, agentid, a,b):
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state)
            v = -float("inf")
            for each in state.getLegalActions(agentid):
                v = max(v, minval(state.generateSuccessor(agentid, each),depth,agentid+1,a,b))
                if v>b:
                    return v
                a = max(a,v)
            return v

        def minval(state, depth, agentid,a,b):
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state)
            v = float("inf")
            for each in state.getLegalActions(agentid):
                if agentid != self.agentnum-1:
                    v = min(v, minval(state.generateSuccessor(agentid, each), depth,agentid+1,a,b))
                else:         
                    v = min(v, maxval(state.generateSuccessor(agentid, each), depth-1,0,a,b))
                if v<a:
                    return v
                b = min(b,v)
                    
            return v

        def topmax(state, depth, agentid, a, b):
            #revise
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state)
            v = -float("inf")
            choice = state.getLegalActions(0)[0]
            for each in state.getLegalActions(agentid):
                if v<minval(state.generateSuccessor(agentid, each),depth,agentid+1,a,b):
                    choice = each
                v = max(v, minval(state.generateSuccessor(agentid, each),depth,agentid+1,a,b))
                a = max(a,minval(state.generateSuccessor(agentid, each),depth,agentid+1,a,b))
            return choice

        result = topmax(gameState,self.depth,0,-float("inf"),float("inf"))
        return result
##        actions = gameState.getLegalActions(0)
##        successors = [gameState.generateSuccessor(0, each) for each in actions] 
##        mins = [minval(each, self.depth, 1,-float("inf"),float("inf")) for each in successors]
####        print(max(mins))
##        return actions[mins.index(max(mins))]

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
        import random
        self.agentnum = gameState.getNumAgents()
        def maxval(state, depth, agentid=0):
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state)
            v = -float("inf")
            for each in state.getLegalActions(agentid):
                v = max(v, avgval(state.generateSuccessor(agentid, each),depth,agentid+1))
            return v

        def avgval(state, depth, agentid=1):
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state)
            
            vals=0
            for each in state.getLegalActions(agentid):
                if agentid != self.agentnum-1:
                    vals += avgval(state.generateSuccessor(agentid, each), depth,agentid+1)
                else:
                    vals += maxval(state.generateSuccessor(agentid, each), depth-1,0)
                v = vals/len(state.getLegalActions(agentid))
            return v

        actions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, each) for each in actions] 
        avgs = [avgval(each, self.depth, 1) for each in successors]
##        print(max(mins))
        return actions[avgs.index(max(avgs))]



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    s = currentGameState
    pacPos = s.getPacmanPosition()
    foodList = s.getFood().asList()
    foodNum = s.getNumFood()
    ghostState = s.getGhostStates()
    
    scareTime = [gs.scaredTimer for gs in ghostState]
        
    distances = 0.0
    result = 0.0
    ghostPos = [each.getPosition() for each in ghostState]
    capsule = s.getCapsules()

    #Best and Worst
    if s.isLose():
        return -float("inf")
    elif s.isWin():
        return float("inf")
    #Close to ghost = very bad(if ghost not scared)
    distance = [manhattanDistance(pacPos, each) for each in ghostPos]
    
    if 0 in scareTime:
        result -= distance.count(1)*10000
        result -= distance.count(2)*5000


    #Eat capsule = Nice
    result -= len(capsule)*200
        
    #Eat food = Better
    result -= len(foodList)*100
    if len(foodList) == 0:
        return float("inf")
    #close to food = Better
    fooddistance = [manhattanDistance(pacPos, each) for each in foodList]
    for i in range(len(foodList)):
        result += 10/(fooddistance[i])
    if len(fooddistance):
        result += 50/(min(fooddistance))

    #close to capsule = Better
    for i in range(len(capsule)):
        result += 20/(manhattanDistance(pacPos, capsule[i]))
    

    return result




# Abbreviation
better = betterEvaluationFunction
