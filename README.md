A package for console application to make a custom swiss tournament system

Features:
- Read fighters list from a text\csv file
- Make pairs
- Save pairs to csv file
- Save fighters standings to csv file (for display) and txt (for statistics)
- Read round results from a csv file

# Installation
1. Install Python 3.7.4 +
2. Clone repository or copy this folder to your computer
3. run tests (not implemented yet)

# Usage:

1. Type in command line
   
    ```bash
    python mws.py fighters_list
    ``` 
    where fighters_list is a text file with the fighters names each in a new row (see tests for examples).
    Now the script is running and fighters are initialized with 12 HP (see response "Tournament ready")
2. To calculate pairs and start a new round, type

    ```bash
   round filename 
   ```
   where 'filename' is a base name to save the round data (standings and pairs)
   Pairs are saved in filename_pairs.csv, and standings in filename_standings.txt
   
 3. After the fights, enter all the results of each fight into the '..._pairs.csv'.
 The results should be negative, as we substract HP from participants. 
 You may as well save it to another file. Save it only as CSV or plain-text file, the app does not understand excel format
 
 4.  Type into command line
    
    ```bash
    update filname_pairs.csv
    ```
    to enter the results of the fights into the tournament.
    A csv file with sorted list of fighters and their HP will be saved, 
    so you could show it to the fencers on the big screen
 5. If the working directory is clear, and the process did not interrupt, 
    you can use automatic filenames typing just:
    ```bash
    round
    update 
    ```
    and adding the fights score in-place into the file 'N_pairs.csv', N is round number
    
 5. If after a certain round the conditions of the finals are met, 
    the app will report it and the list of the finalists into command line.
    Type
    ```bash
    exit
    ```
    to close the app
    
 6. If on a certain stage the results are corrupted, you can always load the state of the tournament,
  by exiting it and entering again with a correct 'filename_standings.txt' as argument:
    ```bash
        python mws.py filename_standings.txt
    ``` 