# Google spreadsheet ID, or None if we want to create a new
google_doc = None #'1QApXX4W2u1Kk6yBz74g-AYp_2tjcvXvUlw3SMaUC-58' #"1P4cP-V8FWYa7Jwu1IEEWSQ1dmMG9vu6El-x54xspifQ"

# list of google accounts to share the new doc with
collaborators = ['alexey.trekin@gmail.com']

# Base name for csv files
csv_name = 'mws'

# Folder for csv files
csv_folder = '/home/trekin/Data/test'

# main api - google or csv
main_api = 'google'

# randomize the pairs in the first round or not
random_pairs = False

# number of the fight areas to spread the fights to
num_areas = 1

# default HP for a fighter
hp = 20
# the cap is maximum allowed amount of points given
cap = 6