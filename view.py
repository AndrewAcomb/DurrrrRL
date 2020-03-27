from holdem_model import table

class View:
    model = None
    playerid = 0

    def __init__(self, model, playerid):
        self.model = model
        self.playerid = playerid

    def show_player_action(self, pid, prev_pot, to_call, action):
        pass

    def show_model_state(self):
        pass

    def show_showdown_results(self):
        pass

    def show_history(self):
        pass


class UIView(View):
    model = None
    playerid = 0

    def card_to_string(self, card):
        pass

    def show_model_state(self):
        pass

    def show_showdown_results(self):
        pass

    def show_history(self):
        pass


    def show_player_action(self, pid, prev_pot, to_call, action):
        actions = ['folds', 'checks', 'calls', 'raises', 'goes all-in']
        you = ' (You)' if pid == self.playerid else ''
        if action < 2:
            print("Player {}{} {}.".format(pid, you, actions[action]))
        else: 
            amount = self.model.players_dict[pid].chips_in - prev_pot
            print("Player {}{} {} for {}.".format(pid, you, actions[action], amount))
        



