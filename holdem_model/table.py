import random
from . import player, hands


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

    