import pytest
from ..pairings.swiss_pairings import swiss_pairings
from ..tournament.fighter import Fighter

MAX_FIGHTERS = 50


def generate_data_all():
    data = []
    data.append([Fighter(name=str(i+1)) for i in range(12)])
    # Add more data samples
    return data


class TestSwissPairings:

    # Test normal behavior
    def test_num_fights_in_a_round(self):
        for fighters in generate_data_all():
            pairings = swiss_pairings(fighters)
            assert len(pairings) == len(fighters)/2

    def test_one_fight_for_fighter_in_a_round(self):
        for fighters in generate_data_all():
            pairings = swiss_pairings(fighters)
            fights = {}
            for i in range(len(pairings)):
                if pairings[i][0] not in fights.keys():
                    fights[pairings[i][0].name] = 1
                else:
                    fights[pairings[i][0].name] += 1

                if pairings[i][1] not in fights.keys():
                    fights[pairings[i][1].name] = 1
                else:
                    fights[pairings[i][1].name] += 1

            # Fighters list is the same
            assert sorted([f.name for f in fighters]) == sorted(list(fights.keys()))

            # Every one gets one fight
            for f, f_num in fights.items():
                assert f_num == 1

    def test_no_self_fight(self):
        for fighters in generate_data_all():
            pairings = swiss_pairings(fighters)
            for p in pairings:
                assert p[0] != p[1]

    def test_no_repeated_fight(self):
        for fighters in generate_data_all():
            pairings = swiss_pairings(fighters)
            for p in pairings:
                assert p[1].name not in p[0].enemies
                assert p[0].name not in p[1].enemies

    # test special cases
    def test_error_on_odd_number(self):
        fighters = [Fighter(name=str(i + 1)) for i in range(11)]
        with pytest.raises(ValueError):
            swiss_pairings(fighters)