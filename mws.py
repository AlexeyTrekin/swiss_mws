import sys
from tournament import Tournament
from csv_api import CsvApi
from google_api import GoogleAPI


def update(t, api, round_num):
    t.read_results(api, round_num)
    res = t.remove()
    print("Results for round {} imported\n".format(round_num))
    return res


def set_round(t, apis, round_num):
    # Automatic file name
    t.swissPairings()
    try:
        for api in apis:
            filename = t.write_pairs(api, round_num)
        #t.pairs_to_csv(filename + '_pairs.csv')
        #t.standings_to_txt(filename + '_standings.txt')
        print("New pairs calculated, saved to file " + filename)
        # os.system('libreoffice ' + filename + '_pairs.csv')
    except Exception as e:
        print("Failed to write to file")


def set_final(finalists, candidates, api):
    pass


def start(fighters_file):
    t = Tournament()
    t.read_fighters(fighters_file)
    return t


def restart(fighters_file, api, rounds_passed):
    t = start(fighters_file)
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
    t = start(fighters_file)
    # API setup
    csv_api = CsvApi('/home/trekin/Data/test', 'mws1', decorate=False)
    google_api = GoogleAPI("1P4cP-V8FWYa7Jwu1IEEWSQ1dmMG9vu6El-x54xspifQ", 2,
                           "test", collaborators=[])
    #google_api = GoogleAPI(None, 2, "test", collaborators=['alexey.trekin@gmail.com'])
    #
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
                    res = update(t, google_api, round_num)
                if res is not None:
                    set_final(res[0], res[1], google_api)
                else:
                    set_round(t, [csv_api, google_api], round_num+1)
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
            t_tmp = restart(fighters_file, google_api, round_num)
            if t_tmp is not None:
                # it means that all the rounds were imported
                # So we can setup a new round
                t = t_tmp
                round_num += 1
                set_round(t, [csv_api, google_api], round_num)
            else:
                # Some rounds were not imported correctly, so we can proceed manually,
                # but we do not want to lose the data due to overwriting,
                # so we do not launch the further updates
                round_num += 1
                print('The restart did not complete. '
                      'You can correct the results and restart once again')

        else:
            print('Unknown command, only round and restart <int> can be used')


if __name__ == '__main__':
    main()