# DurrrrRL
Machine Learning agent for heads-up no-limit Texas Hold'em, and a minimalistic MVC implementation of Texas Hold'em 

The title of the project is a reference to professional poker player Tom Dwan's screen name, Durrrr. It is a bit of a misnomer since I ended up using supervised learning rather than reinforcement learning.


## table.py: 
Tmplementation of the heads-up no-limit Texas Hold'em game model


## game.py: 
Implementation of the game structure (rounds of betting, hands)


## heads_up.py: 
Argument parsing that allows game to be set up via CLI with user-specified player types


## utils.py
Implements various functions used by agents and other parts of the game


## controller.py:
Implements subclasses of the Controller class, each of which has its own get_action() function.

### HumanController 
Allows a person to play against an agent or other player through the command line.

### AgentController
The meat of this project, implements an algorithm that makes the agent play based on its prediction of its opponent's cards, and what it predicts it's opponent will do if it makes a given action (using the cards model and action model, respectively). This allows it to learn to read opponents, size bets appropriately, and even bluff and trap.

### RandomController
Agent that makes random moves. Mostly used to test table.py

### OmniscientController
Agent that cheats and sees its opponent's cards. Bets more aggressively when its EV is higher, folds when behind and facing a bet. Used to train the agent in the beginning to improve the baseline level of skill while playing against itself.


## view.py
Implements subclasses of the View class, each of which has its own view_player_action() and view_hand_results() functions.

### UIView
View for human player. Prints details of the state that they should be able to see (e.g, not their opponent's cards, not the deck) of the game to stdout.

### AgentView
View for the agent. Implements predict_cards() and predict_action() which are used by the AgentController to make its decisions. view_player_action() formats the state of the game into a history of the hand, which is used to in predict_cards() and predict_action(), and saved and used as training data after the hand is completed. The states of the game are used as training data to train the models during view_hand_results(), such that the model can dynamically learn the behaviors of the one player, then adjust while playing another.

