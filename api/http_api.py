import warnings
from flask import Flask, jsonify, request
from random import choice
import string
from api.api import Api
from tournament.fight import Fight
from api.utils import split_to_areas

import threading

def generate_tokens(num_areas: int, length: int=10):
    letters = string.ascii_lowercase
    return [''.join(choice(letters) for i in range(length)) for area in range(num_areas)]


class httpApi:

    def __init__(self, num_areas=1, tokens=None):

        Api.__init__(self)

        self.host ='0.0.0.0'
        self.port = '5000'
        self.pairs = []
        self.round_num = 0
        self.num_areas = num_areas
        if not isinstance(tokens, list) or len(tokens) != num_areas:
            self.tokens = generate_tokens(self.num_areas)
            print('Tokens generated: \n' +
                          '\n'.join(["Area {}: {}".format(area+1, self.tokens[area]) for area in range(num_areas)]))

        else:
            self.tokens = tokens

        app = Flask(__name__)

        @app.route("/heartbeat", methods=['GET'])
        def heartbeat():
            app.logger.info("heartbeat request")
            return "OK"

        @app.route("/next_pair", methods=['GET'])
        def next_pair():
            token = request.args.get('token')
            area = self.check_token(token)
            response = ()
            if area < 0:
                response = jsonify("Incorrect token")
            # Awful mess! Clean it... maybe, make all inside the fights, with 'conducted' flag
            else:
                for p in self.area_pairs(area):
                    for fight in self.fights:
                        if (fight.fighter1, fight.fighter2) == p or (fight.fighter2, fight.fighter1) ==p:
                            continue
                    response = jsonify((p[0].__dict__, p[1].__dict__))
                    break
            # If the request is correct, but no pairs left, the response is empty
            return response

        @app.route("/all_pairs", methods=['GET'])
        def all_pairs():
            token = request.args.get('token')
            area = self.check_token(token)
            if area < 0:
                response = jsonify("Incorrect token")
            else:
                response = jsonify([(p[0].__dict__, p[1].__dict__) for p in self.area_pairs(area)])
            return response

        @app.route("/put_results", methods=['POST'])
        def put_results():
            token = request.args.get('token')
            area = self.check_token(token)
            if area < 0:
                # we still do not accept the results from anauthorized, but will accept the results from any of authorized areas
                return jsonify("Incorrect token")
            new_fight = Fight(**(request.args.to_dict()))
            if any([new_fight.repeats(f) for f in self.fights]):
                return jsonify('The fight is already done in this round, if you need to override it, use other way')

            self.fights.append(new_fight)
            #find the correct fight
            #if (conducted) -> error
            #else -> make conducted, write results
            return jsonify('Results imported')

        # API runs in a separate thread not to block the CLI
        x = threading.Thread(target=app.run, kwargs={'host': self.host,
                                                     'port': self.port,
                                                     'debug': False})
        x.start()

    def check_token(self, token):
        """

        :param token:
        :return: area number for a given token, or -1 if token is incorrect
        """
        # Areas are 1-based
        if not isinstance(token, str):
            return -1
        if token not in self.tokens:
            return -1
        return self.tokens.index(token)

    def area_pairs(self, area):
        area_index = split_to_areas(len(self.pairs), self.num_areas)[area-1]
        return self.pairs[area_index[0]:area_index[1]]

    def check_results(self):
        """
        Only checking if the fights are conducted and the results are here.
        Validation is on the tournament itself
        :return: boolean
        """
        if len(self.fights) != len(self.pairs):
            return False

        # Checking for the correct names, assuming(!) no repeated fights within a round
        for fight in self.fights:
            if (fight.fighter1, fight.fighter2) not in self.pairs and \
                    (fight.fighter2, fight.fighter1) not in self.pairs:
                return False
        return True

    def write(self, pairs, round_num):
        self.pairs = pairs
        self.fights = [Fight(p[0].name, p[1].name, conducted=False) for p in pairs]

        self.round_num = round_num
        return self.host + '/' + self.port


        # Prepare responses and wait for requests


    def read(self, round_num):
        if self.check_results():
            return self.fights
        else:
            return
        # Collect all the responses and take them to the tournament