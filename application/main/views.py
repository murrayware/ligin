import random
from flask import render_template,request,redirect,url_for,flash,session,current_app
from flask_login import login_user, current_user, logout_user, login_required
from ..models import *
from pathlib import Path
import requests
from .forms import *
import secrets
from .methods import *
import secrets
from . import main
from flask_login import login_user, current_user, logout_user, login_required
from flask_session import Session



#need to take sockets in here with users with events function for connect users
@main.route('/new_game', methods=['GET', 'POST'])
def new_game():
    # define game id
    game_id = secrets.token_hex(8)
    # shuffle the deck and store in JSON for gamestate
    deck = ['AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH',
    'AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC',
    'AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS',
    'AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD']
    random.shuffle(deck)
    player1cards = deck[:10]
    player2cards = deck[11:21]
    middle_cards = deck[22:23]
    player1_score = 0
    player2_score = 0
    # store the game parameters in JSON

    #take in values from websockets to find the score to
    play_to = ""
    game = {
    "deck":deck[24:52],
    "player1cards":player1cards,
    "player2cards":player2cards,
    "middle_cards":middle_cards,
    "player1_score": 0,
    "player2_score": 0,
    "play_to":play_to,
    "player1melds": possible_melds(player1cards),
    "player2melds": possible_melds(player2cards),
    "player1":'',
    "player2":'',
    #checking in the knocking screen, if someones score is greater than play to, it will return true
    "endgame" : False
    }

    #find how to connect with websockets with two seperate players
    #connect player 1 and player 2 via websockets and store game ID, then redirect to
    # /game route for game play
    player1 = ''
    player2 = ''

    new_game = Game(game_id=game_id, game_data=game)
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


@main.route('/')
@main.route('/online')
def online():
    """Chat room. The user's name and room must be stored in
    the session."""
    if current_user.is_authenticated:
        session['name'] = current_user.username
        name = current_user.username
    else:
        name = 'Guest' + str(secrets.token_hex(8))
        session['name'] = name
    # room = session.get('room', '123')
    return render_template('online.html', name=name)

@main.route('/test')
def test():

    return render_template('testcards.html')





#this route handles game and all attributes within, API calls will all happen within this template
@main.route('/game/<game_id>', methods=['GET', 'POST'])
def game(game_id):
    current_game = Game.query.filter_by(game_id=game_id).first()
    player1=current_game.game_data['player1']
    player2=current_game.game_data['player2']
    deck=current_game.game_data['deck']
    session['game_id']=current_game.game_id
    game_id=current_game.game_id
    room = session.get('room', '123')
    return render_template('game.html',game=current_game,
        player1=player1,player2=player2,deck=deck,game_id=game_id,room=room)


@main.route('/game/draw_card/<id>')
def draw_card(id):
    #model stored for the inital game data
    current_game = Game.query.filter_by(game_id=game_id).first()
    if request.method == 'POST':
        #player name when someone card
        #who drew the card on the html needs to be sent back
        player_name = request.sid
        #Pulling the game JSON out of the game data model so we can manipulate the deck way we want
        game_data = current_game.game_data()
        player1 = game_data['player1']
        player2 = game_data['player2']
        #taking the deck out of the JSON from the game data
        deck = game_data['deck']
        middle_cards = game_data['middle_cards']
        player1cards = game_data['player1cards']
        player2cards = game_data['player2cards']
        player1score = game_data['player1_score']
        player2score = game_data['player2_score']
        play_to = game_data['play_to']
        #we need to define in the frontend which player is which
        if player_name == player1:
            player1cards.append(deck[0:1][0])
        if player_name == player2:
            player2cards.append(deck[0:1][0])
        #del the card from the deck
        del deck[0:1]
        #redefine the game json with the updated variables
        play_to = request.form['play_to']
        game = {
        "deck":deck,
        "player1cards":player1cards,
        "player2cards":player2cards,
        "middle_cards":middle_cards,
        "player1_score": player1score,
        "player2_score": player2score,
        "player1melds": possible_melds(player1cards),
        "player2melds": possible_melds(player2cards),
        "player1":player1,
        "player2":player2,
        "play_to": play_to,
        "endgame" : False
        }
        current_game.game = game
        db.session.commit()
        #we return the game json to the front end with the updated values
        #in this case we are only sending back player1s cards as they were the only ones to change perhaps
        return(game['player1cards'])



