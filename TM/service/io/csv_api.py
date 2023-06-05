from pathlib import Path
from TM.api.api import Api
from TM.tournament import Fight, Round


class CsvApi(Api):
    """
    This is an input-output to the CSV file in the local filesystem
    By now, it is restricted to one-round fight without doubles and warnings, but can be easily extended if there is need

    It is useful as a backup to store previous rounds untouched.
    """

    def __init__(self, folder, prefix):
        """

        :param folder:
        :param prefix:
        """
        Api.__init__(self)
        self.path = Path(folder)
        self.prefix = prefix

    def write(self, pairs, fighters, round_num):
        filename = self.path/(self.prefix+str(round_num) + '.csv')
        with open(filename, 'w') as dst:
            dst.write('RED, Red HP, Red score, Blue score, Blue HP, BLUE\n')
            for p in pairs:
                dst.write(p.fighter_1 + ',' + str(fighters[p.fighter_1].rating)
                          + ', , , '
                          + str(fighters[p.fighter_2].rating) + ',' + p.fighter_2 + '\n')
        return str(filename)

    @staticmethod
    def parse_results(line):
        split = line.split(',')
        fighter_1 = split[0].rstrip().strip('\"')
        result_1 = -abs(int(split[2].rstrip().strip('\"')))
        fighter_2 = split[5].rstrip().strip('\"')
        result_2 = -abs(int(split[3].rstrip().strip('\"')))
        r = Round(status='finished', score_1=result_1, score_2=result_2)
        return Fight(fighter_1, fighter_2, 'finished', rounds_num=1, rounds = [r],
                     rating_score_1=r.score_1, rating_score_2=r.score_2)

    def read(self, round_num):
        """
        The reading is not connected with writing, it does not use the parameters of the written fights.
        It allows to return any manually changed pairs with the same fighters; however it may cause any kind of problem
        if the results are corrupted.
        :param round_num:
        :return:
        """

        filename = self.path / (self.prefix + str(round_num) + '.csv')
        results = []
        with open(filename) as src:
            for line in src.readlines()[1:]:
                results.append(self.parse_results(line=line))
        return results
