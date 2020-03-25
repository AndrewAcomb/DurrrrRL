

# ----Get Possible----

def get_possible(community):
    poss = {}

    # Check if the board is paired

    pb = {c: 0 for c in range(13)}
    for c in community:
        pb[c[0]] += 1

    bps = []
    for item in pb.items():
        if item[1] > 1:
            bps.append(item)
    bps.sort()

    poss['q'] = None if bps else poss_q(community, bps)
    poss['fh'] = None if bps else poss_fh(community, pb)

    # Check if flushes are possible
    fsf = {c: 0 for c in range(4)}
    for c in community:
        fsf[c[1]] += 1
        if fsf[c[1]] > 2:
            f_suit = c[1]
            fsf = False
            break
    
    poss['f'] = None if fsf else poss_f(community, f_suit)

    # Check if straights are possible
    
    poss['s'] = poss_s(community)

    poss['sf'] = None if fsf or not poss['s'] else poss_sf(community, f_suit)

    poss['t'] = poss_t(community)

    poss['2p'] = poss_2p(community, bps)

    return(poss)


def poss_q(community, bps):
    # results[(full hand)] = tiebreaker

    results = {}
    itr = 0
    for i in range(len(bps)):
        template = [(bps[i][0], j) for j in range(4)]
        for v in range(13):
            if v==bps[i][0]: continue
            for s in range(4):
                results[tuple(sorted(template + [(v, s)], key=lambda x: (x[0], x[1])))] = itr
            itr += 1

    return(results)


def poss_fh(community, pb):
    # results[(set,pair)] = tiebreaker

    results = {}
    itr = 0
    
    for i in range(13):
        for j in range(13):
            if i==j:
                continue
            if pb[i] + pb[j] >= 3:
                results[(i,j)] = itr
                itr += 1

    return(results)


def poss_sf(community, f_suit):
    # results[(whole hand)] = tiebreaker

    results = {((0,f_suit), (1,f_suit), (2,f_suit), (3,f_suit), (12,f_suit)):0}

    itr = 1

    for i in range(9):
        results[((i + 0, f_suit), (i + 1, f_suit), (i + 2, f_suit), (i + 3, f_suit), (i + 4, f_suit))] = itr
        itr += 1

    return(results)


def poss_f(community, f_suit):
    # results[(whole hand)] = tiebreaker

    results = {}
    suited = []
    for c in community:
        if c[1] == f_suit:
            suited.append(c[0])

    top3 = sorted(suited)[-3:]

    template = [(top3[0], f_suit), (top3[1], f_suit), (top3[2], f_suit)]

    for i in range(12):
        for j in range(i+1, 13):
            if i in top3 or j in top3:
                continue
            results[tuple(sorted(template + [(i, f_suit), (j, f_suit)], key=lambda x: x[0]))] = itr
            itr += 1

    return(results)


def poss_s(community):
    # results[(straight (no suits))] = tiebreaker

    results = {}
    itr = 0
    vals = {c[0] for c in community}

    if len(vals) < 3:
        return(None)

    # The wheel
    if len({0,1,2,3,12} - vals) < 3:
        results[(0,1,2,3,12)] = 0
        itr += 1

    for i in range(9):
        if len({x for x in range(i,i+5)} - vals) < 3:
            results[tuple([x for x in range(i,i+5)])] = itr
            itr += 1

    return(results)

def poss_t(community):
    # results[(trip, 2nd highest, high card)] = tiebreaker

    results = {}

    vals = sorted(list({v[0] for v in community}))

    itr = 0
    for v in vals:
        for i in range(12):
            if i == v:
                continue
            for j in range(i+1, 13):
                if j == v:
                    continue
                results[(v, i, j)] = itr
                itr += 1

    return(results)


def poss_2p(community, bps):

    results = {}
    itr = 0
    for i in range(12):
        for j in range(i + 1, 13):
            for k in range(13):
                if k not in [i,j]:
                    results[(j,i,k)] = itr
                    itr += 1

    return(results)




# ----Get Rank----

