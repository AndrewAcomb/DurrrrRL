import holdem_model.table as table,  holdem_model.utils as utils

class View:
    model = None
    playerid = 0

    def __init__(self, model, playerid):
        self.model = model
        self.playerid = playerid

    def view_player_action(self, pid, prev_pot, to_call, action):
        pass

    def view_hand_results(self):
        pass

    def view_history(self):
        pass



class AgentView(View):
    model = None
    playerid = 0

    def view_model_state(self):
        pass

    def view_hand_results(self):
        pass

    def view_history(self):
        pass

    def show_player_action(self, pid, prev_pot, to_call, action):
        pass



class UIView(View):
    model = None
    playerid = 0

    def view_cards(self):
        if not self.model.community_cards:
            print("\nRound: Preflop")
            if self.model.players[self.playerid]['position']:
                print("You are the big blind ({})".format(self.model.blinds[1]))
            else:
                print("You are the little blind ({})".format(self.model.blinds[0]))
        
        elif len(self.model.community_cards) == 3:
            print("\nRound: Flop")
        
        elif len(self.model.community_cards) == 4:
            print("\nRound: Turn")

        elif len(self.model.community_cards) == 5:
            print("\nRound: River")

        else:
            print("Error!")


        hand = self.model.players[self.playerid]['hand']
        print('Hand: ' + ' '.join([utils.card_to_string(card) for card in hand]))

        print('Community: ' + ' '.join([utils.card_to_string(card) for card in self.model.community_cards]))    
        best = utils.get_rank(self.playerid, hand, self.model.community_cards)   
        print("The best hand you currently have is {}".format(utils.hand_to_string(best[1])))


    def view_chips(self):
        c1 = self.model.players[self.playerid]['chips']
        c2 = self.model.players[1 - self.playerid]['chips']

        if self.model.players[self.playerid]['position']:
            blind = 'big'
            b = self.model.blinds[1]
        else:
             blind = 'little'
             b = self.model.blinds[0]

        print("Pot: {}. The current bet is {}.".format(self.model.pot, self.model.to_call))
        if c2:
            print("You have {} chips. Opponent has {}.".format(c1,c2))
        else:
            print("You have {} chips. Opponent is all-in.".format(c1))
        print("You are the {} blind ({})".format(blind, b))


    def view_hand_results(self, result=None):
        if result:
            print("\nRound: Showdown")
            print('Community cards: ' + ' '.join([utils.card_to_string(card) for card in result[4]]))
            print('Your cards: ' + ' '.join([utils.card_to_string(card) for card in result[2]]))
            print("Opponent's cards: " + ' '.join([utils.card_to_string(card) for card in result[3]]))

        if not result:
            if self.model.active_player == self.playerid:
                print("Your opponent folded. You win the pot of {}".format(self.model.pot))
            else:
                print("You folded. Your opponent wins the pot of {}".format(self.model.pot))
                
        elif len(result) == 7:
            loser = utils.hand_to_string(result[0][1])
            winner = utils.hand_to_string(result[1][1])
            if result[6] == self.playerid:
                print("You have {} and your opponent has {}. You win the pot of {}".format(winner,loser, result[5]))
            else:
                print("You have {} and your opponent has {}. Your opponent wins the pot of {}".format(loser,winner, result[5]))
        else:
            print("You and your opponent each have {} and split the pot of {}".format(utils.hand_to_string(result[0][1]), result[5]))


    def view_player_action(self, action):
        actions = ['folds', 'checks', 'calls', 'raises by']
        you = ' (You)' if self.model.active_player != self.playerid else ''
        if action < 3:
            print("Player {}{} {}.".format(1 - self.model.active_player, you, actions[action]))
        else:
            print("Player {}{} {} {}.".format(1 - self.model.active_player, you, actions[action], self.model.to_call))
        

    def end_game(self, pid):
        if pid == self.playerid:
            print("You win!")
        else:
            print("You lose!")

    
    def view_history(self):
        pass

