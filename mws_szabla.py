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
    pass


def set_final(groups, api):
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

    finals = Tournament(rules=TournamentRules(pairing_function=PlayoffPairings(),
                                             start_rating=0,
                                             max_rating=10007,
                                             min_rating=-7,
                                             round_points_cap=7, rating_fn=calc_rating,
                                             rounds_num=1,
                                             time=90),
                       fighters=finalists)
    return finals


def calc_rating(rounds: List[Round]):
    # self.rating_score_1, self.rating_score_2 = rating_fn(self.rounds)
    # Критерии определения лучших: количество побед, количество ничьих, разница нанесенных и пропущенных
    # Поэтому за победу даем 10000, за ничью 1000, разницу учитываем как есть
    # Порядок критериев строго соблюдается если ничьих меньше 10, а баллов меньше 1000, что всегда верно

    assert len(rounds) == 1
    rating_1 = rating_2 = 0

    score_diff = rounds[0].score_1 - rounds[0].score_2
    if score_diff == 0:
        return 1000, 1000
    elif score_diff > 0:
    # Win rating
        rating_1 = 10000 + score_diff
        rating_2 = 0 - score_diff
    else: #score_diff < 0
        rating_1 = 0 + score_diff
        rating_2 = 10000 - score_diff

    return rating_1, rating_2


def start(fighters_file, pairing_function=RoundPairings()):

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
        t = Tournament(rules=TournamentRules(pairing_function=pairing_function,
                                             start_rating=0,
                                             max_rating=10007,
                                             min_rating=-7,
                                             round_points_cap=7, rating_fn=calc_rating,
                                             rounds_num=1,
                                             time=90),
                       fighters=group)
        tournaments.append(t)
    return tournaments


def main():
    #Input check. Too simple to use click or others
    if len(sys.argv) < 2:
        print('There must be parameter - filename')
    fighters_file = sys.argv[1]
    if len(sys.argv) >= 3 and sys.argv[2] == '-v':
        v = True
    else:
        v = False

    #Tournament setup
    ts = start(fighters_file)

    for group_num, t in enumerate(ts):
        print(f'Group {group_num+1}')
        print(t.list_fighters())

    # API setup
    if config.main_api == 'google':
        api_1 = GoogleAPI(config.google_doc, 1,
                           "MwSB", collaborators=config.collaborators)
        api_2 = CsvApi(config.csv_folder, config.csv_name)
    else:
        api_2 = GoogleAPI(config.google_doc, 1,
                           "MwSB", collaborators=config.collaborators)
        api_1 = CsvApi(config.csv_folder, config.csv_name)

    for group_num, t in enumerate(ts):
        print(f'Uploading group {group_num+1} pairs')
        set_group(t, [api_2, api_1], group_num+1)

    print("Tournament ready: group stage")

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
                for group_num, t in enumerate(ts):
                    update(t, api_1, group_num+1)
            except Exception as e:
                print('Failed to read results. Format round results correctly and try again')
                print(str(e))
                continue

            final = set_final(ts, api_1)
            break

        elif split[0] == 'list':
            for group_num, t in enumerate(ts):
                print(f'Group {group_num+1}')
                print(t.list_fighters())

        else:
            print('Unknown command, only \'list\', \'round\' and \'restart <int>\' can be used')

    print('Final stage')
    round_num = 1

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
                update(final, api_1, round_num + len(ts))
                set_round(final, [api_2, api_1], round_num+1+len(ts))
            except Exception as e:
                print('Failed to update round {}. Format round results correctly and try again'.format(round_num))
                print(str(e))
                continue
            round_num += 1

        else:
            print('Unknown command, only \'list\', \'round\' and \'restart <int>\' can be used')



if __name__ == '__main__':
    main()