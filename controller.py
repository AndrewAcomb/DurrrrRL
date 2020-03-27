from holdem_model import table
from view import UIView
import random

class Controller:
    player = None
    model = None
    
    def __init__(self, model, player):
        self.player = player
        self.model = model

    def get_action(self):
        pass


class AgentController(Controller):
    player = None
    model = None
    
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
        print("Valid commands: 'fold', 'call', 'check', 'raise x'")
        print("'raise' must be followed by a value you want to raise by.")
        print("To go all-in, enter 'raise allin'")
        return(False)

    def fold(self, to_call):
        self.finished = True
        return(self.player.action(to_call, 0))


    def call(self, to_call, check=False):
        if check and to_call:
            print("Cannot check when there is a bet of {}.".format(to_call))
            return

        self.finished = True
        return(self.player.action(to_call, to_call))


    def bet(self, to_call, amount):
        self.finished = True

        if amount == 'allin':
            return(self.player.action(to_call, self.player.chips))
        else:
            return(self.player.action(to_call, amount + to_call))

        

    def get_action(self):
        to_call = self.model.get_to_call(self.player.playerid)
        valid_actions = ['help','fold','call', 'check', 'raise']
        result = None
        self.finished = False

        print("Your turn!")
        if to_call:
            print("The current bet is {}.".format(to_call))
            if to_call >= self.player.chips:
                print("You may fold or call. The latter will put you all-in.")
            else:
                print("You may fold, call, or raise.")
        else:
            print("The current bet is 0. You may check or raise")
        print("Type 'help' for help.")
    

        while not self.finished:
            response = input().split()
            action = response[0]
            value = response[1] if len(response) > 1 else None
            
            if action not in valid_actions:
                print("Invalid action. Type 'help' for help.")
            
            if action == 'help':
                self.help()
            elif action == 'fold':
                result = self.fold(to_call)
            elif action == 'call':
                result = self.call(to_call)
            elif action == 'check':
                result = self.call(to_call, check=True)
            elif action in ['raise']:
                result = self.bet(to_call, value)
            else:
                print("\n\n\n")
            
            return(result)
            

class RandomController(Controller):
    player = None
    model = None

    def get_action(self):
        # Equal chance to call, raise, or fold.

        to_call = self.model.get_to_call(self.player.playerid)
        decision = random.randint(0,2)

        if not decision:
            self.player.action(to_call, 0)
        elif decision == 1:
            self.player.action(to_call, to_call)
        else:
            if to_call >= self.player.chips:
                self.player.action(to_call, self.player.chips)
            else:
                raise_amount = random.randint(to_call, self.player.chips)
                self.player.action(to_call, raise_amount)
