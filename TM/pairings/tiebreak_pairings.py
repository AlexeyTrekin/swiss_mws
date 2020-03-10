from .pairings import Pairings


class TieBreakPairings(Pairings):
    """
    The goal is to get 'slots' fighters with minimum fights
    """
    def __init__(self, slots):
        """

        :param slots: Number of slots in finals to fill with the fighters.
        """
        super().__init__()
        self.slots = slots

    def __call__(self, fighters):
        if len(fighters) < self.slots:
            raise ValueError(f'Not enough fighters {len(fighters)} to fill the {self.slots} places in finals')
