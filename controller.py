from holdem_model import table
from view import UIView
import random

class Controller:
    player = None
    model = None
    view = None
    
    def __init__(self, model, player, show_output):
        self.player = player
        self.model = model

        if show_output:
            self.view = UIView(model, player.playerid)

    def get_action(self):
        pass


class AgentController(Controller):
    player = None
    model = None
    view = None
    
    def get_action(self):
        pass


class HumanController(Controller):
    player = None
    model = None
    view = None
    finished = False

    def __init__(self, model, player):
        self.player = player
        self.model = model
        self.view= UIView(model, player.playerid)
        self.finished = True

    def help(self):
        print("Valid commands: 'fold', 'call', 'check', 'raise x', 'view cards', 'view chips'")
        print("'raise' must be followed by a value you want to raise by.")
        print("To go all-in, enter 'raise allin'")
        print("To see your cards, 'view cards'. To see your chips and the pot, 'view chips'")
        print("Type 'exit' to quit the game.")

    def fold(self, to_call):
        if not to_call:
            print("The current bet is 0. Checking instead.")
        self.finished = True
        return(self.player.action(to_call, 0))

    def use_view(self, what, to_call):
        if what == 'cards':
            self.view.view_cards()
        elif what == 'chips':
            self.view.view_chips(to_call)
        else:
            print("You must specify: 'view cards' or 'view chips'")

        return
            

    def call(self, to_call, check=False):
        if check and to_call:
            print("Cannot check when there is a bet of {}.".format(to_call))
            return

        elif to_call >= self.player.chips:
            print("This would put you all-in. Is that okay? Type y/n.")
            if input()[0] in ['y','Y']:
                self.finished = True
                return(self.player.action(to_call, self.player.chips))
            else:
                return

        self.finished = True
        return(self.player.action(to_call, to_call))


    def bet(self, to_call, amount):
        if amount == None:
            print("You must specify an amount to bet.")
            return
        

        self.finished = True
        if amount == 'allin':
            return(self.player.action(to_call, self.player.chips))
        
        elif not amount.isdigit():
            print("You must specify an numeric amount to bet, or exactly 'raise allin'")
            return

        elif int(amount) > self.player.chips:
            print("This would put you all-in. Is that okay? Type y/n.")
            if input()[0] in ['y','Y']:
                return(self.player.action(to_call, self.player.chips))
            else:
                self.finished = False
                return
        else:
            return(self.player.action(to_call, int(amount) + to_call))

        

    def get_action(self, to_call):
        #valid_actions = ['help','fold','call', 'check', 'bet', 'raise', 'see', 'view', 'exit']
        result = None
        self.finished = False

        print("Your turn!")
        if to_call:
            print("The current bet is {}.".format(to_call))
            if to_call >= self.player.chips:
                print("You may fold or call. The latter will put you all-in.")
            else:
                print("You may 'fold', 'call', or 'raise x'.")
        else:
            print("The current bet is 0. You may 'check' or 'raise x'")
        print("Type 'help' for help.")
    

        while not self.finished:
            response = input().split()
            if not response:
                print("You must enter an action.")
                continue
            action = response[0]
            value = response[1] if len(response) > 1 else None
            
            if action == 'help':
                self.help()
            elif action in ['see','view']:
                self.use_view(value, to_call)
            elif action == 'fold':
                result = self.fold(to_call)
            elif action == 'call':
                result = self.call(to_call)
            elif action == 'check':
                result = self.call(to_call, check=True)
            elif action in ['bet','raise']:
                result = self.bet(to_call, value)
            elif action == 'exit':
                exit()
            else:
                print("Invalid action. Type 'help' for help.")
                

        return(result)
            

class RandomController(Controller):
    player = None
    model = None

    def get_action(self, to_call):
        # Equal chance to call, raise, or fold.

        decision = random.randint(0,2)

        if not decision:
            result = self.player.action(to_call, 0)
        elif decision == 1:
            result = self.player.action(to_call, to_call)
        else:
            if to_call >= self.player.chips:
                result = self.player.action(to_call, self.player.chips)
            else:
                raise_amount = random.randint(to_call, self.player.chips)
                result = self.player.action(to_call, raise_amount)

        return(result)