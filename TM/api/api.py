from typing import List, Tuple
from TM.tournament import Fighter

class Api:

    def __init__(self):
        pass

    def write(self,
              pairs: List[Tuple[Fighter,Fighter]],
              round_num: int):
        """
        :param pairs: a list of tuples of strings ('fighter1', 'fighter2')
        #TODO: Make it of class Fighter
        :param round_num: round number
        :return: an ID of the output device (URL, or filename)
        """
        raise NotImplementedError

    def read(self,
             round_num: int):
        """

        :param round_num:
        :return: a list of results, which are tuples of tuples ((fighter1, fighter1_score), (fighter2, fighter2_score))
        # TODO: add extendable results with warnings and doubles. Class 'Fight' maybe?
        """
        raise NotImplementedError