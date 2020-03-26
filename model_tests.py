import unittest
import random
from holdem_model import table, player, rank_hands as rh


def random_card():
    return((random.randint(0,12),random.randint(0,3)))


REPEAT_RANDOM_TESTS = 1000


class TestShowdown(unittest.TestCase):
    def testShowdown(self):
        pass

# class TestTableConstructor(unittest.TestCase):
#     def testConstructor(self):
#         #for _ in range(REPEAT_RANDOM_TESTS):
#         for i in range(3,11):

#             pids = [x for x in range(i)]
#             random.shuffle(pids)
#             removed = set({}) 
#             t = table.Table(num_players=i)

#             for j in range(i-1):

#                 if j:
#                     to_remove = pids.pop()
#                     removed.add(to_remove)
#                     t.remove_player(to_remove)

#                 self.assertEqual(set(pids).union(removed), {x for x in range(i)})

#                 self.assertEqual(i-j, t.num_players)
#                 self.assertEqual(len(t.players_dict), t.num_players)

#                 random_player_id = random.randint(0, len(pids)-1)
#                 current = t.players_dict[pids[random_player_id]]

#                 seen = []

#                 for _ in range(len(pids)):
#                     seen.append(current.playerid)
#                     current = current.next_player

#                 self.assertEqual(sorted(pids), sorted(seen))

#                 blind_tot = 0
#                 for p in t.players_dict.values():
#                     blind_tot += p.blind
#                 self.assertEqual(blind_tot, 3)




# class TestPlayerAction(unittest.TestCase):
#     def testAction(self):
#         for _ in range(REPEAT_RANDOM_TESTS):
#             buyin = random.randint(0,200)
#             p = player.Player(1, buyin)
#             to_call = random.randint(0,200)
#             bet_amount = random.randint(0,200)
#             result = p.action(to_call, bet_amount)
        
#             self.assertLessEqual(result, buyin)
#             if bet_amount < min(to_call, p.chips):
#                 self.assertEqual(result,0)
            
#             if to_call <=bet_amount and  bet_amount < p.chips:
#                 self.assertEqual(result, bet_amount)

# class TestRankHands(unittest.TestCase):

#     def testRandomHands(self):
#         for _ in range(REPEAT_RANDOM_TESTS):
#             num_players = random.randint(2,10)
#             community = set({})
#             while len(community) <  5 + (2 * num_players):
#                 community.add(random_card())

#             hole_dict = {}
#             for i in range(num_players):
#                 hole_dict[i] = {community.pop() for _ in range(2)}

#             results = rh.rank_hands(hole_dict, community)




# class TestGetRank(unittest.TestCase):
    
#     def testStraightFlush(self):

#         for _ in range(REPEAT_RANDOM_TESTS):
#             highest = random.randint(4,12)
#             suit = random.randint(0,3)

#             community = {(i,suit) for i in range(highest - 4, highest + 1)}

#             while len(community) < 7:
#                 c = random_card()
#                 if c not in community:
#                     community.add(c)

#             hole = {community.pop() for _ in range(2)}
            
            
#             rank = rh.get_rank(1, hole, community)

#             self.assertEqual(rank[1], 8, 'Missed the straight flush.')
#             self.assertGreaterEqual(rank[2], highest, 'Missed the highest straight flush')


#     def testQuads(self):

#         for _ in range(REPEAT_RANDOM_TESTS):
#             q = random.randint(0,12)
#             community = {(q,i) for i in range(4)}
#             hole = set({})
#             while len(hole) < 3:
#                 r = random_card()
#                 if r not in community:
#                     hole.add(r)
            
#             max_single = max({x[0] for x in hole})
#             rank = rh.get_rank(1, hole, community)

#             community = community.union(hole)
#             hole = {community.pop() for _ in range(2)}

#             self.assertEqual(rank[1], 7, 'Missed quads.')

#             if q:
#                 self.assertEqual(int(str(rank[2])[:-2]), q, 'Tiebreaker is wrong')

#             self.assertEqual(int(str(rank[2])[-2:]), max_single, 'Tiebreaker is wrong')


#     def testBoat(self):
        
#         for _ in range(REPEAT_RANDOM_TESTS):

#             p = t = random.randint(0,12)
#             while p == t:
#                 p = random.randint(0,12)
            
#             ts = {(t,i) for i in range(4)}
#             ts.pop()
#             ps = {(p,i) for i in range(4)}
#             for _ in range(2): ps.pop()

#             other = set({})
#             while len(other) < 2:
#                 c = random_card()
#                 if c not in ts.union(ps):
#                     other.add(c)

#             community = ts.union(ps,other)

