

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



# ----Rank Hands----

def rank_hands(hole_dict, community):

    hand_ranks = {}

    for k, v in hole_dict.items():
        hand_ranks[k] = (get_rank(k, v, community))
    
    return(hand_ranks)