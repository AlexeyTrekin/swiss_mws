import os
import sys
from pathlib import Path
from tournament import Tournament

def update(t, args):
    # Automatic file name
    if len(args) == 1:
        filename = str(round_num)
    else:
        filename = args[1]

    if not Path(filename).exists():
        filename = filename + '_pairs.csv'
        if not Path(filename).exists():
            print('File {} does not exist'.format(filename))
            return
    try:
        t.results_from_csv(filename)
        t.standings_to_csv(filename.replace('.csv', '_standings_after.csv'))
        print("Results from {} imported\n".format(filename))
        if v:
            print(t.fighters)
    except Exception as e:
        print("Failed to import results from file {}. ".format(filename))
        if v:
            print(str(e))

def set_round(t, args, round_num):
    # Automatic file name
    if len(args) == 1:
        filename = str(round_num)
    else:
        filename = args[1]

    t.swissPairings()
    if v:
        print(t.pairings)
    try:
        t.pairs_to_csv(filename + '_pairs.csv')
        t.standings_to_txt(filename + '_standings.txt')
        print("New pairs calculated, saved to file " + filename + '_pairs.csv')
        # os.system('libreoffice ' + filename + '_pairs.csv')
    except Exception as e:
        print("Failed to write to file {} " + filename + '_pairs.csv')
        if v:
            print(str(e))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('There must be parameter - filename')

    t = Tournament()
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
            round_num += 1
            set_round(t, split, round_num)

        elif split[0] == 'update':
            update(t, split)

        else:
            print('Unknown command, only round and update can be used')