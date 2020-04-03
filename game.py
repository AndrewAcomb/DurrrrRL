import random
import controller
import view
import holdem_model.table as table

class Game:
    controllers = None
    model = None

    def __init__(self, players, modeL_settings=None, show_output=False):
        # Initialize model without settings 
        if not modeL_settings:
            self.model = table.Table()

        self.controllers = {}
        for i in range(2):
            if players[i] == 'human':
                self.controllers[i] = controller.HumanController(self.model, i)

            elif players[i] == 'random':
                self.controllers[i] = controller.RandomController(self.model, i, show_output)
                show_output = False

            elif players[i] == 'agent':
                self.controllers[i] = controller.AgentController(self.model, i)

            elif players[i] == 'cheater':
                self.controllers[i] = controller.OmniscientController(self.model, i)
                
            else:
                self.controllers[i] = controller.RandomController(self.model, i, show_output)
                show_output = False            

        if random.randint(0,1):
            self.model.move_blinds()


    def hand(self):
        # Preflop
        self.model.deal(to_players=True)

        for v in self.controllers.values():
            if v.view:
                v.view.view_cards()  

        # Get little blind, deael with blinds

        for v in self.model.players.values():
            if v['chips'] > self.model.blinds[v['position']]:
                v['chips'] -= self.model.blinds[v['position']]
                v['chips_in'] += self.model.blinds[v['position']]
            else:
                v['chips_in'] = v['chips']
                v['chips'] = 0
                self.model.all_in = True        

        self.model.min_bet = self.model.blinds[1]
        self.model.update_state()

        if not self.model.all_in:
            folded = self.round_of_betting(preflop=True)
            if folded != None:
                for v in self.controllers.values():
                    if v.view:
                        v.view.view_hand_results()
                self.model.resolve_hand(folded)
                return
        
        # Flop, Turn, River
        for _ in range(2):
            self.model.deal()

        for _ in range(3):
            self.model.deal()

            for v in self.controllers.values():
                if v.view:
                    v.view.view_cards()    

            if not self.model.all_in:
                self.model.min_bet = self.model.blinds[1]
                folded = self.round_of_betting()
                if folded != None:
                    for v in self.controllers.values():
                        if v.view:
                            v.view.view_hand_results()
                    self.model.resolve_hand(folded)
                    return
        
        # Showdown
        results = self.model.resolve_hand()
        for v in self.controllers.values():
            if v.view:
                v.view.view_hand_results(results)
        return


    def round_of_betting(self, preflop=False):

        result = self.controllers[self.model.active_player].get_action()
        last_action = result
        self.model.update_state()

        for v in self.controllers.values():
            if v.view:         
                v.view.view_player_action(result)          

        if not result:
            return(1 - self.model.active_player)


        # Repeat as long as players reraise
        while True:

            result = self.controllers[self.model.active_player].get_action()
            self.model.update_state()

            # Display result
            for v in self.controllers.values():
                if v.view:         
                    v.view.view_player_action(result)   

            # Player folded
            if not result:
                return(1 - self.model.active_player)

            if result == 2 or (result == last_action and result == 1) or (result == 1 and preflop):
                return(None)

            last_action = result



    def play_game(self):
        a = 0
        while self.model.winner == None:
            self.hand()
            a += 1

        for v in self.controllers.values():
            if v.view:
                v.view.end_game(self.model.winner)
        
        return(a)

    def reset_game(self):
        self.model.players[0]['chips'] = self.model.players[1]['chips'] = self.model.players[self.model.winner]['chips'] // 2
        self.model.winner = None
        self.model.all_in = False
        self.model.active_player = 0
        self.model.update_state()
