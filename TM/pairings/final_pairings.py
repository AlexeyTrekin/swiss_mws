from .pairings import Pairings


class FinalPairings(Pairings):
    def __call__(self, fighters):
        fighters.sort(key=lambda f:f.rating, reverse=True)
        return [(fighters[0], fighters[1]),(fighters[2], fighters[3])]

