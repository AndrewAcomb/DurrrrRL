class Player:
    playerid = -1
    chips = 200
    blind = 0
    hand = set({})
    next_player = None
    chips_in = 0
    folded = False

    def __init__(self,playerid, chips, blind=0):
        self.playerid = playerid
        self.chips = chips
        self.blind = blind
        self.hand = set({})
        self.folded = False

    def action(self, to_call, bet_amount):

        # Fold
        if bet_amount < to_call:
            self.folded = True
            return(0)

        # All-in
        elif bet_amount >= self.chips:
            allin = self.chips
            self.chips = 0
            self.chips_in += allin
            if to_call >= allin:
                return(5)
            return(4)

        # Call or non-all-in raise
        else:
            self.chips -= bet_amount
            self.chips_in += bet_amount
            # Raise
            if bet_amount - to_call:
                return(3)
            # Call
            elif to_call:
                return(2)
            # Check
            else:
                return(1)


