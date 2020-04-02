from itertools import combinations


# ----Get Rank----
def get_rank(playerid, hole_cards, community):
    
    cards = hole_cards.union(community)
    vals = {}
    suits = {}

    for card in cards:
        if card[0] in vals:
            vals[card[0]] += 1
        else:
            vals[card[0]] = 1

        if card[1] in suits:
            suits[card[1]] += 1
        else:
            suits[card[1]] = 1

    valset = set(vals)
    vals_arr = sorted(list(vals))


    # Find highest quads, trips, and pairs
    multiplicity = sorted([item for item in vals.items()], key=lambda x: (x[1], x[0]), reverse=True)


    # Find flushes
    flush = []
    flushsuit = None
    for k,v in suits.items():
        if v < 5: continue
        flushsuit = k

        for card in cards:
            if card[1] == flushsuit:
                flush.append(card[0])

        flush = sorted(flush, reverse=True)
        break


    # Find straights
    straights = []
    if len(vals_arr) >= 5: 
        # The wheel
        if {0,1,2,3,12} <= valset:
            straights.append(3)

        for i in range(4, len(vals_arr)):
            in_row = 4

            while in_row:
                offset = (5 - in_row)
                if vals_arr[i] == vals_arr[i - offset] + offset:
                    in_row -= 1
                else:
                    break

            if not in_row:
                straights.append(vals_arr[i])


    # Straight Flush
    if straights and flush:
        flushset = set(flush)

        for s in reversed(straights):
            if {x for x in range(s-4,s+1)} <= flushset:
                return((playerid, 8, s))
        # The wheel
        if {0,1,2,3,12} <= flushset:
            return((playerid, 8, 3))

    # Four of a Kind
    if multiplicity[0][1] == 4:
        single = max(valset - set({multiplicity[0][0]}))
        return((playerid, 7, to_tb([multiplicity[0][0], single])))

    # Full House
    if  multiplicity[0][1] >= 3 and multiplicity[1][1] >= 2:
        return((playerid, 6, to_tb([multiplicity[0][0],multiplicity[1][0]])))

    # Flush
    if flush:
        return((playerid, 5, to_tb(flush[:5])))

    # Straight
    if straights:
        return((playerid, 4, straights[-1]))

    # Three of a Kind
    if multiplicity[0][1] == 3:
        n = vals_arr[-1] == multiplicity[0][0]
        return((playerid, 3, to_tb([multiplicity[0][0], vals_arr[-1 - n], vals_arr[-2 - n]])))

    # Two Pair
    if len(multiplicity) > 1 and multiplicity[0][1] == multiplicity[1][1] == 2:
        single = max(valset - {multiplicity[0][0], multiplicity[1][0]})
        return((playerid, 2, to_tb([multiplicity[0][0], multiplicity[1][0], single])))

    # Pair
    if multiplicity[0][1] == 2:
        others = sorted(list(valset - {multiplicity[0][0]}), reverse=True)
        return((playerid, 1, to_tb([multiplicity[0][0]] + others[:3])))

    # High Card
    inorder = sorted(vals_arr, reverse=True)[:5]
    return((playerid, 0, to_tb(inorder)))


def to_tb(arr):
    # Generate tiebreaker from hand
    tb = ''   
    for a in arr:
        s = str(a)
        if len(s) < 2:
            tb += '0' + s
        else:
            tb += s
    return(int(tb))

def card_to_string(card):
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    suits = ["D", "C", "H", "S"]
    return(values[card[0]] + suits[card[1]])

def hand_to_string(result):
    hands = ["a high card", "a pair", "two pair", "three of a kind", "a straight",
        "a flush", "a full house", "four of a kind", "a straight flush"]
    return(hands[result])

def int_to_card(cardint):
    return((cardint//4, cardint % 4))

def card_to_int(card):
    return(card[0] * 4 + card[1])

def encode_hole_cards(hole_cards):
    faces = {8:'T',9:'J',10:'Q',11:'K',12:'A'}
    result = ''
    suit = None

    hc = sorted(list(hole_cards), reverse=True)
    if hc[0][0] == hc[1][0]:
        if hc[0][0] in faces:
            result += faces[hc[0][0]]
            result += faces[hc[0][0]]
        else:
            result += str(hc[0][0] + 2)
            result += str(hc[0][0] + 2)
        return(result)

    for card in hc:
        if card[0] in faces:
            result += faces[card[0]]
        else:
            result += str(card[0] + 2)
        if card[1] == suit:
            result += 's'
        else:
            suit = card[1]
    if len(result) < 3:
        result += 'o'
    
    return(result)
			


def get_pot_equity(deck, cards, opp_cards, community):
    # Takes hands as sets of card tuples
    
    num_poss = 0
    wins = 0.0
    # Get possible community cards
    possibilities =  combinations(deck, 5 - len(community)) if len(community) < 5 else [[]]

    # For each possible set of community cards, determine winner
    for p in possibilities:
        my_rank = get_rank(0, cards, community.union(set(p)))
        opp_rank = get_rank(1, opp_cards, community.union(set(p))) 
        if my_rank[1] > opp_rank[1] or my_rank[1] == opp_rank[1] and my_rank[2] > opp_rank[2]:
            wins += 1.0
        elif my_rank[1] == opp_rank[1] and my_rank[2] > opp_rank[2]:
            wins += 0.5
        num_poss += 1

    return(wins/num_poss)


def get_bet_ev(to_call, fold_chance, pot_equity, pot, bet):
    # Calculates the expected change in EV for a given bet

    # Current EV
    current_ev = pot_equity * (pot)

    # Change in EV if the opponent folds
    fold_ev =  fold_chance * (pot - current_ev)

    # Change in EV if the opponent calls
    new_pot = pot + (2 * bet) + to_call
    cost_of_raising = bet + to_call
    call_ev = (1 - fold_chance) * (pot_equity * new_pot - current_ev - cost_of_raising)

    return(fold_ev + call_ev)