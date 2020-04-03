import holdem_model.table, holdem_model.utils as utils
from view import UIView, AgentView
from itertools import combinations
import random, json

class Controller:
    playerid = None
    model = None
    view = None
    public = None
    
    def __init__(self, model, playerid, show_output):
        self.playerid = playerid
        self.model = model

        if show_output:
            self.view = UIView(model, playerid)

    def get_action(self):
        pass


class AgentController(Controller):
    playerid = None
    model = None
    view = None

    def __init__(self,model, playerid):
        self.playerid = playerid
        self.model = model
        self.view = AgentView(model, playerid)
        with open('matchups.json') as matchups:
            self.matchups = eval(matchups.read())

    
    def predict_opponent_cards(self):
        # TODO
        return([1/1326]*1326)

    def predict_fold_chance(self, bet):
        # TODO
        chance = bet/(2*self.model.max_bet) if self.model.max_bet else 0
        return(chance)


    def get_action(self):
        deck = {(i,j) for i in range(13) for j in range(4)} - self.model.players[self.playerid]['hand'] - self.model.community_cards
        hands = combinations(deck, 2)

        opp_pred = self.predict_opponent_cards()
        
        scores = []
        probs = []
        bet_evs = [[] for _ in range(self.model.min_bet, self.model.max_bet + 1)]

        # For each possible opposing hand    
        for h in hands:
            
            # Get the probability of them having it
            idx = 52*utils.card_to_int(h[0]) - sum([i for i in range(utils.card_to_int(h[0]) + 1)]) + (utils.card_to_int(h[1]) - utils.card_to_int(h[0]) - 1)
            probs.append(opp_pred[idx])

            # Get pot equity    
            if self.model.community_cards:
                pot_equity = utils.get_pot_equity(deck - set(h),
                 self.model.players[self.playerid]['hand'], set(h), self.model.community_cards)
            else:
                pot_equity = self.matchups[utils.encode_hole_cards(self.model.players[self.playerid]['hand'])][utils.encode_hole_cards(set(h))]
                pot_equity /= 100
            
            scores.append(pot_equity)

            # Get EVs of possible bets
            for bet in range(self.model.min_bet, self.model.max_bet + 1):
                fold_chance = self.predict_fold_chance(bet)
                bet_evs[bet - self.model.min_bet].append(utils.get_bet_ev(self.model.to_call, fold_chance, pot_equity, self.model.pot, bet))
        
        # Normalize probabilities, calculate expected pot equity
        probs = [p / sum(probs) for p in probs]
        pot_equity = sum([scores[i] * probs[i] for i in range(len(probs))])

        # Calculate EV fold: 100% to lose existing equity
        ev_fold = -1 * pot_equity * self.model.pot

        # Calculate EV check/call: Positive if equity > 0.5
        ev_checkcall = (2 * self.model.to_call * pot_equity) - self.model.to_call
        
        # Calculate EV raise, optimal bet size
        optimal_bet = 0
        bets = []
        ev_raise = -2 * self.model.pot
        for i in range(len(bet_evs)):
            b = sum([bet_evs[i][j] * probs[j] for j in range(len(probs))])
            bets.append(b)
            if b > ev_raise:
                ev_raise = b
                optimal_bet = i
        
        # Choose best option
        actions = [ev_fold, ev_checkcall, ev_raise]
        best = ev_checkcall
        best_action = 1
        for i in range(3):
            if actions[i] > best:
                best = actions[i]
                best_action = i

        # print(pot_equity)
        # print({"fold":ev_fold, "checkcall":ev_checkcall, "raise":ev_raise})

        if best_action == 0:
            return(self.model.fold())
        
        elif best_action == 1:
            return(self.model.checkcall())
        
        else:            
            return(self.model.bet(optimal_bet + self.model.min_bet))
        



