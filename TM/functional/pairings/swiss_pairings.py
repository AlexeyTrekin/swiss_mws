import warnings
import numpy as np
from typing import List, Tuple

from .pairings import Pairings
from ...model import Fighter


class SwissPairings(Pairings):
    """
    Swiss tournament system that tries to avoid repeated pairings
    The parameters make balance between speed and probability of repeat:

    Args:
        max_diff: maximum rating difference for the pair to be established. If negative, any is allowed
        candidates_to_keep: number of candidate pairings to keep at each stage.
            The more it is, the longer the pairing takes, but probability of good solution grows. Default is OK.
    """
    def __init__(self, max_diff=-1, candidates_to_keep=15):
        super().__init__()
        self.max_diff = max_diff
        self.candidates_to_keep = candidates_to_keep

    def __call__(self, fighters: List[Fighter]) -> List[Tuple[Fighter, Fighter]]:
        """Returns a list of pairs of players for the next round of a match in this tour.

        Assuming that there are an even number of players registered, each player
        appears exactly once in the pairings.  Each player is paired with another
        player with an equal or nearly-equal HP, that is, a player adjacent
        to him or her in the standings.  Rematches are not allowed, so all pairings are new
        (excluding situations when all pairs have matched, see Fighter.normalize_played )

        Returns: a list of tuples of fighters
        """
        if len(fighters) % 2 != 0 or len(fighters) == 0:
            raise ValueError("Number of fighters is {}, does not suit for pairing".format(len(fighters)))

        standings = sorted(fighters, key=lambda f: f.rating, reverse=True)

        # Dynamic programming method with width-search and cutoff of the bad variants
        # We start from pairing all the players with the first one
        # Then we add the next pair to each first pair until all are paired
        # Keeping these requirements:
        # 1. Without the same pairing twice
        # 2. Minimizing the maximum point difference between matches
        # The current version cuts the best candidates at every iteration and thus is sped up very much, but
        # can miss good variants

        candidates = [Candidate([], standings)]
        for i in range(len(standings) // 2):
            new_candidates = []
            for c in candidates:
                first = c.remaining[0]
                for second in c.remaining[1:]:
                    if not (first.played(second) or second.played(first)) and \
                            (abs(first.rating - second.rating) <= self.max_diff or self.max_diff < 0):
                        new_candidates.append(c.add_pair((first, second)))
            candidates = sorted(new_candidates,
                                key=lambda candidate: candidate.max_diff)[
                         0:min(self.candidates_to_keep, len(new_candidates))]
            # In some cases the algorithm will fail and give zero candidates for the current standings.
            # It is a rare situation in real parameters, but we must have a solution for it
            if len(candidates) == 0:
                warnings.warn("Pairings failed to match without repeared fight!")
                return swiss_pairings_old(fighters)
        # candidates = sorted(candidates, key=lambda candidate: candidate.max_diff*len(standings)*10 + candidate.tot_diff)
        return candidates[0].pairs


def swiss_pairings_old(fighters: List[Fighter]):
    """Returns a list of pairs of players for the next round of a match in this tour.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal HP, that is, a player adjacent
    to him or her in the standings.  Rematches are not allowed, so all pairings are new
    (excluding situations when all pairs have matched, see Fighter.normalize_played )

    Returns: a list of tuples of fighters
    """

    if len(fighters) % 2 != 0 or len(fighters) == 0:
        raise ValueError("Number of fighters is {}, does not suit for pairing".format(len(fighters)))

    standings = sorted(fighters, key=lambda f: f.rating, reverse=True)

    pairings = []

    for i in range(0, len(standings), 2):
        for j in range(i + 1, len(standings)):
            if not (standings[i].played(standings[j]) or standings[j].played(standings[i])):
                # good pair found, swap into place then break the inner loop
                while j > i + 1:
                    standings[j - 1], standings[j] = standings[j], standings[j - 1]
                    j -= 1
                break
        pairings.append((standings[i], standings[i + 1]))
    return pairings


class Candidate:
    """ A Candidate pairing

    It represents a pairing under construction, where .pairs are established pairs,
    and .remaining are the fighters who do not have a pair yet

    It is necessary for the swiss_pairings to store the pairing variants

    """
    def __init__(self, pairs: List[Tuple[Fighter, Fighter]], fighters: List[Fighter]):
        self.pairs = pairs
        self.remaining = [f for f in fighters if not any(f in p for p in pairs)]

        diff = [abs(p[0].rating - p[1].rating) for p in pairs]
        if not diff:
            self.max_diff = 0
            self.tot_diff = 0
        else:
            self.max_diff = np.max(diff)
            self.tot_diff = np.sum(diff)

    def add_pair(self, pair):
        return Candidate(self.pairs + [pair], self.remaining)



