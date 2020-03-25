import random
from . import player, rank_hands

class Table:
    players = None
    deck = [(i,j) for i in range(13) for j in range(4)]
    pots = [0]
    community_cards = set({})
    table_bet = 0
    num_players = 0
    players_in = 0
    
    def __init__(self, num_players=2, buy_in=200, little_blind=1, big_blind=2):

        assert (buy_in >= 10 * big_blind), "Initial stacks must be >= 10 big blinds"
        assert (num_players > 1 and num_players < 24), "There must be 2-23 players."
        assert (big_blind >= little_blind), "Big blind can't be < little blind."

        self.num_players = num_players

        # Create big and little blind players
        lb = player.Player(buy_in, little_blind)
        bb = player.Player(buy_in, big_blind)
        lb.next_player = bb
        last = bb

        # Create the rest of the players
        for _ in range(num_players - 2):
            temp = player.Player(buy_in)
            last.next_player = temp
            last = temp
        
        last.next_player = lb

        # Little Blind = head of circular linked list
        self.players = lb


    def deal(self, to_players=False):

        if not to_players:
            self.community_cards.add(self.deck.pop())
            return

        # Shuffle the deck
        random.shuffle(self.deck)
    
        num_cards = 2 * self.num_players
        k = self.players

        while num_cards:
            # Deal player 2 cards
            k.hand.add(self.deck.pop())
            k.hand.add(self.deck.pop())
            k = k.next_player

    def remove_player(self, player):
        if self.players is player:
            self.players = player.next_player

        last = player
        while last.next_player != player:
            last = last.next_player
        last.next_player = player.next_player

        if player.blind > 0:
            if player.next_player.blind > 0:
                last.blind = player.blind
            else:
                player.next_player.blind = player.blind


    def showdown(self):
        current = self.players
        hole_dict = {}
        pot_eligibility = {}
        player_dict = {}

        for i in range(self.players_in):
            while current.max_pot < 0:
                current = current.next_player
            hole_dict[i] = current.hand
            pot_eligibility[i] = current.max_pot
            player_dict[i] = current

            current = current.next_player

        hand_ranks = rank_hands.rank_hands(hole_dict, self.community_cards)
        
        winnings = {x:0 for x in pot_eligibility}

        while hand_ranks and self.pots != [0] * len(self.pots):

            split = {x: set({}) for x in range(len(self.pots))}
            best = [(pot_eligibility[b], b) for b in hand_ranks.pop()]

            for p in best:
                for i in range(p[0] + 1):
                    if self.pots[i]:
                        split[i].add(p[1])

            for s in split:
                if split[s]:
                    payout = self.pots[s] // len(split[s])
                    for p in split[s]:
                        winnings[p] += payout

        for p in player_dict:
            player_dict[p].chips += winnings[p]
            if player_dict[p].chips == 0:
                self.remove_player(player_dict[p])
        