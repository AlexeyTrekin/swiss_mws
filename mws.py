import sys
from pathlib import Path
from tournament import Tournament
from csv_api import CsvApi


def update(t, api, round_num):
    t.read_results(api, round_num)
    print("Results for round {} imported\n".format(round_num))
    if v:
        print(t.fighters)


def set_round(t, api, round_num):
    # Automatic file name
    t.swissPairings()
    if v:
        print(t.pairings)
    try:
        filename = t.write_pairs(api, round_num)
        #t.pairs_to_csv(filename + '_pairs.csv')
        #t.standings_to_txt(filename + '_standings.txt')
        print("New pairs calculated, saved to file " + filename)
        # os.system('libreoffice ' + filename + '_pairs.csv')
    except Exception as e:
        print("Failed to write to file")
        if v:
            print(str(e))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('There must be parameter - filename')

    t = Tournament()
    csv_api = CsvApi('/home/trekin/Data/test', 'mws1', decorate=False)

    t.read_fighters(sys.argv[1])
    print("Tournament ready")
    if len(sys.argv) >= 3 and sys.argv[2] == '-v':
        v = True
    else:
        v = False

    wait = True
    round_num = 0
    while wait:
        command = input()
        split = command.split(' ')

        if command == 'exit':
            wait = False
            break
        # ignore accidental 'enter' without warnings
        elif command == '':
            continue

        elif split[0] == 'round':
            if round_num > 0:
                try:
                    update(t, csv_api, round_num)
                except Exception as e:
                    print('Failed to update round {}. Format round results correctly and try again'.format(round_num))
                    print(str(e))
                    continue
            round_num += 1
            set_round(t, csv_api, round_num)

        else:
            print('Unknown command, only round and update can be used')