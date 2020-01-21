from .fighter import Fighter

class Fight:

    def __init__(self, fighter1: Fighter, fighter2: Fighter,
                 fighter1_score=0, fighter2_score=0,
                 fighter1_warns=0, fighter2_warns=0,
                 doubles=0, conducted=False, time=0.0, **kwargs):
        """
        A class describing a fight with all the attributes.
        :param fighter1:
        :param fighter2:
        :param fighter1_score:
        :param fighter2_score:
        :param fighter1_warns:
        :param fighter2_warns:
        :param doubles:
        :param conducted:
        """
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.fighter1_score = fighter1_score
        self.fighter2_score = fighter2_score
        self.fighter1_warns = fighter1_warns
        self.fighter2_warns = fighter2_warns
        self.doubles = doubles
        self.conducted = conducted
        self.time = time

    def repeats(self, other):
        if self.fighter1 == other.fighter1 and self.fighter2 == other.fighter2 \
            or self.fighter1 == other.fighter2 and self.fighter2 == other.fighter1:
            return True
        else:
            return False
