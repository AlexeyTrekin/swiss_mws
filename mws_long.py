import sys

from typing import List

from TM.tournament import Fighter
from TM.api import GoogleAPI

import config

from stages import selection_stage


def fighters_from_file(fighters_file):

    # Groups of fighters are divided by blank lines

    fighters = []
    with open(fighters_file, encoding='utf-8') as src:
        for line in src.readlines():
            if line.strip() != '':
                name = line.split(',')[0].rstrip()
                fighters.append(Fighter(name, first_name='', last_name=name, rating=config.hp))

    return fighters


def main():

    # Input check. Too simple to use click or others
    if len(sys.argv) < 2:
        print('There must be parameter - filename')
    fighters_file = sys.argv[1]

    # skip_selections = False

    if len(sys.argv) >= 4 and sys.argv[2] == '-r':
        # Restart from existing data
        restart = sys.argv[3]
    else:
        restart = False
    # Tournament setup
    fighters = fighters_from_file(fighters_file)

    # API setup
    api = GoogleAPI(config.google_doc, num_areas=1, num_rounds=1,
                    name="MwS", collaborators=config.collaborators)

    finalists, tiebreak = selection_stage(fighters, api, restart=restart)
    if tiebreak:
        print(f'Something strange happened! Tiebreak should not happen')
    else:
        finalists.sort(key=lambda x: x.rating, reverse=True)
        for f in finalists:
            print(f)

    print('Exiting')


if __name__ == '__main__':
    main()