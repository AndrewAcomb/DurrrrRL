import random
from . import player, rank_hands

class Table:
    players = None
    players_dict = {}
    deck = [(i,j) for i in range(13) for j in range(4)]
    pots = [0]
    community_cards = set({})
    table_bet = 0
    num_players = 0
    players_in = 0
    
    def __init__(self, num_players=2, buy_in=200, little_blind=1, big_blind=2):

        self.num_players = num_players

        # Create big and little blind players
        lb = player.Player(0, buy_in, little_blind)
        self.players_dict[0] = lb
        bb = player.Player(1, buy_in, big_blind)
        self.players_dict[1] = bb
        lb.next_player = bb
        last = bb

        # Create the rest of the players
        for i in range(2, num_players):
            temp = player.Player(i, buy_in)
            self.players_dict[i] = temp
            last.next_player = temp
            last = temp
        
        last.next_player = lb


    def deal(self, to_players=False, deterministic=False):

        if not to_players:
            self.community_cards.add(self.deck.pop())
            return

        # Shuffle the deck
        if not deterministic:
            random.shuffle(self.deck)
    
        num_cards = 2 * self.num_players
        k = self.players

        while num_cards:
            # Deal player 2 cards
            k.hand.add(self.deck.pop())
            k.hand.add(self.deck.pop())
            k = k.next_player


    def sidepot(self, round_results):
        # round_results is a dictionary with each player's bet for the round

        unique_amounts = set({})
        new_sidepots = []
        for p in round_results.values():
            if p:
                new_sidepots.append(p)
                unique_amounts.add()
        new_sidepots.sort()
        

        # Update max_pot for non-folded players
        unique_amounts = sorted(list(unique_amounts))
        for p in round_results:
            if self.players_dict[p].max_pot == -1:
                continue
            for i in range(len(unique_amounts)):
                if unique_amounts[i] == round_results[p]:
                    self.players_dict[p].max_pot += i + 1
                    break

        result_sidepots = []

        for i in range(len(new_sidepots) - 1):
            subtotal = 0
            if not new_sidepots[i]:
                continue

            for j in range(i+1, len(new_sidepots)):
                new_sidepots[j] -= new_sidepots[i]
                subtotal += new_sidepots[i]

            result_sidepots.append(new_sidepots[i] + subtotal)

        self.pots.extend(result_sidepots)

    def remove_player(self, pid):
        player = self.players_dict[pid]

        last = player
        while last.next_player != player:
            last = last.next_player
        last.next_player = player.next_player

        if player.blind > 0:
            if player.next_player.blind > 0:
                last.blind = player.blind
            else:
                player.next_player.blind = player.blind

        self.num_players -= 1
        del(self.players_dict[pid])


    def showdown(self):
        hole_dict = {}
        pot_eligibility = {}

        for v in self.players_dict.values():
            if v.max_pot < 0:
                continue
            hole_dict[v.playerid] = v.hand
            pot_eligibility[v.playerid] = v.max_pot

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

        for p in self.players_dict:
            if self.players_dict[p].max_pot < 0:
                continue

            self.players_dict[p].chips += winnings[p]
            if self.players_dict[p].chips == 0:
                self.remove_player(p)
        