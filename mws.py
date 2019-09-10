import sys
from pathlib import Path
from tournament import Tournament

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
    while wait:
        command = input()

        if command == 'exit':
            wait = False
            break

        split = command.split(' ')
        if len(split) < 2:
            continue


        if split[0] == 'round':
            t.swissPairings()
            if v:
                print(t.pairings)
            try:
                t.pairs_to_csv(split[1] + '_pairs.csv')
                t.standings_to_txt(split[1] + '_standings.txt')
                print("New pairs calculated\n")
            except Exception as e:
                print("Failed to write to file {}. \n".format(split[1]))
                if v:
                    print(str(e))

        elif split[0] == 'update':
            if not Path(split[1]).exists():
                print('File {} does not exist'.format(split[1]))
            else:
                try:
                    t.results_from_csv(split[1])
                    t.standings_to_csv(split[1].replace('.csv', '_standings_after.csv'))
                    print("Results from {} imported\n".format(split[1]))
                    if v:
                        print(t.fighters)

                except Exception as e:
                    print("Failed to import results from file {}. ".format(split[1]))
                    if v:
                        print(str(e))

        else:
            print('Unknown command, only round and update can be used')