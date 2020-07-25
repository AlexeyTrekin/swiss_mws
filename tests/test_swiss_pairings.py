import pytest
from random import randint
from TM.pairings import SwissPairings
from TM.tournament import Fighter

MAX_FIGHTERS = 20
MAX_HP = 20


class ProxyFighter:
    """
    mocks the basic functionality needed for the fighter class: has name, list of matches, and can be matched with other
    """
    def __init__(self, fighter_id: str, rating: int = 0,  fights=None):
        self.fighter_id = fighter_id
        self.rating = rating
        if fights is None:
            self.fights = []
        else:
            self.fights = fights

    def played(self, other):
        """
        Legacy. Will be replaced by self.fights and its queries
        :param other:
        :return:
        """
        if other.fighter_id in self.fights:
            return 1
        else:
            return 0


def generate_data_all():
    """
    Generates test cases for further tests
    Will add more test cases.
    :return:
    """
    data = []
    # Just a blank tournament
    data.append([ProxyFighter(fighter_id=str(i+1)) for i in range(12)])
    # This case emerged from our first tournament and revealed that the current method is flawed,

    # As it paired Ryabov with Volodkov again
    data.append([ProxyFighter('Zakharov', 6, ['Danilov']),
                 ProxyFighter('Kashitsyn', 7, ['Nekrylov']),
                 ProxyFighter('Danilov', 7, ['Volodkov', 'Zakharov']),
                 ProxyFighter('Nekrylov', 7, ['Ryabov', 'Kashitsyn']),
                 ProxyFighter('Volodkov', 7, ['Ryabov', 'Danilov']),
                 ProxyFighter('Ryabov', 10, ['Nekrylov', 'Volodkov'])])

    # And reverse HP, as the previous can pass if we sort the fighters
    data.append([ProxyFighter('Zakharov', 10, ['Danilov']),
                 ProxyFighter('Kashitsyn', 7, ['Nekrylov']),
                 ProxyFighter('Danilov', 7, ['Volodkov', 'Zakharov']),
                 ProxyFighter('Nekrylov', 7, ['Ryabov', 'Kashitsyn']),
                 ProxyFighter('Volodkov', 7, ['Ryabov', 'Danilov']),
                 ProxyFighter('Ryabov', 6, ['Nekrylov', 'Volodkov'])])

    # Big tournament to test time and memory
    data.append([ProxyFighter(fighter_id=str(i+1), rating=randint(1, MAX_HP)) for i in range(MAX_FIGHTERS)])

    # Add more data samples
    return data


class TestSwissPairings:

    # Test normal behavior
    def test_num_fights_in_a_round(self):
        for fighters in generate_data_all():
            pairings = SwissPairings()(fighters)
            assert len(pairings) == len(fighters)/2

    def test_one_fight_for_fighter_in_a_round(self):
        for fighters in generate_data_all():
            pairings = SwissPairings()(fighters)
            fights = {}
            for i in range(len(pairings)):
                if pairings[i][0] not in fights.keys():
                    fights[pairings[i][0].fighter_id] = 1
                else:
                    fights[pairings[i][0].fighter_id] += 1

                if pairings[i][1] not in fights.keys():
                    fights[pairings[i][1].fighter_id] = 1
                else:
                    fights[pairings[i][1].fighter_id] += 1

            # Fighters list is the same
            assert sorted([f.fighter_id for f in fighters]) == sorted(list(fights.keys()))

            # Every one gets one fight
            for f, f_num in fights.items():
                assert f_num == 1

    def test_no_self_fight(self):
        for fighters in generate_data_all():
            pairings = SwissPairings()(fighters)
            for p in pairings:
                assert p[0] != p[1]

    def test_no_repeated_fight(self):
        for fighters in generate_data_all():
            pairings = SwissPairings()(fighters)
            for p in pairings:
                assert p[1].fighter_id not in p[0].fights
                assert p[0].fighter_id not in p[1].fights

    # test special cases
    def test_error_on_odd_number(self):
        fighters = [Fighter(fighter_id=f'{i}', first_name=f'Name{i}', last_name=f'Surname{i}') for i in range(11)]
        with pytest.raises(ValueError):
            SwissPairings()(fighters)

