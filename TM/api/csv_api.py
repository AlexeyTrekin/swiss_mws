from pathlib import Path

def decorate(filename):
    """
    We do not want to lose any of the data due to overwriting
    :param filename:
    :return:
    """
    if Path(filename).exists:
        noext = filename[:filename.rfind('.')]
        ext = filename[filename.rfind('.'):]
        decorated = filename
        i=1
        while Path(decorated).exists():
            decorated = noext + str(i) + ext
            i += 1
        return decorated
    else:
        return filename

class CsvApi:

    def __init__(self, folder, prefix, decorate=False):
        self.decorate = decorate
        self.path = Path(folder)
        self.prefix = prefix

    def write(self, pairs, round_num):
        filename = self.path/(self.prefix+str(round_num) + '.csv')
        with open(filename, 'w') as dst:
            dst.write('RED, Red HP, Red score, Blue score, Blue HP, BLUE\n')
            for p in pairs:
                dst.write(p[0].name + ',' + str(p[0].rating) + ', , , ' + str(p[1].rating) + ',' + p[1].name + '\n')
        return str(filename)

    def read(self, round_num):
        filename = self.path / (self.prefix + str(round_num) + '.csv')
        results = []
        with open(filename) as src:
            for p in src.readlines()[1:]:
                split = p.split(',')
                results.append(
                    ((split[0].rstrip().strip('\"'), int(split[2].rstrip().strip('\"'))),
                               (split[5].rstrip().strip('\"'), int(split[3].rstrip().strip('\"'))))
                )
        return results


"""
    def standings_to_txt(self, filename: str):
        with open(decorate(filename), 'w') as dst:
            for f in self.fighters:
                dst.write(f.to_str() + '\n')

    def all_to_txt(self, filename: str):
        with open(decorate(filename), 'w') as dst:
            for f in self.fighters:
                dst.write(f.to_str() + '\n')
        for f in self.outs:
            dst.write(f.to_str() + '\n')

    def standings_to_csv(self, filename):

        with open(decorate(filename), 'w') as dst:
            for f in sorted(self.fighters, key=hp):
                dst.write(repr(f) + '\n')

"""