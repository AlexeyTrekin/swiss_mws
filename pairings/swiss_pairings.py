from tournament.fighter import Fighter, hp


def alreadyPlayed(player1: Fighter, player2: Fighter) -> bool:
    """Have these two players already played in this tour?

        A boolean indicating if this would be a rematch
    """
    return player1.played(player2) > 0 or player2.played(player1) > 0


def swissPairings(fighters):
    """Returns a list of pairs of players for the next round of a match in this tour.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal HP, that is, a player adjacent
    to him or her in the standings.  Rematches are not allowed, so all pairings are new
    (excluding situations when all pairs have matched, see Fighter.normalize_played )

    Returns: a list of tuples of fighters
    """

    if len(fighters) % 2 != 0 or len(fighters) == 0:
        raise ValueError("Number of fighters is {}, does not suit for pairing".format(len(self.fighters)))

    standings = sorted(fighters, key=hp)

    pairings = []

    for i in range(0, len(standings), 2):
        for j in range(i + 1, len(standings)):
            if not alreadyPlayed(standings[i], standings[j]):
                # good pair found, swap into place then break the inner loop
                while j > i + 1:
                    standings[j - 1], standings[j] = standings[j], standings[j - 1]
                    j -= 1
                break
        pairings.append((standings[i], standings[i + 1]))
    return pairings
