
def rank_hand(hole, community, straight, flush, straghtflush):
    cards = hole.union(community)
    vals = {}
    pair = 0
    trip = 0
    quad = 0
    
    # Get high cards
    min_best = 0
 

    # Get pairs, sets, quads
    for card in cards:
        if card[0] in vals:
            vals[card[0]] += 1

            if vals[card[0]] == 2:
                pair += 1

                if pair == 1:
                    min_best = max(min_best, 6) if trip else max(min_best, 1)

                else:
                    min_best = max(min_best, 2)
                
            elif vals[card[0]] == 3:
                pair -= 1
                trip += 1
                min_best = max(min_best, 6) if pair else max(min_best, 3)

            else:
                trip -= 1
                quad += 1
                min_best = max(min_best, 7)
            
        else:
            vals[card[0]] = 1

    # Get straights
    if straight:
        if straight == 'all' or tuple(sorted([card[0] for card in hole])) in straight:
            min_best = max(min_best, 4)

    # Get flushes
    if flush:
        if flush == 'all':
            min_best = max(min_best, 5)
        else:
            matches = flush[0]
            for card in hole:
                if card in flush[1]:
                    matches -=1
            if matches <= 0:
                min_best = max(min_best, 4)

    # Get straight-flushes
    if straghtflush:
        if straghtflush == 'all' or tuple(sorted([c for c in hole])) in straghtflush:
            min_best = 8

    return(min_best)


def straight_draws(community):
    draws = set({})

    vals = {x[0] for x in community}

    wheelcards = {0,1,2,3,12} - vals
    if len(wheelcards) == 0:
        return('all')
    elif len(wheelcards) == 1:
        w = wheelcards.pop()
        for i in range(13):
            draws.add(tuple(sorted([w, i])))

    elif len(wheelcards) == 2:
        draws.add(tuple(sorted([c for c in wheelcards])))

    for i in range(9):
        slider = {j for j in range(i, i + 5)}
        to_straight = slider - vals

        if len(to_straight) == 0:
            return('all')

        elif len(to_straight) == 1:
            w = to_straight.pop()
            for i in range(13):
                draws.add(tuple(sorted([w, i])))

        elif len(to_straight) == 2:
            draws.add(tuple(sorted([c for c in to_straight])))

    return(draws)


def flush_draws(community):
    max_suit = -1
    flush_suit = None

    suits = {x:0 for x in range(3)}
    for card in community:
        suits[card[1]] += 1
        if suits[card[1]] > max_suit:
            max_suit = suits[card[1]]
            flush_suit = card[1]

    if max_suit == 5:
        return('all')

    elif max_suit in [3,4]:
        draws = set({})

        for i in range(13):
            draws.add((i,flush_suit))

        return((5-max_suit, draws, flush_suit))

    else:
        return(None)


def straightflush_draws(community, straight, flush):
    if not (straight and flush):
        return(None)

    if straight == 'all' and flush_draws == 'all':
        return('all')

    single_draws = set({})
    double_draws = set({})
    

    slider = {(0, flush[2]), (1, flush[2]), (2, flush[2]), (3, flush[2]), (12, flush[2])}
    to_sf = slider - community
    if len(to_sf) == 2:
        double_draws.add(tuple(sorted([k for k in to_sf])))

    elif len(to_sf) == 1:
        single_draws.union(to_sf)

    for i in range(9):
        slider = {(j,flush[2]) for j in range(i, i + 5)}
        to_sf = slider - community
        if len(to_sf) == 2:
            double_draws.add(tuple(sorted([k for k in to_sf])))

        elif len(to_sf) == 1:
            single_draws.union(to_sf)

    return((single_draws, double_draws))


def higher_hole_card(h1,h2):
    a = sorted([n[0] for n in h1])
    b = sorted([n[0] for n in h2])
    for i in range(2):
        if a[i] == b[i]:
            continue
        elif a[i] > b[i]:
            return(1)
        else:
            return(2)

    return(None)

def higher_multiple(h1,h2, community, k, add_pair):

    a2 = b2 = 0

    a_count = {}
    for card in h1:
        if card[0] in a_count:
            a_count[card[0]] 
        else:
            a_count[card[0]] += 1
    for card in community:
        if card[0] in a_count:
            a_count[card[0]] 
        else:
            a_count[card[0]] += 1
    a = -1
    for key, val in a_count.items():
        if val == k and key > a:
            a = key
    
    b_count = {}
    for card in h1:
        if card[0] in b_count:
            b_count[card[0]] 
        else:
            b_count[card[0]] += 1
    for card in community:
        if card[0] in b_count:
            b_count[card[0]] 
        else:
            b_count[card[0]] += 1
    b = -1
    for key, val in b_count.items():
        if val == k and key > a:
            b = key

    if add_pair:

        for key, val in a_count.items():
            if val >= 2 and key != a and key > a2:
                a2 = key

        for key, val in b_count.items():
            if val >= 2 and key != b and key > b2:
                b2 = key
    
    if a > b:
        return(1)
    elif b > a:
        return(2)
    elif a2 > b2:
        return(1)
    elif b2 > a2:
        return(2)
    else:
        return(None)


def break_tie(h1,h2, community, rank):
    same = sorted([n[0] for n in h1]) == sorted([n[0] for n in h2])

    if same and rank not in [5,8]: return(None) 

    # high card
    if rank == 0:
        return(higher_hole_card(h1,h2))

    # 1 pair
    elif rank == 1:
        result = higher_multiple(h1,h2, community, 2, False)
        if result:
            return(result)
        else:
            return(higher_hole_card(h1,h2))

    # 2 pair
    elif rank == 2:
        result = higher_multiple(h1,h2, community, 2, True)
        if result:
            return(result)
        else:
            return(higher_hole_card(h1,h2))

    # 3 of a kind
    elif rank == 3:
        result = higher_multiple(h1,h2, community, 3, False)
        if result:
            return(result)
        else:
            return(higher_hole_card(h1,h2))

    # straight
    elif rank == 4:

        return(None)

    # flush
    elif rank == 5:
        suits = {k:0 for k in range(3)}
        for c in community:
            suits[c[1]] += 1
        suit = max(suits.values())

        a_top = b_top= -1

        for card in h1:
            if card[1] == suit and card[0] > a_top:
                a_top = card[0]

        for card in h2:
            if card[1] == suit and card[0] > b_top:
                b_top = card[0]

        if a_top > b_top:
            return(1)
        elif b_top > a_top:
            return(2)
        else:
            return(None)

    # full house
    elif rank == 6:
        result = higher_multiple(h1,h2, community, 3, True)
        if result:
            return(result)
        else:
            return(higher_hole_card(h1,h2))

    # four of a kind
    elif rank == 7:
        result = higher_multiple(h1,h2, community, 4, False)
        if result:
            return(result)
        else:
            return(higher_hole_card(h1,h2))

    # straight flush
    elif rank == 8:
        return(None)

