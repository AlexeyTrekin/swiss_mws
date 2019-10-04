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

1. Setup the config.py file. Add all the secretaries' e-mails to 'collaborators'; let doogle_doc=None if you do not have it yet.

1. Type in command line
   
    ```bash
    python mws.py fighters_list
    ``` 
    where fighters_list is a text file with the fighters names each in a new row (see tests for examples).
    Now the script is running and fighters are initialized with 12 HP (see response "Tournament ready")
    
2. To calculate pairs and start a new round, type

    ```bash
   round 
   ```
   The link to the google sheet will be printed into command line
 3. Open the link for the display and the secretaries
 
 3. Enter all the results of each fight into the google sheet. Save the sheet with ctrl+s to ensure all is OK
 
 4.  Type into command line
    
    ```bash
    round
    ```
    to enter the results of the fights into the tournament and make a new sheet in google docs
    
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
    
 6. If on a certain stage the results are corrupted, you can enter the right numbers into the sheet and do
 ```bash
 restart <N>
 ```
 where N is number of correctly entered rounds
