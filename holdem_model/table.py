import random
from . import player, rank_hands as rh

class Table:
    players = {}
    deck = []
    pot = 0
    community_cards = set({})
    table_bet = 0
    num_players = 0
    little_blind = 1
    big_blind = 2
    opponent = {}
    
    def __init__(self, num_players=2, buy_in=200, little_blind=1, big_blind=2):
        self.deck = [(i,j) for i in range(13) for j in range(4)]
        self.community_cards = set({})
        self.players = {}
        self.pot = 0
        self.num_players = num_players
        self.little_blind = little_blind
        self.big_blind = big_blind

        # Create big and little blind players
        lb = player.Player(1, buy_in, little_blind)
        self.players[1] = lb
        self.opponent[1] = 2
        bb = player.Player(2, buy_in, big_blind)
        self.players[2] = bb
        self.opponent[2] = 1
        lb.next_player = bb
        last = bb

        # # Create the rest of the players
        # for i in range(2, num_players):
        #     temp = player.Player(i, buy_in)
        #     self.players[i] = temp
        #     last.next_player = temp
        #     last = temp
        
        last.next_player = lb



    def deal(self, to_players=False, deterministic=False):

        if not to_players:
            self.community_cards.add(self.deck.pop())
            return

        # Shuffle the deck
        if not deterministic:
            random.shuffle(self.deck)
    
        for p in self.players.values():
            p.hand.add(self.deck.pop())
            p.hand.add(self.deck.pop())



    def showdown(self):
        hands = {}
        bets = []
        for k,v in self.players.items():
            hands[k] = v.hand
            bets.append((v.chips_in, k))

        # Deal with all-in
        bets.sort()
        if bets[1][0] > bets[0][0]:
            self.players[bets[1][1]].chips += bets[1][0] - bets[0][0]
            self.pot -= bets[1][0] - bets[0][0]


        # Rank hands, determine winner, and pay out
        rankings = sorted([v for v in rh.rank_hands(hands, self.community_cards).values()], key=lambda x: (x[1], x[2]))
        if rankings[0][1] == rankings[1][1] and rankings[0][2] == rankings[1][2]:
            for v in self.players.values():
                v.chips += v.chips_in
            result = [rankings[1], self.pot, self.community_cards, self.players[1].hand, self.players[2].hand]
        else:
            self.players[rankings[1][0]].chips += self.pot
            result = [rankings, self.pot, self.community_cards, self.players[1].hand, self.players[2].hand]

        # Reset chips in the pot
        for v in self.players.values():
            v.chips_in = 0
        self.pot = 0

        # Reset hands and deck
        self.deck = [(i,j) for i in range(13) for j in range(4)]
        self.community_cards = set({})
        for v in self.players.values():
            v.hand = set({})

        self.move_blinds()

        return(result)


    def no_showdown(self, playerid):

        # Pay out
        self.players[playerid].chips += self.pot
        self.pot = 0

        # Reset chips in
        for v in self.players.values():
            v.chips_in = 0

        # Reset hands and deck
        self.deck = [(i,j) for i in range(13) for j in range(4)]
        self.community_cards = set({})
        for v in self.players.values():
            v.hand = set({})

        self.move_blinds()



    def get_to_call(self, pid):
        return(self.players[self.opponent[pid]].chips_in - self.players[pid].chips_in)


    def move_blinds(self):
        for v in self.players.values():
            if v.blind == self.little_blind:
                v.blind = self.big_blind
            else:
                v.blind = self.little_blind


    def update_pot(self):
        newpot = 0
        for v in self.players.values():
            newpot += v.chips_in
        self.pot = newpot

    # def remove_player(self, pid):
    #     player = self.players[pid]

    #     # Remove player from circularly linked list
    #     last = player
    #     while last.next_player != player:
    #         last = last.next_player
    #     last.next_player = player.next_player

    #     # Ensure both blinds remain in play
    #     if player.blind > 0:
    #         if player.next_player.blind > 0:
    #             last.blind = player.blind
    #         else:
    #             player.next_player.blind = player.blind

    #     self.num_players -= 1
    #     del(self.players[pid])


    # def get_payouts(self):
        
    #     earnings = {}
    #     hands = {}
    #     allins = []
    #     main_pot = [0,set({}), 0]
    #     max_chips_in = max({v.chips_in for v in self.players.values()})

    #     for pid, p in self.players.items():
    #         earnings[pid] = 0
    #         hands[pid] = p.hand
    #         main_pot[2] += p.chips_in
    #         if p.folded: 
    #             continue

    #         if p.chips == 0 and p.chips_in < max_chips_in:
    #             allin = [p.chips_in, set({}), 0]
    #             if allin not in allins:
    #                 allins.append(allin)
    #         else:
    #             main_pot[1].add(pid)
        
    #     allins.sort(key=lambda x: x[0])

    #     for i in range(len(allins)):
    #         for pid, p in self.players.items():
    #             if not p.chips_in:
    #                 continue
    #             elif p.chips_in < allins[i][0]:
    #                 # must be folded
    #                 allins[i][2] += p.chips_in
    #                 p.chips_in = 0
    #             else:
    #                 allins[i][2] += allins[i][0]
    #                 p.chips_in -= allins[i][0]
    #                 allins[i][1].add(pid)

    #         for j in range(i+1, len(allins)):
    #             allins[j][0] -= allins[i][0]

    #         main_pot[2] -= allins[i][2]

    #     rankings = rh.rank_hands(hands, self.community_cards)
    #     allins.append(main_pot)

    #     for pot in allins:
    #         pot_ranks = []

    #         # get and sort pot_ranks, the ranks of those eligible to win the pot
    #         for p, r in rankings.items():
    #             if p not in pot[1] or self.players[p].folded: 
    #                 continue
    #             pot_ranks.append(r)
    #         pot_ranks.sort(key=lambda x: (x[1],x[2]), reverse=True)

    #         # Split contains the ids of all the winners of the pot
    #         winning_rank = pot_ranks.pop(0)
    #         split = [winning_rank[0]]

    #         if pot_ranks:
    #             for pr in pot_ranks:
    #                 if pr[1] == winning_rank[1] and pr[2] == winning_rank[2]:
    #                     split.append(pr[0])
    #                 else:
    #                     break
            
    #         sp = pot[2]
    #         rem = sp % len(split)

    #         for p in split:
    #             earnings[p] += (sp - rem) // len(split)
    #         if rem:
    #             for p in split:
    #                 earnings[p] += 1
    #                 rem -= 1
    #                 if not rem: break

    #     return(earnings)



    # def showdown(self):
        
    #     # Determine winners and distribute payouts
    #     payouts = self.get_payouts()
    #     for p in payouts:
    #         self.players[p].chips += payouts[p]


    #     # Reset hands and deck
    #     self.deck = [(i,j) for i in range(13) for j in range(4)]
    #     self.community_cards = set({})

    #     out_players = []
    #     for k, v in self.players.items():
    #         v.chips_in = 0
    #         if v.chips == 0:
    #             out_players.append(k)
    #         v.hand = set({})
    #         v.folded = False


    #     # Remove players who are out of chips
    #     for o in out_players:
    #         self.remove_player(o)


    #     # Move the blinds
    #     if self.num_players < 2: return(True)
    #     current = self.players[max(self.players)]

    #     for _ in range(self.num_players):
    #         if current.blind != self.little_blind:
    #             current = current.next_player

    #     hold = current.blind
    #     current.next_player.next_player.blind = current.next_player.blind
    #     current.next_player.blind = hold

    #     return(False)
