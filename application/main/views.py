from __future__ import generators
import math
import random
import difflib
from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from flask_login import login_user, current_user, logout_user, login_required
from ..models import *
from pathlib import Path
import requests
from application.forms import *
import secrets
from PIL import Image
from difflib import get_close_matches, SequenceMatcher
import itertools
from flask_restful import Resource, Api
from flask_cors import CORS
from .forms import LoginForm
from .methods import *
import secrets




main = Blueprint('main',__name__,template_folder='templates')
app_root = Path(__file__).parents[1]
api = Api(main)
CORS(main)
###testing area

@main.route('/new_game', methods=['GET', 'POST'])
def new_game():
    # define game id
    game_id = secrets.token_hex(8)
    # shuffle the deck and store in JSON for gamestate
    deck = ['AH','2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH',
    'AC','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC',
    'AS','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS',
    'AD','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD']
    random.shuffle(deck)
    player1_hand = deck[:10]
    player2_hand = deck[11:21]
    middle_cards = deck[22:23]
    player1_score = 0
    player2_score = 0
    # store the game parameters in JSON
    game = {
    "deck":deck[24:52],
    "player1cards":player1_hand,
    "player1cards":player2_hand,
    "middle_cards":middle_cards,
    "player1_score": 0,
    "player2_score": 0
    }

    #find how to connect with websockets with two seperate players
    player1 = ''
    player2 = ''







    new_game = Game(game_id=game_id, game_data=game_data, player1_id=player1, player2_id=player2)
    db.session.add(new_game)
    db.session.commit()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', game=game)


@main.route('/chat',methods=['GET', 'POST'])
def chat():

    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)




class HelloWorld(Resource):
    def get(self):
        return ({'hello': 'world'})


api.add_resource(HelloWorld,'/hello')


class DrawCard(Resource):
    def get(self):
        return ({'hello': 'world'})



class DiscardCard(Resource):
    def get(self):
        return ({'hello': 'world'})

class PossibleMelds(Resource):
    def get(self):
        return ({'hello': 'world'})

class Tap(Resource):
    def get(self):
        return ({'hello': 'world'})

# this app route will set inital state of game dealing cards, request is send in game JSON and posts to DB as such

    # instead of returning each variable as a individual varible, send it in JSON and parase it this way, we will set functions to update
    # each varible within the JSON and send it back to the server to update the database
    # or we can unpack the JSON here if it is easier to do, determine which way works better for you
    # it may be easier to unpack the JSON here
    # see here how to unpack JSON
