from TM.functional.pairings.round_pairings import RoundPairings

MAX_FIGHTERS = 50

class TestRoundPairings:

    def test_total_fight_number(self):
        for i in range(1, MAX_FIGHTERS):
            fighters = [j for j in range(1, i + 1)]
            pairings = RoundPairings()(fighters)
            assert len(pairings) == len(fighters)*(len(fighters)-1)/2

    def test_fights_number_for_each_fighter(self):
        for i in range(1, MAX_FIGHTERS):
            fights = {}
            fighters = [j for j in range(1, i + 1)]
            pairings = RoundPairings()(fighters)

            for i in range(len(pairings)):
                if pairings[i][0] not in fights.keys():
                    fights[pairings[i][0]] = 1
                else:
                    fights[pairings[i][0]] += 1

                if pairings[i][1] not in fights.keys():
                    fights[pairings[i][1]] = 1
                else:
                    fights[pairings[i][1]] += 1
            for f, f_num in fights.items():
                assert f_num == len(fighters) - 1

    def test_no_self_fight(self):
        for fighters_num in range(1, MAX_FIGHTERS):
            fighters = [i for i in range(1, fighters_num + 1)]
            pairings = RoundPairings()(fighters)

            for pair in pairings:
                assert pair[0] != pair[1]

    def test_no_repeat(self):
        for fighters_num in range(3, MAX_FIGHTERS):
            fighters = [i for i in range(1, fighters_num + 1)]
            pairings = RoundPairings()(fighters)

            for f1 in range(len(fighters) - 1):
                for f2 in range(f1+1, len(fighters)):
                    assert pairings[f1] != pairings[f2]
                    # search for the same fight in reverse order
                    assert pairings[f1][0] != pairings[f2][1] or pairings[f2][0] != pairings[f1][1]

    def test_no_two_fights_in_row(self):
        # In the groups of 4 and 3 it is OK to have fights in a row, so skipping this test
        for fighters_num in range(5, MAX_FIGHTERS):
            fighters = [i for i in range(1, fighters_num + 1)]
            pairings = RoundPairings()(fighters)

            for f1 in range(len(fighters) - 1):
                assert pairings[f1][0] != pairings[f1 + 1][0] and pairings[f1][0] != pairings[f1 + 1][1] and \
                        pairings[f1][1] != pairings[f1 + 1][0] and pairings[f1][1] != pairings[f1 + 1][1]

