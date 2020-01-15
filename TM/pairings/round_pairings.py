def dumb_round_pairings(fighters):
    """
    Formally, it gives every fight, but in useless order
    :param fighters:
    :return:
    """
    pairings = []
    f_num = len(fighters)
    for f1 in range(f_num):
        for f2 in range(f1):
            pairings.append((fighters[f1], fighters[f2]))
    return pairings


def subround_consequent(fighters):
    # Return list of the consequent pairings, like (i, i+1)
    pairings = []
    i = 0

    # Odd pairs (1,2),(3,4),... (7,1)
    while i < len(fighters):
        pairings.append((fighters[i], fighters[(i + 1) % len(fighters)]))
        i += 2
    # Even pairs (2,3), (4,5), ... (8,1)
    i = 1
    while i < len(fighters):
        if i == len(fighters) - 1:
            # Special case - when the number of fighters is even,
            # we want the last pair to be inserted in the previous position
            # to avoid consequent fights for the first fighter
            pairings.insert(-1, (fighters[i], fighters[(i + 1) % len(fighters)]))
        else:
            pairings.append((fighters[i], fighters[(i + 1) % len(fighters)]))
        i += 2
    # Special case - when the number of fighters is even,

    return pairings


def subround_half_shift(fighters):
    pairings = []
    if len(fighters) % 2 != 0:
        return []
    for i in range(len(fighters) // 2):
        pairings.append((fighters[i], fighters[i + len(fighters) // 2]))
    return pairings


def subround(fighters, shift):
    L = len(fighters)

    if shift == 1:
        # If the pairs are consequent, general algorithm would make 2 fights in a row for one fighter
        # So it is a special case
        return subround_consequent(fighters)
    if L % 2 == 0 and L // 2 == shift:
        return subround_half_shift(fighters)
    pairings = []
    for i in range(L):
        pairings.append((fighters[i], fighters[(i + shift) % L]))
    return pairings


def round_pairings(fighters):
    """
    Make pairings for every pair in 'fighters', arranging it so that none will have 2 figts in a row
    (except case with 3 or 4 fighters)
    :param fighters: list of fighters
    :return: list of pairs (tuples)
    """
    # Special cases
    if len(fighters) < 2:
        return []
    if len(fighters) == 2:
        return [(fighters[0], fighters[1])]

    pairings = []
    for shift in range(1, len(fighters) // 2 + 1):
        pairings += subround(fighters, shift)
    return pairings