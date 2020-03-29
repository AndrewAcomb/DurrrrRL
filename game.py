import random
import controller
import view
import holdem_model.table as table

class Game:
    controllers = None
    model = None

    def __init__(self, player1, player2, modeL_settings=None, show_output=False):
        # Initialize model without settings 
        if not modeL_settings:
            self.model = table.Table()

        self.controllers = {}
        if player1 == 'human':
            self.controllers[1] = controller.HumanController(self.model, self.model.players[1])

        else:
            self.controllers[1] = controller.RandomController(self.model, self.model.players[1], show_output)

        self.controllers[2] = controller.RandomController(self.model, self.model.players[2], False)

        if random.randint(0,1):
            self.model.move_blinds()


    def hand(self):
        # Preflop
        self.model.deal(to_players=True)

        for v in self.controllers.values():
            if v.view:
                v.view.view_cards()  

        allin = None

        # Get little blind, deael with blinds
        for v in self.controllers.values():
            if v.player.blind == self.model.little_blind:
                lb = v.player.playerid
            if v.player.chips > v.player.blind:
                v.player.chips -= v.player.blind
                v.player.chips_in += v.player.blind
            else:
                v.player.chips_in = v.player.blind
                v.player.chips = 0
                allin = True
        
        self.model.update_pot()
        #print(self.model.pot, self.model.players[1].chips_in, self.model.players[2].chips_in)

        if not allin:
            folded, allin = self.round_of_betting(lb, preflop=True)
            if folded:
                for v in self.controllers.values():
                    if v.view:
                        v.view.view_hand_results(None, folded)
                self.model.no_showdown(folded)
                return
        
        # Flop, River, Turn
        for _ in range(2):
            self.model.deal()

        for _ in range(3):
            self.model.deal()

            for v in self.controllers.values():
                if v.view:
                    v.view.view_cards()    

            if not allin:
                folded, allin = self.round_of_betting(lb)
                if folded:
                    for v in self.controllers.values():
                        if v.view:
                            v.view.view_hand_results(None, folded)
                    self.model.no_showdown(folded)
                    return
        
        # Showdown


        result = self.model.showdown()
        for v in self.controllers.values():
            if v.view:
                v.view.view_hand_results(result, None)
        return


    def round_of_betting(self, lb, preflop=False):

        # Lb is first to act preflop, then bb after (heads-up rules are weird)
        current = lb if preflop else self.model.opponent[lb]
        
        last_pot = self.model.pot
        last_action = 0

        to_call = self.model.get_to_call(current)
        result = self.controllers[current].get_action(to_call)
        self.model.update_pot()

        for v in self.controllers.values():
            if v.view:         
                v.view.view_player_action(current, last_pot, result, to_call)          

        if not result:
            return(self.model.opponent[current],False)

        current = self.model.opponent[current]
        last_action = result
        
        # Repeat as long as players reraise
        while True:
            to_call = self.model.get_to_call(current)
            result = self.controllers[current].get_action(to_call)

            last_pot = self.model.pot
            self.model.update_pot()

            # Display result
            for v in self.controllers.values():
                if v.view:         
                    v.view.view_player_action(current, last_pot, result, to_call)   


            # Player folded
            if not result:
                return(self.model.opponent[current],False)

            # Player called all-in
            elif result == 5:
                return(0, True)

            # Player did not raise
            elif result not in [3,4]:
                if last_action == 4:
                    return(0,True)
                return(0,False)

            # Player raised but other is all-in
            elif last_action == 4:
                return(0, True)

            last_action = result
            current = self.model.opponent[current]
            

        return(0,False)



    def play_game(self):
        
        loser = None
        while not loser:

            self.hand()

            for v in self.model.players.values():
                if v.chips == 0:
                    loser = v.playerid
        
        for v in self.controllers.values():
            if v.view:
                v.view.end_game(loser)
        
