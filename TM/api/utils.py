import numpy as np
from typing import List
from TM.tournament import Fighter, Fight


def split_to_areas(num_pairs, num_areas):
    """
    Evenly splits pairs for the areas.
    :param pairs_num: number of fights to be distributed between the areas
    :param areas_num: number of fencing areas
    :return: list of tuples (begin, end) - range of pairs for each area
    """
    if num_areas > num_pairs or num_areas <= 0:
        raise ValueError("Incorrect number of areas {} or pairs {}".format(num_areas, num_pairs))
    min_pairs = num_pairs//num_areas
    excess = num_pairs % num_areas
    pairs_per_area = [min_pairs for i in range(num_areas)]
    for i in range(excess):
        pairs_per_area[i] += 1
    # It is a mess yet...
    pairs_positions = [(int(np.sum(pairs_per_area[0:i])), int(np.sum(pairs_per_area[0:i+1]))) for i in range(num_areas)]
    return pairs_positions
