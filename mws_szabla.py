import sys

from typing import List

from TM.tournament import Tournament, Fighter, TournamentRules
from TM.api import GoogleAPI
from TM.pairings import RoundPairings

import config

from stages import group_stage, playoff_stage, final_stage, set_group
from calc_rating import calc_rating_selections


def tournament_from_file(fighters_file):

    # Groups of fighters are divided by blank lines

    groups = []
    new_group = []
    with open(fighters_file, encoding='utf-8') as src:
        for line in src.readlines():
            if line.strip() == '':
                groups.append(new_group)
                new_group = []
            else:
                name = line.split(',')[0].rstrip()
                new_group.append(Fighter(name, first_name='', last_name=name))
    # Add the last group in case there is no last empty string
    if new_group != []:
        groups.append(new_group)
    tournaments = []
    for group in groups:
        t = Tournament(rules=TournamentRules(pairing_function=RoundPairings(),
                                             start_rating=0,
                                             max_rating=10007,
                                             min_rating=-7,
                                             round_points_cap=7, rating_fn=calc_rating_selections,
                                             rounds_num=1,
                                             time=90),
                       fighters=group)
        tournaments.append(t)

    return tournaments


def start(ts: List[Tournament], api):
    """
    Fills the table with new figthers dta
    :param ts:
    :param api:
    :return:
    """
    for group_num, t in enumerate(ts):
        print(f'Uploading group {group_num+1} pairs')
        set_group(t, [api], group_num+1)


def main():
    #Input check. Too simple to use click or others
    if len(sys.argv) < 2:
        print('There must be parameter - filename')
    fighters_file = sys.argv[1]

    start_new = True
    #skip_selections = False

    if len(sys.argv) >= 3:
        if sys.argv[2] == '-r':
            # Restart from existing data
            start_new = False
        #elif sys.argv[2] == '-f':
            # Start finals from the list of fighters
        #    skip_selections = True
        #elif sys.argv[2] == '-rf' or sys.argv[2] == '-fr':
        #    skip_selections = True
        #    start_new = False


    #Tournament setup
    ts = tournament_from_file(fighters_file)

    #for group_num, t in enumerate(ts):
    #    print(f'Group {group_num+1}')
    #    print(t.list_fighters())

    # API setup
    api = GoogleAPI(config.google_doc, num_areas=1, num_rounds=1,
                    name="MwSzabla", collaborators=config.collaborators)

    if start_new:
        start(ts, api)
        print("Tournament ready: group stage")
    else:
        print(f"Tournament ready from existing spreadsheet, the data is in {api.SpreadsheetURL}")

    playoff = group_stage(ts, api)
    if playoff:
        final = playoff_stage(playoff, api)
        if final:
            final_stage(final, api)
    print('Exiting')


if __name__ == '__main__':
    main()