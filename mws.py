import sys
import random

from TM.tournament import Tournament, Fighter, TournamentRules
from TM.api import CsvApi, GoogleAPI
from TM.functional.pairings import SwissPairings, RoundPairings

import config


def remove(tournament: Tournament, v=True):
    """
    moves the fighters with negative score out of the list
    One lucky can stand if there is need for the additional fighter to complete the even number
    :return:
    """
    new_outs = []
    minHP = - tournament.rules.min_rating

    for f in tournament.fighters:
        if f.rating <= 0:
            new_outs.append(f)
        else:
            minHP = min(minHP, f.rating)

    # If there 6 fighters or less, we can make finals:
    if len(tournament.fighters) - len(new_outs) <= 2:
        finalists = [f for f in tournament.fighters if f.rating > 0]
        candidates = [f for f in tournament.fighters if f.rating <= 0]
        if v:
            print("We need to setup an additional round to choose finalists.",
                  "Ready finalists are:")

            print(finalists)
            print('Candidates for additional round:')
            print(candidates)
        return finalists, candidates
    elif len(tournament.fighters) - len(new_outs) <= 6:
        finalists = [f for f in tournament.fighters if f.rating > 0]
        if v:
            print("We have the finalists:")
            print(finalists)
        return finalists, []

    # We leave one lucky fighter from the list if there is uneven number left.
    # TODO: add coefficient to determinate the lucky one.
    elif (len(tournament.fighters) - len(new_outs)) % 2 != 0:
        lucky = random.choice(new_outs)
        if v:
            print('Lucky one: {}'.format(lucky))
        lucky.rating = minHP
        new_outs.remove(lucky)

    for f in new_outs:
        tournament.remove_fighter(f)


def fighter_from_str(line: str, start_rating: int = 0):
    """
    Legacy. For read_figters() from txt file

    String format:
    NAME, <initial rating>
    :return:
    """
    split = line.split(',')
    # This is a very unsafe function, but will do if we only read the properly formatted data
    name = split[0].rstrip()

    # A temporary solution for current functionality
    f = Fighter(name, first_name='', last_name=name)
    if len(split) > 1:
        f.rating = int(split[1].rstrip())
    else:
        f.rating = start_rating

    return f


def update(t, api, round_num):
    t.read_results(api, round_num)
    res = remove(t)
    print("Results for round {} imported\n".format(round_num))
    return res


def set_round(t, apis, round_num):
    # Automatic file name
    t.make_pairs()
    try:
        filename = ''
        for api in apis:
            filename = t.write_pairs(api, round_num)
        # t.pairs_to_csv(filename + '_pairs.csv')
        # t.standings_to_txt(filename + '_standings.txt')
        print("New pairs calculated, saved to file " + filename)
    except Exception as e:
        print("Failed to write to file \n" + str(e))


def set_final(finalists, candidates, api):
    pass


def start(fighters_file, pairing_function=SwissPairings()):

    with open(fighters_file, encoding='utf-8') as src:
        fighters = [fighter_from_str(line, config.hp) for line in src.readlines()]
    t = Tournament(rules=TournamentRules(pairing_function=pairing_function,
                                         start_rating=config.hp,
                                         max_rating=0,
                                         min_rating=-abs(config.cap)),
                   fighters=fighters)
    return t


def restart(fighters_file, api, rounds_passed, pairing_function=SwissPairings()):
    t = start(fighters_file, pairing_function)
    for round_num in range(rounds_passed):
        try:
            update(t, api, round_num+1)
            #print(t.fighters)
        except Exception as e:
            print('Failed to update round {}. Format round results correctly and try again'.format(round_num+1))
            print(str(e))
            return
    return t


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
    if config.pairing_function == 'round':
        pairing_function = RoundPairings()
    else:
        pairing_function = SwissPairings()
    t = start(fighters_file, pairing_function)
    # API setup

    if config.main_api == 'google':
        api_1 = GoogleAPI(config.google_doc, 2,
                           "MwSB", collaborators=config.collaborators)
        api_2 = CsvApi(config.csv_folder, config.csv_name)
    else:
        api_2 = GoogleAPI(config.google_doc, 2,
                           "MwSB", collaborators=config.collaborators)
        api_1 = CsvApi(config.csv_folder, config.csv_name)

    #api_1 = HttpApi(num_areas=config.num_areas)
    #api_2 = CsvApi(config.csv_folder, config.csv_name, decorate=False)

    round_num = 0
    print("Tournament ready")

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
                res = None
                if round_num > 0:
                    res = update(t, api_1, round_num)
                if res is not None:
                    set_final(res[0], res[1], api_1)
                else:
                    set_round(t, [api_2, api_1], round_num+1)
            except Exception as e:
                print('Failed to update round {}. Format round results correctly and try again'.format(round_num))
                print(str(e))
                continue
            round_num += 1

        elif split[0] == 'restart':
            if len(split) > 1:
                try:
                    round_num = int(split[1])
                except ValueError:
                    print('Enter integer number of correctly passed rounds')
                    continue
            # restart the tournament and update it with the specified number of rounds
            t_tmp = restart(fighters_file, api_1, round_num, pairing_function)
            if t_tmp is not None:
                # it means that all the rounds were imported
                # So we can setup a new round
                t = t_tmp
                round_num += 1
                set_round(t, [api_2, api_1], round_num)
            else:
                # Some rounds were not imported correctly, so we can proceed manually,
                # but we do not want to lose the data due to overwriting,
                # so we do not launch the further updates
                round_num += 1
                print('The restart did not complete. '
                      'You can correct the results and restart once again')

        elif split[0] == 'list':
            print(t.list_fighters())

        else:
            print('Unknown command, only \'list\', \'round\' and \'restart <int>\' can be used')


if __name__ == '__main__':
    main()