#logic after user pulls a card, discard must be written on front end, so if user has 11 cards, logic has to be written on frontend
@main.route('/game/discard/<id>')
def discard(id):
    current_game = Game.query.filter_by(game_id=game_id).first()
    if request.method == 'POST':
        #we request the players name from the frontend, we define the form as "discard"
        player_name = request.form["discard"]
        #send back the card as a form from the frontend, define as varible card, we look for form
        #value 'card'
        card = request.form['card']
        game_data = current_game.game_data()
        player1 = game_data['player1']
        player2 = game_data['player2']
        deck = game_data.game['deck']
        middle_cards = game_data.game['middle_cards']
        player1cards = game_data.game['player1cards']
        player2cards = game_data.game['player2cards']
        player1score = game_data['player1_score']
        player2score = game_data['player2_score']
        play_to = game_data['play_to']
        if player_name == player1:
            #remove the variable 'card' from the form taken from the frontend
            player1cards.remove(card)
            #add the card removed to the middle card list
            middle_cards.append(card)
        if player_name == player2:
            player2cards.remove(card)
            middle_cards.append(card)
        game = {
        "deck":deck,
        "player1cards":player1cards,
        "player2cards":player2cards,
        "middle_cards":middle_cards,
        "player1_score": player1score,
        "player2_score": player2score,
        "player1melds": possible_melds(player1cards),
        "player2melds": possible_melds(player2cards),
        "player1":player1,
        "player2":player2,
        "play_to": play_to,
        "endgame" : False

        }
        current_game.game = game
        db.session.commit()
        return game


@main.route('/game/draw_middle_card/<id>')
def draw_middle_card(id):
    current_game = Game.query.filter_by(game_id=game_id).first()
    if request.method == 'POST':
        #finding the player who did this action
        player_name = request.form["draw_card"]
        game_data = current_game.game_data()
        player1 = game_data['player1']
        player2 = game_data['player2']
        #deconstructing the JSON
        deck = current_game.game['deck']
        middle_cards = current_game.game['middle_cards']
        player1cards = current_game.game['player1cards']
        player2cards = current_game.game['player2cards']
        player1score = game_data['player1_score']
        player2score = game_data['player2_score']
        play_to = game_data['play_to']
        #finding which player did this action

        if player_name == player1:
            #appending the middle card to the list
            #not defining a card above such as we did with discard
            player1cards.append(middle_cards[len(middle_cards)-1:len(middle_cards)])
        if player_name == player2:
            player2cards.append(middle_cards[len(middle_cards)-1:len(middle_cards)])
        del middle_cards[len(middle_cards)-1:len(middle_cards)]
        game = {
        "deck":deck,
        "player1cards":player1cards,
        "player2cards":player2cards,
        "middle_cards":middle_cards,
        "player1_score": player1score,
        "player2_score": player2score,
        "player1melds": possible_melds(player1cards),
        "player2melds": possible_melds(player2cards),
        "player1":player1,
        "player2":player2,
        "play_to": play_to,
        "endgame" : False
        }
        current_game.game = game
        db.session.commit()
        return game




@main.route('/new_deal', methods=['GET', 'POST'])
def new_deal(id):
    current_game = Game.query.filter_by(game_id=game_id).first()
    # shuffle the deck and store in JSON for gamestate
    deck = ['AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH',
    'AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC',
    'AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS',
    'AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD']
    random.shuffle(deck)
    player1cards = deck[:10]
    player2cards = deck[11:21]
    middle_cards = deck[22:23]
    player1_score = current_game.game['player1score']
    player2_score = current_game.game['player2score']
    # store the game parameters in JSON

    #take in values from websockets to find the score to
    play_to = current_game.game['play_to']
    game = {
    "deck":deck[24:52],
    "player1cards":player1cards,
    "player2cards":player2cards,
    "middle_cards":middle_cards,
    "player1_score": player1_score,
    "player2_score": player2_score,
    "play_to":play_to,
    "player1melds": possible_melds(player1cards),
    "player2melds": possible_melds(player2cards),
    #checking in the knocking screen, if someones score is greater than play to, it will return true
    "endgame" : False
    }
    return render_template('index.html', game=game)


