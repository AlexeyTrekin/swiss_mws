class Fighter:

    def __init__(self, name, hp=12):
        self.name = name
        # health points for all the tournament
        self.hp = hp
        # a list of other fighters, with which this one has fought
        self.enemies = {}

    def to_str(self):
        """
        Format all the fighter data in the form we need to read it further
        :return:
        """
        opps = [':'.join([str(key), str(value)]) for key, value in self.enemies.items()]
        return ','.join([self.name, str(self.hp)] + opps)

    def fight(self, other, hp_lost):
        if other.name in self.enemies.keys():
            self.enemies[other.name] += 1
        else:
            self.enemies[other.name] = 1
        self.hp -= hp_lost

    def played(self, other):
        if other.name in self.enemies.keys():
            return self.enemies[other.name]
        else:
            return 0

    def normalize_played(self, others):
        """
        If all others have played at least once, wa cannot make pairings any more, as the system tries to
        avoid repetitive figths. So, if all the 'played' vaules for current opponents are positive,
        we substract from it to have zeros again
        This can be not mutual, as there may be free slots for one of the fighters and no slots for the other one.
        That is why we must check played() for both
        :param others: list of Fighters to match
        :return: None
        """
        min_played = 99

        for o in others:
            if o.name not in self.enemies.keys():
                return
            else:
                m = min(min_played, self.enemies[o.name])
        if min_played == 0:
            return
        # If we reached here it means that all others played at least 1 time
        # Then we substract 1 from all of them to nullify at least one of them
        print(self.name + " played with all at least {} times".format(m))
        for o in others:
            self.enemies[o.name] -= m

    def __repr__(self):
        return (self.name + ', ' + str(self.hp))


def fighter_from_str(line: str, maxHP: int) -> Fighter:
    """
    String format:
    NAME,<HP>,<Opponent:NumOfFights>
    :return:
    """
    split = line.split(',')
    # This is a very unsafe function, but will do if we only read the properly formatted data
    name = split[0].rstrip()
    f = Fighter(name)
    if len(split) > 1:
        f.hp = int(split[1].rstrip())
    else:
        f.hp = maxHP
    for cell in split[2:]:
        opp = cell.rstrip().split(':')
        f.enemies[opp[0]] = int(opp[1])
    return f
