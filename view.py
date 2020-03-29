from holdem_model import table, rank_hands

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


class UIView(View):
    model = None
    playerid = 0

    def card_to_string(self, card):
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        suits = ["D", "C", "H", "S"]
        return(values[card[0]] + suits[card[1]])

    def hand_to_string(self, result):
        hands = ["a high card", "a pair", "two pair", "three of a kind", "a straight",
         "a flush", "a full house", "four of a kind", "a straight flush"]
        return(hands[result])

    def view_cards(self):
        if not self.model.community_cards:
            print("\nRound: Preflop")
            if self.model.players[self.playerid].blind == self.model.little_blind:
                print("You are the little blind ({})".format(self.model.little_blind))
            else:
                print("You are the big blind ({})".format(self.model.big_blind))
            
        
        elif len(self.model.community_cards) == 3:
            print("\nRound: Flop")
        
        elif len(self.model.community_cards) == 4:
            print("\nRound: Turn")

        elif len(self.model.community_cards) == 5:
            print("\nRound: River")

        else:
            print("Error!")

        hand = self.model.players[self.playerid].hand
        print('Hand: ' + ' '.join([self.card_to_string(card) for card in hand]))
        if True:#self.model.community_cards:
            print('Community: ' + ' '.join([self.card_to_string(card) for card in self.model.community_cards]))    
            best = rank_hands.get_rank(self.playerid, hand, self.model.community_cards)   
            print("The best hand you currently have is {}".format(self.hand_to_string(best[1])))

    def view_chips(self, to_call):
        for k,v in self.model.players.items():
            if k == self.playerid:
                c1 = v.chips
                b1 = v.blind
            else:
                c2 = v.chips
                b2 = v.blind
        blind = 'little' if b1 < b2 else 'big'
        print("Pot: {}. The current bet is {}.".format(self.model.pot, to_call))
        if c2:
            print("You have {} chips. Opponent has {}.".format(c1,c2))
        else:
            print("You have {} chips. Opponent is all-in.".format(c1))
        print("You are the {} blind ({})".format(blind, b1))

    def view_hand_results(self, result=None, fold=None):

        if result:
            print("\nRound: Showdown")
            print('Community cards: ' + ' '.join([self.card_to_string(card) for card in result[2]]))
            print('Your cards: ' + ' '.join([self.card_to_string(card) for card in result[3]]))
            print("Opponent's cards: " + ' '.join([self.card_to_string(card) for card in result[4]]))

        if fold:
            if fold != self.playerid:
                print("You folded. Your opponent wins the pot of {}".format(self.model.pot))
            else:
                print("Your opponent folded. You win the pot of {}".format(self.model.pot))
        elif len(result[0]) == 2:
            loser = self.hand_to_string(result[0][0][1])
            winner = self.hand_to_string(result[0][1][1])
            if result[0][1][0] == self.playerid:
                print("You have {} and your opponent has {}. You win the pot of {}".format(winner,loser, result[1]))
            else:
                print("You have {} and your opponent has {}. Your opponent wins the pot of {}".format(loser,winner, result[1]))
        else:
            print("You and your opponent each have {} and split the pot of {}".format(self.hand_to_string(result[0][1]), result[1]))

    def view_player_action(self, pid, prev_pot, action, to_call):
        actions = ['folds', 'checks', 'calls', 'raises by', 'goes all-in for', 'calls all-in for']
        you = ' (You)' if pid == self.playerid else ''
        if action < 3:
            print("Player {}{} {}.".format(pid, you, actions[action]))
        else: 
            amount = self.model.pot - prev_pot - to_call
            print("Player {}{} {} {}.".format(pid, you, actions[action], amount))
        
    def end_game(self, pid):
        if pid == self.playerid:
            print("You lose!")
        else:
            print("You win!")
    
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