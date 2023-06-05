A server application for HEMA tournament management.

It stores all the information about the current tournament.
REST api allows to connect with client app (secretary web page) and
- get the fights to conduct
- save the results to the server

# Requirements: 
- Docker engine + docker compose plugin. 
- Internet connection with static IP address or local network to connect the secretary tables

# Secretary app
Use https://github.com/AlexeyTrekin/mws-tablo
(currently not working with this version)

# How to manage your own tournament

## Configure the tournament:
Open `config.py` file and set the values you need.
Important options:
- stages: describes the stages of the tournament with different rules (pools, playoffs, finals etc.).
  - every stage depends on the previous one
  - every stage has its criteria for transition to the next stage
  - stages have their own rules (number or rounds, rating rules, pairing functions etc)
- secretaries: initializes the secretary credentials (login, password) for every area. They will connect with these logins from their apps
- admin: administrator api token to manage the tournament stages

You can use sample configs from `configs/` directory as examples, or as ready tournament rulesets
## Add fighters
Write them to the file "fighters.txt" one in a string

## Start the tournament:
Run 
`docker compose up`

## Connect from secretary workspaces
Use login/password pairs set in config

## Connect the tournament display app
Write it?

# License
MIT

# Contributing
If you have found an error, or have feature request, use github issues on this project.

If you want to help, we are open to pull-requests with valuable features that correspond to the project goals.ß