class HumanController(Controller):
    playerid = None
    model = None
    view = None

    def __init__(self, model, playerid):
        self.playerid = playerid
        self.model = model
        self.view= UIView(model, playerid)

    def help(self):
        print("Valid commands: 'fold', 'call', 'check', 'raise x', 'view cards', 'view chips'")
        print("'raise' must be followed by a value you want to raise by.")
        print("To go all-in, enter 'raise allin'")
        print("To see your cards, 'view cards'. To see your chips and the pot, 'view chips'")
        print("Type 'exit' to quit the game.")


    def use_view(self, what):
        if what == 'cards':
            self.view.view_cards()
        elif what == 'chips':
            self.view.view_chips()
        else:
            print("You must specify: 'view cards' or 'view chips'")
        return

        

    def get_action(self):
        #valid_actions = ['help','fold','call', 'check', 'bet', 'raise', 'see', 'view', 'exit']

        print("Your turn!")
        if self.model.to_call:
            print("The current bet is {}.".format(self.model.to_call))
            if self.model.to_call >= self.model.players[self.playerid]['chips']:
                print("You may fold or call. The latter will put you all-in.")
            else:
                print("You may 'fold', 'call', or 'raise x'.")
        else:
            print("The current bet is 0. You may 'check' or 'raise x'")
        print("Type 'help' for help.")
    

        while True:
            response = input().split()
            if not response:
                print("You must enter an action.")
                continue

            action = response[0]
            value = response[1] if len(response) > 1 else None
            
            if action == 'help':
                self.help()

            elif action in ['see','view']:
                self.use_view(value)

            elif action == 'fold':
                if not self.model.to_call:
                    print("The current bet is 0. Checking instead.")
                    return(self.model.checkcall())
                else:
                    return(self.model.fold())

            elif action == 'call':
                return(self.model.checkcall())

            elif action == 'check':
                if self.model.to_call:
                    print("Cannot check when there is a bet of {}.".format(self.model.to_call))
                else:
                    return(self.model.checkcall())

            elif action in ['bet','raise']:
                if value:
                    value = int(value)
                if value and value <= min(self.model.max_bet,
                 self.model.players[self.playerid]['chips'] - self.model.to_call) and value >= min(self.model.min_bet, self.model.max_bet):
                    return(self.model.bet(value))
                else:
                    print("You must specify an amount to bet between {} and {}.".format(min(self.model.min_bet, self.model.max_bet),
                    min(self.model.max_bet,
                 self.model.players[self.playerid]['chips'] - self.model.to_call)))

            elif action == 'exit':
                exit()

            else:
                print("Invalid action. Type 'help' for help.")

            

class RandomController(Controller):
    playerid = None
    model = None

    def get_action(self):
        # Equal chance to call, raise, or fold.

        decision = random.randint(0,2)

        if not decision:
            return(self.model.fold())
        elif decision == 1:
            return(self.model.checkcall())
        else:
            if self.model.max_bet - self.model.min_bet:
                raise_amount = random.randint(self.model.min_bet, self.model.max_bet)  
            else:
                raise_amount =  self.model.max_bet                
            if raise_amount:
                return(self.model.bet(raise_amount))
            else:
                return(self.model.checkcall())


class OmniscientController(Controller):
    playerid = None
    model = None

    def __init__(self,model, playerid):
        self.playerid = playerid
        self.model = model
        with open('matchups.json') as matchups:
            self.matchups = eval(matchups.read())

    def get_action(self):
        
        myhand = self.model.players[self.playerid]['hand']
        opphand = self.model.players[1 - self.playerid]['hand']

        #print("Cheater: {}, Player: {}".format(myhand,opphand))
        
        if self.model.community_cards:
            pot_equity = utils.get_pot_equity(self.model.deck, myhand, opphand, self.model.community_cards)
        else:
            pot_equity = self.matchups[utils.encode_hole_cards(myhand)][utils.encode_hole_cards(opphand)]
            pot_equity /= 100

        if pot_equity <= 0.5:
            if self.model.to_call <= pot_equity * (self.model.pot + self.model.to_call):
                return(self.model.checkcall())
            else:
                return(self.model.fold())
        else:
            if not self.model.max_bet:
                return(self.model.checkcall())
            confidence = (pot_equity - 0.5)/0.5
            optionsrange = self.model.max_bet - self.model.min_bet
            if not optionsrange:
                return(self.model.bet(self.model.max_bet))
            else:
                return(self.model.bet(int(self.model.min_bet + (confidence * optionsrange))))
