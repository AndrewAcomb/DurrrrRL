import random
from . import player, rank_hands as rh

class Table:
    players_dict = {}
    deck = []
    pot = 0
    community_cards = set({})
    table_bet = 0
    num_players = 0
    players_in = 0
    
    def __init__(self, num_players=2, buy_in=200, little_blind=1, big_blind=2):
        self.deck = [(i,j) for i in range(13) for j in range(4)]
        self.community_cards = set({})
        self.players_dict = {}
        self.pot = 0
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
    
        for p in self.players_dict.values():
            p.hand.add(self.deck.pop())
            p.hand.add(self.deck.pop())



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
        
        earnings = {}
        hands = {}
        allins = []
        main_pot = [0,set({}), 0]
        max_max_pot = max({v.max_pot for v in self.players_dict.values()})

        for pid, p in self.players_dict.items():
            main_pot[2] += p.max_pot
            if p.folded: 
                continue

            earnings[pid] = 0
            hands[pid] = p.hand

            if p.chips == 0 and p.max_pot < max_max_pot:
                allin = [p.max_pot, set({}), 0]
                if allin not in allins:
                    allins.append(allin)
            else:
                main_pot[1].add(pid)
        
        allins.sort(key=lambda x: x[0])

        for i in range(len(allins)):
            for pid, p in self.players_dict.items():
                if not p.max_pot:
                    continue
                elif p.max_pot < allins[i][0]:
                    # must be folded
                    allins[i][2] += p.max_pot
                    p.max_pot = 0
                else:
                    allins[i][2] += allins[i][0]
                    p.max_pot -= allins[i][0]
                    allins[i][1].add(pid)

            for j in range(i+1, len(allins)):
                allins[j][0] -= allins[i][0]

            main_pot[2] -= allins[i][2]

        rankings = rh.rank_hands(hands, self.community_cards)
        allins.append(main_pot)

        for pot in allins:
            pot_ranks = []
            for p, r in rankings.items():
                if p not in pot[1]: continue
                pot_ranks.append(r)
            pot_ranks.sort(key=lambda x: (x[1],x[2]))
            split = [pot_ranks.pop()]
            if pot_ranks:
                for pr in pot_ranks:
                    if pr[1] == split[0][1] and pr[2] == split[0][2]:
                        split.append(pr)
                    else:
                        break
            s = len(split)
            sp = pot[2]
            rem = sp % s
            for pl in split:
                earnings[pl[0]] += (sp - rem) // s
            for pl in split:
                earnings[pl[0]] += 1
                rem -= 1
                if not rem: break