@main.route('/game/knock/<id>')
def knock(id):
    current_game = Game.query.filter_by(game_id=game_id).first()
    #initilze points for each user for this round to 0
    knocker_points = 0
    opponent_points = 0
    if request.method == 'POST':
        #finding the player who did this action
        knock_name = request.form["knock"]
        #player hand should be of JSON format {meld1:[CA,CA,CA], meld2: [CA,CA,CA,CA], meld3: [] , deadwood:[CA,CA,CA]}
        knocker_hand = request.form["cards"]
        opponent_hand = request.form["opponent_hand"]
        #if there is no deadwood, player has called gin
        if len(knocker_hand['deadwood']) == 0:
            knocker_points = 25 + count_cards(opponent_hand['deadwood'])


        else:
            if len(knocker_hand['meld1']) == 3:
                possible_melds = possible_melds(knocker_hand['meld1']+ opponent_hand['deadwood'])
                if possible_melds[0] == knocker_hand['meld1']:
                    pass
                else:
                    for meld in possible_melds:
                        for card in meld:
                            if card in opponent_hand['deadwood']:
                                opponent_hand['deadwood'].remove(card)


            if len(knocker_hand['meld2']) == 3:
                possible_melds = possible_melds(knocker_hand['meld2']+ opponent_hand['deadwood'])
                if possible_melds == knocker_hand['meld2']:
                    pass
                else:
                    for meld in possible_melds:
                        for card in meld:
                            if card in opponent_hand['deadwood']:
                                opponent_hand['deadwood'].remove(card)


            if len(knocker_hand['meld3']) == 3:
                possible_melds = possible_melds(knocker_hand['meld3']+ opponent_hand['deadwood'])
                if possible_melds == knocker_hand['meld3']:
                    pass
                else:
                    for meld in possible_melds:
                        for card in meld:
                            if card in opponent_hand['deadwood']:
                                opponent_hand['deadwood'].remove(card)

            #logic had to be added for your animations, showing who won and lost, after this stage
            if count_cards(knocker_hand['deadwood']) > count_cards(opponent_hand['deadwood']):
                knocker_points = count_cards(knocker_hand['deadwood']) - count_cards(opponent_hand['deadwood'])


            if count_cards(knocker_hand['deadwood']) < count_cards(opponent_hand['deadwood']):
                opponent_points = (count_cards(opponent_hand['deadwood']) - count_cards(knocker_hand['deadwood']))
                opponent_points = knocker_points + 10


            if count_cards(knocker_hand['deadwood']) == count_cards(opponent_hand['deadwood']):
                pass


        game_data = current_game.game_data()
        player1 = game_data['player1']
        player2 = game_data['player2']
        #deconstructing the JSON
        player1score = game_data['player1_score']
        player2score = game_data['player2_score']

        if knock_name == player1:
            player1score = player1score + knocker_points
            player2score = player2score + opponent_points


        if knock_name == player2:
            player2score = player2score + knocker_points
            player1score = player1score + opponent_points


        if player1score > current_game.game['play_to']:
            endgame == True
        if player2score > current_game.game['play_to']:
            endgame == True
        else:
            endgame == False


        if endgame == False:
            game = {
            "deck":[],
            "player1cards":[],
            "player2cards":[],
            "middle_cards":[],
            "player1_score": player1score,
            "player2_score": player2score,
            "player1":player1,
            "player2":player2,
            "play_to": play_to,
            "endgame" : False
            }
            current_game.game = game
            db.session.commit()
            return render_template('new_deal.html')


        if endgame == True:
            game = {"player1_score": player1score,
            "player2_score": player2score,
            "play_to": play_to}
            current_game.game = game
            db.session.commit()
            return render_template('gameover.html')




