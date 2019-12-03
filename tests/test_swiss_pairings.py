import pytest
from ..pairings.swiss_pairings import swiss_pairings
from ..tournament.fighter import Fighter

MAX_FIGHTERS = 50


class ProxyFighter:
    """
    mocks the basic functionality needed for the fighter class: has name, list of matches, and can be matched with other
    """
    def __init__(self, name, hp=12, enemies = []):
        self.name = name
        self.hp = hp
        self.enemies = enemies

    def played(self, other):
        if other.name in self.enemies:
            return True
        else:
            return False

    def match(self, other, score=0):
        self.enemies.append(other.name)
        self.hp += score



def generate_data_all():
    """
    Generates test cases for further tests
    Will add more test cases.
    :return:
    """
    data = []
    data.append([ProxyFighter(name=str(i+1)) for i in range(12)])
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