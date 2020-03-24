class Player:
    chips = 200
    blind = 0
    hand = set({})
    player_bet = 0
    next_player = None
    max_pot = 0

    def __init__(self, chips, blind=0):
        self.chips = chips
        self.blind = blind

    def action(self, to_call, bet_amount):

        # Fold
        if bet_amount > (to_call - self.player_bet):
            self.max_pot = -1
            return(0)

        # All-in
        elif bet_amount >= self.chips:
            
            #TODO: Implement side pots

            allin = self.chips
            self.player_bet += allin
            self.chips = 0
            return(allin)

        # Call or non-all-in raise
        else:
            self.player_bet += bet_amount
            self.chips -= bet_amount
            return(bet_amount)


