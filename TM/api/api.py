from typing import List, Dict
from TM.tournament import Fighter, Fight


class Api:

    def __init__(self):
        self.fighters = []
        self.pairs = []
        pass

    def write(self,
              pairs: List[Fight],
              fighters: Dict[str, Fighter],
              round_num: int,
              **kwargs):
        """
        :param pairs: a list of Fight instances - empty, for the further processing and filling
        :param fighters: a list of Fighters, that covers all the members in pairs, with all the additional Fighter data
        :param round_num: round number
        :return: an ID of the output device (URL, or filename)
        """
        raise NotImplementedError

    def read(self,
             round_num: int) -> List[Fight]:
        """

        :param round_num:
        :return: a list of Fight`s
        """
        raise NotImplementedError