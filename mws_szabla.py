import sys

from typing import List

from TM.tournament import Tournament, Fighter, TournamentRules, Round
from TM.api import CsvApi, GoogleAPI
from TM.pairings import RoundPairings, PlayoffPairings

import config


def update(t, api, round_num):
    t.read_results(api, round_num)
    print("Results of group stage imported\n".format(round_num))
    return


def set_group(t, apis, group_num):
    # Automatic file name
    t.make_pairs()
    try:
        filename = ''
        for api in apis:
            filename = t.write_pairs(api, group_num)
        # t.pairs_to_csv(filename + '_pairs.csv')
        # t.standings_to_txt(filename + '_standings.txt')
        print("Pairs calculated, saved to file " + filename)
    except Exception as e:
        print("Failed to write to file \n" + str(e))


def set_round(t, apis, round_num):
    t.make_pairs()
    try:
        filename = ''
        for api in apis:
            filename = t.write_pairs(api, 10+round_num)
        # t.pairs_to_csv(filename + '_pairs.csv')
        # t.standings_to_txt(filename + '_standings.txt')
        print("Pairs calculated, saved to file " + filename)
    except Exception as e:
        print("Failed to write to file \n" + str(e))

    # Write the data
    pass


def set_final(groups):
    print('Finalizing')
    all_fighters = []
    for group in groups:
        # We normalize the rating on the number of fights in a group
        fighters = group.fighters
        for f in fighters:
            f.rating = f.rating/(len(fighters) -1)

        all_fighters += fighters
    all_fighters.sort(key=lambda x: x.rating, reverse=True)

    print(all_fighters)

    if len(all_fighters) >= 32:
        finalists = all_fighters[:32]
    elif len(all_fighters) >= 16:
        finalists = all_fighters[:16]
    elif len(all_fighters) >= 8:
        finalists = all_fighters[:8]
    elif len(all_fighters) >= 4:
        finalists = all_fighters[:4]
    else:
        raise ValueError('We need at least 4 fighters to start the playoff!')

    final = Tournament(rules=TournamentRules(pairing_function=PlayoffPairings(),
                                             start_rating=0,
                                             max_rating=10007,
                                             min_rating=-7,
                                             round_points_cap=7, rating_fn=calc_rating,
                                             rounds_num=3,
                                             time=90),
                       fighters=finalists)
    return final


def calc_rating(rounds: List[Round]):
    # self.rating_score_1, self.rating_score_2 = rating_fn(self.rounds)
    # Критерии определения лучших: количество побед, количество ничьих, разница нанесенных и пропущенных
    # Поэтому за победу даем 10000, за ничью 1000, разницу учитываем как есть
    # Порядок критериев строго соблюдается если ничьих меньше 10, а баллов меньше 1000, что всегда верно

    if len(rounds) == 1:
        # Selections (1-round fight)
        score_diff = rounds[0].score_1 - rounds[0].score_2
        if score_diff == 0:
            # Draw rating
            return 1000, 1000
        elif score_diff > 0:
        # Win rating + score diff rating
            rating_1 = 10000 + score_diff
            rating_2 = 0 - score_diff
        else: #score_diff < 0
            rating_1 = 0 + score_diff
            rating_2 = 10000 - score_diff

    else:
        # Multi-round fights for finals
        wins_1 = wins_2 = 0
        for round in rounds:
            if round.score_1 - round.score_2 > 0:
                wins_1 +=1
            elif round.score_1 - round.score_2 < 0:
                wins_2 +=1
        # Add 10000 to the winner's rating
        if wins_1 > wins_2:
            # Modify it to match snake-like playoff pairings?
            return 10000, 0
        else:
            return 0, 10000
    return rating_1, rating_2


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
                                             round_points_cap=7, rating_fn=calc_rating,
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


def group_stage(groups, api):
    while True:
        command = input()
        split = command.split(' ')

        if command == 'exit':
            return
        # ignore accidental 'enter' without warnings
        elif command == '':
            continue

        elif split[0] == 'final':
            try:
                for group_num, t in enumerate(groups):
                    update(t, api, group_num+1)
            except Exception as e:
                print('Failed to read results. Format results correctly and try again')
                print(str(e))
                continue

            final = set_final(groups)
            return final

        elif split[0] == 'list':
            for group_num, t in enumerate(groups):
                print(f'Group {group_num+1}')
                print(t.list_fighters())

        else:
            print('Unknown command, only \'list\', \'final\' and \'exit\'  can be used')


def final_stage(final, api):
    round_num=1
    set_group(final, [api], round_num + 10)
    while True:
        command = input()
        split = command.split(' ')

        if command == 'exit':
            return
        # ignore accidental 'enter' without warnings
        elif command == '':
            continue

        elif split[0] == 'round':
            try:
                update(final, api, round_num + 10)
                set_group(final, [api], round_num+11)
            except Exception as e:
                print('Failed to update round {}. Format round results correctly and try again'.format(round_num))
                print(str(e))
                continue
            round_num += 1

        elif split[0] == 'list':
            print(final.list_fighters())

        else:
            print('Unknown command, only \'list\', \'round\' and \'exit\' can be used')


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

    for group_num, t in enumerate(ts):
        print(f'Group {group_num+1}')
        print(t.list_fighters())

    # API setup
    api = GoogleAPI(config.google_doc, 1, "MwSzabla", collaborators=config.collaborators)
    #api_2 = CsvApi(config.csv_folder, config.csv_name)

    if start_new:
        start(ts, api)
        print("Tournament ready: group stage")
    else:
        print(f"Tournament ready from existing spreadsheet, the data is in {api.SpreadsheetURL}")

    final = group_stage(ts, api)
    if final:
        print('Final stage')
        final_stage(final, api)

    print('Exiting')


if __name__ == '__main__':
    main()