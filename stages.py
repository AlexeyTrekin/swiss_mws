from TM.tournament import Tournament, TournamentRules, Fighter
from TM.pairings import PlayoffPairings, RoundPairings, SwissPairings
from calc_rating import calc_rating
import random
import config


# ============ IO ================ #

def remove(tournament: Tournament, v=True, min_finalists=config.min_finalists, max_finalists=config.max_finalists):
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

    # If there are 6 fighters or less, we can make finals:

    if len(tournament.fighters) - len(new_outs) < min_finalists:
        finalists = [f for f in tournament.fighters if f.rating > 0]
        candidates = [f for f in tournament.fighters if f.rating <= 0]
        if v:
            print("We need to setup an additional round to choose finalists.",
                  "Ready finalists are:")

            print(finalists)
            print('Candidates for additional round:')
            print(candidates)
        return finalists, candidates

    elif len(tournament.fighters) - len(new_outs) <= max_finalists:
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


def update(t: Tournament, api, round_num):
    t.read_results(api, round_num)
    print("Results imported\n".format(round_num))


def set_round(t, apis, round_num):
    # Automatic file name
    t.make_pairs()
    try:
        filename = ''
        for api in apis:
            filename = t.write_pairs(api, round_num)
        print("New pairs calculated, saved to file " + filename)
    except Exception as e:
        print("Failed to write to file \n" + str(e))

    return round_num

'''
def set_round(t, apis, round_num=None):

    if len(t.fighters) in [8, 16, 32]:
        # Remove the fighters who lost previous playoff round
        removed = []
        for f in t.fighters:
            if f.rating < 0:
                removed.append(f)
        if len(removed) > 0:
            print('Removing fighters:')
            for f in removed:
                t.remove_fighter(f)
                print(f'{f.name}')

    t.make_pairs()
    try:
        filename = ''
        # We encode the playoff stage in the sheet ID as 10 + 4/2 = 1/2; 10+8/2 = 1/4, 10+32/2 = 1/16
        if not round_num:
            round_num = 10 + len(t.fighters) // 2

        for api in apis:
            filename = t.write_pairs(api, round_num)
        # t.pairs_to_csv(filename + '_pairs.csv')
        # t.standings_to_txt(filename + '_standings.txt')
        print("Pairs calculated, saved to file " + filename)
    except Exception as e:
        print("Failed to write to file \n" + str(e))

    return round_num
'''
# ================================================= #
# =========== Stage definitions =================== #


def selection_stage(fighters, api, restart):

    t = Tournament(rules=TournamentRules(pairing_function=SwissPairings(),
                                         start_rating=config.hp,
                                         max_rating=0,
                                         min_rating=-abs(config.cap),
                                         rating_fn=calc_rating,
                                         ),
                  stage_base_name='Раунд ',
                  fighters=fighters)

    if restart:
        raise NotImplementedError('Restart not implemented yet, start a new tournament instead')
    else:
        round_num = 1
        set_round(t, [api], round_num)

    while True:

        command = input()
        split = command.split(' ')

        if command == 'exit':
            exit()
        # ignore accidental 'enter' without warnings
        elif command == '':
            continue

        elif split[0] == 'round':
            try:
                update(t, api, round_num)
                res = remove(t)
                if res is not None:
                    return res
            except Exception as e:
                print('Failed to update round {}. Format round results correctly and try again'.format(round_num))
                print(str(e))
                continue
            try:
                set_round(t, [api], round_num + 1)
            except:
                print(f'Failed to set a new round. Restart the tournament from round {round_num}')
            round_num += 1

        elif split[0] == 'list':
            print(t.list_fighters())

        else:
            print('Unknown command, only \'list\', \'final\' and \'exit\'  can be used')


def tiebreak_stage(tiebreak, api, min_finalists, max_finalists, round_num):
    # If the tournament is ready (for the multi-stage tiebreaks) we must be able to start from exising one
    if isinstance(tiebreak, Tournament):
        t = tiebreak
    else:
        if len(tiebreak) % 2 != 0:
            tiebreak.append(Fighter(fighter_id='Dummy',
                                    first_name='', last_name='Dummy',
                                    rating=config.hp_tiebreak))

        t = Tournament(rules=TournamentRules(pairing_function=SwissPairings(),
                                         start_rating=config.hp_tiebreak,
                                         max_rating=0,
                                         min_rating=-abs(config.cap),
                                         rating_fn=calc_rating
                                         ),
                   stage_base_name='Стыковочные ',
                   fighters=tiebreak)

    api.num_rounds = t.rules.rounds_num
    set_round(t, [api], round_num)
    while True:

        command = input()
        split = command.split(' ')

        if command == 'exit':
            exit()
        # ignore accidental 'enter' without warnings
        elif command == '':
            continue

        elif split[0] == 'round':
            try:
                update(t, api, round_num)
                res = remove(t, min_finalists=min_finalists, max_finalists=max_finalists)
                if res is not None:
                    # Case when there is less fighters than needed or OK
                    if len(res[1]) == 0:  # we have correct number of finalists
                        return res[0]
                    else:
                        return res[0] + tiebreak_stage(res[1], api,  # recoursively launch the next tiebreak round
                                                            min_finalists - len(res[0]), # with the number of fighters left to select
                                                            max_finalists - len(res[0]), round_num+1)
                else:
                    # case when there still are fighters to remove
                    return tiebreak_stage(t, api,  # recoursively launch the next tiebreak round
                                            min_finalists,  # with the number of fighters left to select
                                            max_finalists, round_num+1)
            except Exception as e:
                print('Failed to update round {}. Format round results correctly and try again'.format(round_num))
                print(str(e))
                continue

        elif split[0] == 'list':
            print(t.list_fighters())

        else:
            print('Unknown command, only \'list\', \'final\' and \'exit\'  can be used')


def final_stage(finalists, api):
    round_num = 100
    final = Tournament(rules=TournamentRules(pairing_function=RoundPairings(),
                                             start_rating=config.hp_finals,
                                             max_rating=0,
                                             min_rating=-abs(config.cap),
                                             rating_fn=calc_rating,
                                             rounds_num=1,
                                             time=90),
                       stage_base_name='Финал ',
                       fighters=finalists)

    api.num_rounds = final.rules.rounds_num
    set_round(final, [api], round_num)
    while True:

        command = input()
        split = command.split(' ')

        if command == 'exit':
            exit()
        # ignore accidental 'enter' without warnings
        elif command == '':
            continue

        elif split[0] == 'list':
            print(final.list_fighters())

        elif split[0] == 'final':
            try:
                update(final, api, round_num)
            except Exception as e:
                print('Failed to update round {}. Format round results correctly and try again'.format(round_num))
                print(str(e))
                continue
            else:
                print('Final rating is:')
                print(final.list_fighters())
    return
