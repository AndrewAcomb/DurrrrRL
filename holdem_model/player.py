class Player:
    playerid = -1
    chips = 200
    blind = 0
    hand = set({})
    next_player = None
    max_pot = 0
    folded = False

    def __init__(self,playerid, chips, blind=0):
        self.playerid = playerid
        self.chips = chips
        self.blind = blind
        self.hand = set({})
        self.folded = False

    def action(self, to_call, bet_amount):

        # Fold
        if bet_amount < min(self.chips,(to_call - self.max_pot)):
            self.folded = True
            return(0)

        # All-in
        elif bet_amount >= self.chips:
            allin = self.chips
            self.chips = 0
            self.max_pot += allin
            return(allin)

        # Call or non-all-in raise
        else:
            self.chips -= bet_amount
            self.max_pot += bet_amount
            return(bet_amount)


