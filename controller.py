import holdem_model.table
from view import UIView
import random

class Controller:
    playerid = None
    model = None
    view = None
    
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
    
    def get_action(self):
        pass


class HumanController(Controller):
    playerid = None
    model = None
    view = None
    finished = False

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
                if self.model.to_call >= self.model.players[self.playerid]['chips']:
                    print("This would put you all-in. Is that okay? Type y/n.")
                    if input()[0] not in ['y','Y']:
                        continue  
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
            raise_amount = random.randint(min(self.model.min_bet, self.model.max_bet), self.model.max_bet)
            if raise_amount:
                return(self.model.bet(raise_amount))
            else:
                return(self.model.checkcall())

