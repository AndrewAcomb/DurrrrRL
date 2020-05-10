import random
from . import utils

class Table:
    players = {}
    deck = []
    pot = 0
    community_cards = set({})
    blinds = []
    active_player = 1
    to_call = 0
    min_bet = 0
    max_bet = 0
    all_in = False
    winner = None
    
    def __init__(self, buy_in=100, little_blind=1, big_blind=2):
        self.deck = [(i,j) for i in range(13) for j in range(4)]
        self.community_cards = set({})
        self.players = {}
        self.pot = 0
        self.blinds = (little_blind, big_blind)

        # Create players
        self.players[0] = {"id": 0, "chips": buy_in, "position": 0, "chips_in": 0, "hand": set({}), "opponent": 1}
        self.players[1] = {"id": 1, "chips": buy_in, "position": 1, "chips_in": 0, "hand": set({}), "opponent": 0}


    def deal(self, to_players=False):
        if to_players:
            random.shuffle(self.deck)
            for p in self.players:
                self.players[p]['hand'].add(self.deck.pop())
                self.players[p]['hand'].add(self.deck.pop())
        else:
            self.community_cards.add(self.deck.pop())            


    def fold(self):
        return(0)


    def checkcall(self):
        if self.to_call:
            self.players[self.active_player]['chips'] -= self.to_call
            self.players[self.active_player]['chips_in'] += self.to_call
            if not self.players[self.active_player]['chips']:
                self.all_in = True
            return(2)
        else:
            return(1)

    def bet(self, value):
        self.min_bet = value

        self.players[self.active_player]['chips'] -= self.to_call + value
        self.players[self.active_player]['chips_in'] += self.to_call + value
        if not self.players[self.active_player]['chips']:
            self.all_in = True
        return(3)


    def resolve_hand(self, folded=None):
        # To be called when a player folds, or on showdown
        # Rank hands if showdown
        if folded == None:
            rankings = [utils.get_rank(v['id'], v['hand'], self.community_cards) for v in self.players.values()]
            rankings.sort(key=lambda x: (x[1], x[2]))
            results = rankings + [self.players[0]['hand'], self.players[1]['hand']]
            results += [self.community_cards, self.pot]
            if rankings[0][1] == rankings[1][1] and rankings[0][2] == rankings[1][2]:
                for v in self.players.values():
                    v['chips'] += v['chips_in']
            else:
                self.players[rankings[1][0]]['chips'] += self.pot
                results.append(rankings[1][0])

        else:
            self.players[1 - folded]['chips'] += self.pot
    
        # Reset hands, deck, and chips in the pot. Check for winner.
        self.deck = [(i,j) for i in range(13) for j in range(4)]
        self.community_cards = set({})
        for v in self.players.values():
            v['hand'] = set({})
            v['chips_in'] = 0
            if not v['chips']:
                self.winner = 1 - v['id']

        self.all_in = False
        self.update_state()
        self.move_blinds()
        self.min_bet = min(self.blinds[1], self.max_bet)
        if folded == None:
            return(results)


    def update_state(self):
        # To be called after each action

        self.to_call = self.players[self.active_player]['chips_in'] -  self.players[1 - self.active_player]['chips_in']
        self.max_bet = min(self.players[self.active_player]['chips'],
         self.players[1 - self.active_player]['chips'] - self.to_call)

        self.min_bet = min(self.min_bet, self.max_bet)
        self.pot = self.players[self.active_player]['chips_in'] + self.players[1 - self.active_player]['chips_in']
        self.active_player = 1 - self.active_player


    def move_blinds(self):
        # To be called after each hand
        for v in self.players.values():
            v['position'] = 1 - v['position']
            if v['position']: self.active_player = v['id']