def get_rank(playerid, hole_cards, community, possible):
    
    cards = hole_cards.union(community)

    hands = set({})
    vals = {}

    for card1 in cards:
        if card1 in vals:
            vals[card1[0]] += 1
        else:
            vals[card1[0]] = 1

        temp = cards - {card1}
        for card2 in temp:
            hands.add(tuple(sorted([c for c in temp - {card2}], key = lambda x: (x[0], x[1]))))

    rank = 0
    tiebreaker = 0
    multiplicity = sorted([item for item in vals.items()], key=lambda x: x[1], reverse=True)

    # SF
    if possible['sf']:
        for hand in hands:
            if hand in possible['sf']:
                rank = max(rank, 8)
                tiebreaker = max(tiebreaker, possible['sf'][hand])
        if rank == 8:
            return((playerid, rank, tiebreaker))

    # Q
    if possible['q'] and multiplicity[0][1] == 4:
        for hand in hands:
            if hand in possible['q']:
                rank = max(rank, 7)
                tiebreaker = max(tiebreaker, possible['q'][hand])
        if rank == 7:
            return((playerid, rank, tiebreaker))

    # FH
    if possible['fh']:
        if multiplicity[0][1] >= 3 and multiplicity[1][1] >= 2:
            trips = []
            pairs = []
            for m in multiplicity:
                if m[1] >= 3:
                    trips.append(m[0])
                    pairs.append(m[0])
                elif m[1] == 2:
                    pairs.append(m[0])
                else:
                    break
            trips.sort()
            pairs.sort()
            t = trips[-1]
            p = pairs[-2] if t==pairs[-1] else pairs[-1]
            return((playerid, 6, possible['q'][(t,t,t,p,p)]))


    # F
    if possible['f']:
        for hand in hands:
            if hand in possible['f']:
                rank = 5
                tiebreaker = max(tiebreaker, possible['f'][hand])
        if rank == 5:
            return((playerid, rank, tiebreaker))

    # S
    if possible['s']:
        if len(vals) < 5:
            for i in reversed(range(min(vals) + 5, max(vals) + 1)):
                if {x for x in range(i-5, i)} <= set(vals):
                    return((playerid, 4, possible['s'][tuple([x for x in range(i-5, i)])]))

    # 3
    if multiplicity[0][1] == 3:
        vals_arr = sorted([x for x in vals], reverse=True)
        if vals_arr[0] == multiplicity[0][0]:
            return((playerid, 3, possible['t'][(multiplicity[0][0], vals_arr[4], vals_arr[3])]))
        else:
            return((playerid, 3, possible['t'][(multiplicity[0][0], vals_arr[1], vals_arr[0])]))

    # 2P
    if multiplicity[0][1] == multiplicity[1][1] == 2:
        pairs = []
        for m in multiplicity:
            if m[1] == 2:
                pairs.append(m[0])
        pairs.sort(reverse=True)
        pairs.pop()
        return(playerid, 2, possible['2p'][(pairs[0], pairs[1], max(vals - set(pairs)))])

    # P

    if multiplicity[0][1] == 2:
        others = sorted(list(set(vals) - set(multiplicity[0][0])), reverse=True)
        inorder = [multiplicity[0][0]] + others[:3]
        tb = ''
        for o in inorder:
            if len(str(o)) < 2:
                tb += '0' + str(o)
            else:
                tb += str(o)

        return((playerid, 1, tb))

    # HC

    inorder = sorted(list(vals), reverse=True)

    tb = ''
    for o in inorder:
        if len(str(o)) < 2:
            tb += '0' + str(o)
        else:
            tb += str(o)
    return((playerid, 0, int(tb)))



# ----Rank Hands----

def rank_hands(hole_dict, community):
    
    hand_ranks = []

    possible = get_possible(community)

    for k, v in hole_dict.items():
        hand_ranks.append(get_rank(k, v, community, possible))

    hand_ranks.sort(lambda x: (x[1],x[2]), reverse=True)

    prev = hand_ranks[-1]
    results = [[hand_ranks.pop()[0]]]


    while hand_ranks:
    
        if hand_ranks[-1][1] == prev[1] and hand_ranks[-1][2] == prev[2]:
            results[-1].append(hand_ranks.pop()[0])
        else:
            prev = hand_ranks.pop()
            results.append([prev[0]])

    return(results)