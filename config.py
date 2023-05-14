# Google spreadsheet ID, or None if we want to create a new
google_doc = None #'1i9yWRAvFGu0Esct6Yvw-Drq8-pKydmJ37N5-LLh8W7Y'

# list of google accounts to share the new doc with
collaborators = ['alexey.trekin@gmail.com'] #, 'mwstablo1@gmail.com', 'mwstablo2@gmail.com ']

# Base name for csv files
csv_name = 'mws'

# Folder for csv files
csv_folder = './'

# randomize the pairs in the first round or not
random_pairs = False

# number of the fight areas to spread the fights to
num_areas = 1

# default HP for a fighter
hp = 24

# the cap is maximum allowed amount of points given
cap = -6

#
pairing_function = 'swiss'
# maximum difference between the fighters rating for the pair
# If it cannot be achieved, classic ("old") swiss pairing is used
max_diff = 2
#

# size of the final group
min_finalists = 1
max_finalists = 16
