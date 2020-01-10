import numpy as np

def split_to_areas(num_pairs, num_areas):
    """
    Evenly splits pairs for the areas.
    :param pairs_num:
    :param areas_num:
    :return:
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