#             hole = {community.pop() for _ in range(2)}

#             rank = rh.get_rank(1, hole, community)

#             self.assertGreaterEqual(rank[1], 6, 'Missed Full House')

#             if t and rank[1] == 6:
#                 self.assertGreaterEqual(int(str(rank[2])[:-2]), t, 'Tiebreaker is wrong')
            

#     def testFlush(self):
#         for _ in range(REPEAT_RANDOM_TESTS):
#             poss = sorted(random.sample(range(13), 5), reverse=True)
#             suit = random.randint(0,3)
#             community = {(i, suit) for i in poss}
#             while len(community) < 7:
#                 community.add(random_card())
#             hole = {community.pop() for _ in range(2)}

#             rank = rh.get_rank(1, hole, community)
#             tb = rh.to_tb(poss)

#             self.assertGreaterEqual(rank[1], 5, 'Missed Flush')

#             if rank[1] == 5:
#                 self.assertGreaterEqual(rank[2], tb, 'Tiebreaker is wrong')

#     def testStraight(self):
#         for _ in range(REPEAT_RANDOM_TESTS):
#             top = random.randint(4,12)
#             community = {(i, random.randint(0,3)) for i in range(top-4, top+1)}

#             while len(community) < 7:
#                 community.add(random_card())
#             hole = {community.pop() for _ in range(2)}
#             rank = rh.get_rank(1, hole, community)
#             self.assertGreaterEqual(rank[1], 4, 'Missed Straight')

#             if rank[1] == 4:
#                 self.assertGreaterEqual(rank[2], top, 'Tiebreaker is wrong')

#     def testTrips(self):
#         for _ in range(REPEAT_RANDOM_TESTS): 
#             t = random.randint(0,12)
#             community = {(t,i) for i in range(4)}
#             community.pop()

#             while len(community) < 7:
#                 community.add(random_card())
#             hole = {community.pop() for _ in range(2)}
#             rank = rh.get_rank(1, hole, community)
#             self.assertGreaterEqual(rank[1], 3, 'Missed Trips')

#             tb = rh.to_tb(sorted([t] + [x[0] for x in community.union(hole) - {t}], reverse=True)[:2])


#             if rank[1] == 3:
#                 self.assertGreaterEqual(rank[2], tb, 'Tiebreaker is wrong')

#     def testTwoPair(self):
#         for _ in range(REPEAT_RANDOM_TESTS): 
#             p1 = p2 = random.randint(1,12)
#             while p1 == p2:
#                 p2 = random.randint(0,p1-1)

#             p1s = {(p1,i) for i in range(4)}
#             p2s = {(p2,i) for i in range(4)}
#             for _ in range(2):
#                 p1s.pop()
#                 p2s.pop()
#             community = p1s.union(p2s)

#             while len(community) < 7:
#                 community.add(random_card())
#             hole = {community.pop() for _ in range(2)}
#             rank = rh.get_rank(1, hole, community)
#             self.assertGreaterEqual(rank[1], 2, 'Missed Two Pair')            

#             if rank[1] == 2:
#                 tb = rh.to_tb([p1, p2, max({c[0] for c in community.union(hole)} - {p1,p2})])
#                 self.assertGreaterEqual(rank[2], tb, 'Tiebreaker is wrong')


#     def testPair(self):
#         for _ in range(REPEAT_RANDOM_TESTS): 
#             p = random.randint(1,12)
#             community = {(p,i) for i in range(4)}
#             for _ in range(2):
#                 community.pop()

#             while len(community) < 7:
#                 community.add(random_card())
#             hole = {community.pop() for _ in range(2)}

#             rank = rh.get_rank(1, hole, community)
#             self.assertGreaterEqual(rank[1], 1, 'Missed Pair') 
            
#             if rank[1] == 1:
#                 tb = rh.to_tb([p, max({c[0] for c in community.union(hole)} - {p})])
#                 self.assertGreaterEqual(rank[2], tb, 'Tiebreaker is wrong')

    
#     def testHighCard(self):
#         for _ in range(REPEAT_RANDOM_TESTS): 
#             community = set({})
            
#             while len(community) < 7:
#                 community.add(random_card())
#             hole = {community.pop() for _ in range(2)}

#             rank = rh.get_rank(1, hole, community)
#             self.assertGreaterEqual(rank[1], 0, '????') 
        
#             if rank[1] == 0:
#                 tb = rh.to_tb(sorted([x[0] for x in community.union(hole)], reverse=True)[:5])
#                 self.assertGreaterEqual(rank[2], tb, 'Tiebreaker is wrong')

if __name__ == "__main__":
    unittest.main()