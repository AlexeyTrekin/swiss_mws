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


