from flask import session, url_for, request
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import json
from ..models import *
from .methods import *
import secrets
import random
from .forms import *
import os
import sqlite3
lobby_users = []
current_que = {}
current_games={}
link_shared = {}


@socketio.on('joined', namespace='/online')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room','123')
    join_room(room)
    if session.get('name') not in lobby_users:
        lobby_users.append(session.get('name'))
        print(lobby_users)
    current_que_json = json.dumps(current_que, indent=4, sort_keys=True, default=str)
    emit('status', {'msg': session.get('name') + ' has entered the room.','current_que_json':current_que_json}, room=room,current_que=current_que)


@socketio.on('text', namespace='/online')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room','123')
    emit('message', {'msg':session.get('name')+ ":" +  message['msg']}, room=room)


@socketio.on('left', namespace='/online')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room','123')
    leave_room(room)
    if session.get('name') in lobby_users:
        lobby_users.remove(session.get('name'))
        print(lobby_users)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


@socketio.on('join_que', namespace='/online')
def join_que(data):
    room = session.get('room','123')
    if request.sid not in current_que:
        current_que[request.sid] = datetime.now()
    if request.sid in current_que:
        del current_que[request.sid]
        current_que[request.sid] = datetime.now()
    print('User' + session.get('name') + "|||||||||||| has joined the que!||||||||||||||")
    print(current_que)
    current_que_json = json.dumps(current_que, indent=4, sort_keys=True, default=str)
    emit('after_join_que',{'current_que':current_que_json}, room=room,broadcast=True)


@socketio.on('leave_que', namespace='/online')
def leave_que(data):
    room = session.get('room','123')
    # if session.get('name') not in current_que:
    #     current_que[session.get('name')] = datetime.now()
    if request.sid in current_que:
        del current_que[request.sid]
    print('User' + session.get('name') + "|||||||||||| has left the que!||||||||||||||")
    print(current_que)
    current_que_json = json.dumps(current_que, indent=4, sort_keys=True, default=str)
    emit('after_leave_que',{'current_que':current_que_json}, room=room,broadcast=True)

@socketio.on('link_shared', namespace='/online')
def link_shared(data):
    room = session.get('room','123')
    game_id = secrets.token_hex(8)
    if request.sid not in current_que:
        current_que[request.sid] = datetime.now()
    if request.sid in current_que:
        del current_que[request.sid]
        current_que[request.sid] = datetime.now()
    emit('link_sharing',{'current_que':current_que_json}, room=room,broadcast=True)


# @socketio.on('connect_users', namespace='/online')
# def connect_users(data):
#     # room = 'que_room'
#     #build dictionary to connect users
#     room = session.get('room')
    # while True:
    #     connect_users = {}
    #     if len(current_que) >= 2:
    #         oldest_user = min(current_que, key=current_que.get)
    #         del current_que[oldest_user]
    #         second_oldest_user = min(current_que, key=current_que.get)
    #         del current_que[second_oldest_user]
    #         connect_users[oldest_user] = "player1"
    #         connect_users[second_oldest_user] = "player2"
            #emit connected dictionary with users in socket, can redirect to new_game route
            #via web sockets on front end, send to new game
#     emit('connect_users',data,{'current_que':current_que,'connet_users':connect_users},room=room,broadcast=True)


@socketio.on('connect_users', namespace='/online')
def connect_users(data):
    # room = 'que_room'
    #build dictionary to connect users
    room = session.get('room','123')
    current_que_json = json.dumps(current_que, indent=4, sort_keys=True, default=str)
    print('looking for match')
    print('looking for match',current_que)
    print('current_que_json',current_que_json)
    if len(current_que) >= 2:
        connect_users = {}
        oldest_user = min(current_que, key=current_que.get)
        del current_que[oldest_user]
        second_oldest_user = min(current_que, key=current_que.get)
        del current_que[second_oldest_user]
        connect_users['player1']=oldest_user
        connect_users['player2']=second_oldest_user
        # connect_users[oldest_user] = "player1"
        # connect_users[second_oldest_user] = "player2"
        connect_users_json = json.dumps(connect_users, indent=4, sort_keys=True, default=str)
        # player1 = json.dumps(connect_users['player1'], indent=4, sort_keys=True, default=str)
        # player2 = json.dumps(connect_users['player2'], indent=4, sort_keys=True, default=str)

        player1=oldest_user
        player2=second_oldest_user
        print(current_games)

            # define game id
        game_id = secrets.token_hex(8)
        current_games[game_id]=[oldest_user,second_oldest_user]
        print('game_id',game_id)
        print('game_id',type(game_id))

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
        play_to = 100
        game = {
        "deck":deck[24:52],
        "player1cards":player1cards,
        "player2cards":player2cards,
        "middle_cards":middle_cards,
        "player1_score": 0,
        "player2_score": 0,
        "play_to":play_to,
        "player1melds": best_hand(possible_hands(player1cards)),
        "player2melds": best_hand(possible_hands(player2cards)),
        "player1":player1,
        "player2":player2,
        #checking in the knocking screen, if someones score is greater than play to, it will return true
        "endgame" : False
        }

        #find how to connect with websockets with two seperate players
        #connect player 1 and player 2 via websockets and store game ID, then redirect to
        # /game route for game play
        # player1 = ''
        # player2 = ''
        session['game_id']=game_id
        new_game = Game(game_id=game_id, game_data=game)
        db.session.add(new_game)
        db.session.commit()
        print('game_id',game_id)
        room=game_id
        # if form.validate_on_submit():
        #     session['name'] = form.name.data
        #     session['room'] = form.room.data
        #     return redirect(url_for('.chat'))
        # elif request.method == 'GET':
        #     form.name.data = session.get('name', '')
        #     form.room.data = session.get('room', '')
        print('connect_users',connect_users)
        join_room(game_id)
        socketio.server.enter_room(connect_users['player1'], game_id, namespace='/online')
        socketio.server.enter_room(connect_users['player2'], game_id, namespace='/online')
        emit('join_game',{'current_que':current_que_json,'connect_users':connect_users,'url': url_for('main.game',game_id=game_id),'game':game,'game_id':game_id,'room':room},room=connect_users['player2'])
        emit('join_game',{'current_que':current_que_json,'connect_users':connect_users,'url': url_for('main.game',game_id=game_id),'game':game,'game_id':game_id,'room':room},room=connect_users['player1'])
        print('old river nigger')
        #emit connected dictionary with users in socket, can redirect to new_game route
        #via web sockets on front end, send to new game


@socketio.on('get_game_data', namespace='/online')
def get_game_data(data):
    print('get_game_data')
    game_id=data['game_id']
    session['room'] = game_id
    room=game_id
    player_name = request.sid
    print(session['room'])
    print(request.sid)
    connect_users = data['connect_users']
    current_que_json = json.dumps(current_que, indent=4, sort_keys=True, default=str)
    current_game = Game.query.filter_by(game_id=game_id).first()
    player1=current_game.game_data['player1']
    player2=current_game.game_data['player2']
    player = ""
    if player_name == player1:
        player="player1"
    if player_name == player2:
        player="player2"
    deck=current_game.game_data['deck']
    player1cards = current_game.game_data['player1cards']
    player2cards = current_game.game_data['player2cards']
    print('getting game data',current_game)
    middle_cards = current_game.game_data['middle_cards']
    player1melds = current_game.game_data['player1melds']
    player2melds = current_game.game_data['player2melds']
    print('player1melds',player1melds)
    print('player2melds',player2melds)

    # current_game = Game.query.filter_by(id=id).first()
    # deck = current_game['deck']
    # session['name']=data['data']
    # player_name=name
    emit('joined_game',{'player1cards':player1cards,'player2cards':player2cards,'deck':deck,'middle_cards':middle_cards,'player1':player1,'player2':player2,'current_que':current_que_json,'room':room, 'player':player,'player1melds':player1melds,'player2melds':player2melds},room=player_name)




@socketio.on('draw_card', namespace='/online')
def draw_card(data):
    game_id=session.get('room')
    game_id_query = f'"{game_id}"'
    print('game_id',game_id)
    #model stored for the inital game data


    work_dir = os.path.dirname(os.path.realpath(__file__))
    work_dir = work_dir[:-4]
    print('work_dir',work_dir)
    con = sqlite3.connect(work_dir + "/site.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # game_id = '"6a6af791519774d7"'
    query = """
        SELECT
            *
        FROM
            Game
        WHERE
            game_id = {game_id_query}
    """.format(game_id_query=game_id_query)
    cur.execute(query)
    current_game = cur.fetchall()
    print('current game', current_game)
    # current_game = [dict(row) for row in cur.fetchall()]
    game_data=[]
    for row in current_game:
        print(row[0],row[1])
        print(row[2])
        game_data = row[2]
    game_data = (json.loads(game_data))
    print('game_data', game_data)
    print(type(game_data))
    # print ('sql',current_game)


    # current_game = Game.query.filter_by(game_id=game_id).first()
    room=game_id
    print('game_data2' ,game_data)
    print(room)
    #player name when someone card
    #who drew the card on the html needs to be sent back
    player_name = request.sid
    print(player_name)
    #Pulling the game JSON out of the game data model so we can manipulate the deck way we want
    player = ""

    # game_data = current_game.game_data


    player1 = game_data['player1']
    print('player1',player1)

    player2 = game_data['player2']
    print('player2',player2)
    if player_name == player1:
        player="player1"
        player1cards = data['current_hand']
        player2cards = game_data['player2cards']
    if player_name == player2:
        player="player2"
        player2cards = data['current_hand']
        player1cards = game_data['player1cards']
    print('player_name',player_name)
    print('player1',player1)
    print('player2',player2)
    #taking the deck out of the JSON from the game data
    deck = game_data['deck']
    print('deck ',deck)
    middle_cards = game_data['middle_cards']
    # player1cards = game_data['player1cards']
    print('player1 Cards',player1cards)
    # player2cards = game_data['player2cards']
    print('player2 Cards',player2cards)
    player1score = game_data['player1_score']
    player2score = game_data['player2_score']
    play_to = game_data['play_to']
    #we need to define in the frontend which player is which
    if player_name == player1:
        player1cards.append(deck[0:1][0])
    if player_name == player2:
        player2cards.append(deck[0:1][0])
    print('card ',deck[0:1][0], 'drawn by ', player_name)
    #del the card from the deck
    del deck[0:1]
    print('deck ', deck)
    print('player1 Cards',player1cards)
    print('player2 Cards',player2cards)
    #redefine the game json with the updated variables
    # play_to = request.form['play_to']
    player1melds = best_hand(possible_hands(player1cards))
    player2melds = best_hand(possible_hands(player2cards))
    play_to = 6
    game = {
    "deck":deck,
    "player1cards":player1cards,
    "player2cards":player2cards,
    "middle_cards":middle_cards,
    "player1_score": player1score,
    "player2_score": player2score,
    "player1melds": player1melds,
    "player2melds": player2melds,
    "player1":player1,
    "player2":player2,
    "play_to": play_to,
    "endgame" : False
    }
    print('player1melds',player1melds)
    print('player2melds',player2melds)
    print ('game', game)
    game_data = game
    # str(json.dumps(game_data))
    print(type(game_data))
    print ('game', game)
    print('game_data3',game_data)

    cur.execute('''UPDATE Game SET game_data = ? WHERE game_id = ? ''', (json.dumps(game_data,), game_id))
    middle_cards = game['middle_cards']

    # curs.executemany('Update data (loanId, noteAmount) '
    #                  'VALUES (:loanId,:noteAmount)', json.loads(...)['myNotes'])
    con.commit()

    # db.session.commit()
    #we return the game json to the front end with the updated values
    #in this case we are only sending back player1s cards as they were the only ones to change perhaps
    emit('card_drawn',{'player1cards':player1cards,'player2cards':player2cards,'deck':deck,'middle_cards':middle_cards,'player1':player1,'player2':player2,'player':player,'player1melds':player1melds,'player2melds':player2melds, 'room':room},room=game_id)



#logic after user pulls a card, discard must be written on front end, so if user has 11 cards, logic has to be written on frontend
@socketio.on('discard', namespace='/online')
def discard(data):
    game_id=session.get('room')
    print('game_id',game_id)
    game_id_query = f'"{game_id}"'
    # current_game = Game.query.filter_by(game_id=game_id).first()

    work_dir = os.path.dirname(os.path.realpath(__file__))
    work_dir = work_dir[:-4]
    print('work_dir',work_dir)
    con = sqlite3.connect(work_dir + "/site.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # game_id = '"6a6af791519774d7"'
    query = """
        SELECT
            *
        FROM
            Game
        WHERE
            game_id = {game_id_query}
    """.format(game_id_query=game_id_query)
    cur.execute(query)
    current_game = cur.fetchall()
    #we request the players name from the frontend, we define the form as "discard"
    player_name = request.sid
    room=game_id
    #send back the card as a form from the frontend, define as varible card, we look for form
    #value 'card'
    card = data['card']
    player = ""

    print('card ',card)
    game_data=[]
    for row in current_game:
        print(row[0],row[1])
        print(row[2])
        game_data = row[2]
    game_data = (json.loads(game_data))

    # game_data = current_game.game_data
    player1 = game_data['player1']
    player2 = game_data['player2']
    if player_name == player1:
        player="player1"
        player1cards = data['current_hand']
        player2cards = game_data['player2cards']
    if player_name == player2:
        player="player2"
        player2cards = data['current_hand']
        player1cards = game_data['player1cards']
    print('player_name',player_name)
    print('player1',player1)
    print('player2',player2)
    #taking the deck out of the JSON from the game data
    deck = game_data['deck']
    print('deck ',deck)
    middle_cards = game_data['middle_cards']
    # player1cards = game_data['player1cards']
    print('player1 Cards',player1cards)
    print ('card 1 ', player1cards[0])
    # player2cards = game_data['player2cards']
    print('player2 Cards',player2cards)
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
    print('player1 Cards',player1cards)
    print('player2 Cards',player2cards)
    player1melds = best_hand(possible_hands(player1cards))
    player2melds = best_hand(possible_hands(player2cards))
    game = {
    "deck":deck,
    "player1cards":player1cards,
    "player2cards":player2cards,
    "middle_cards":middle_cards,
    "player1_score": player1score,
    "player2_score": player2score,
    "player1melds": player1melds,
    "player2melds": player2melds,
    "player1":player1,
    "player2":player2,
    "play_to": play_to,
    "endgame" : False

    }
    game_data = game
    cur.execute('''UPDATE Game SET game_data = ? WHERE game_id = ? ''', (json.dumps(game_data,), game_id))
    middle_cards = game['middle_cards']

    # curs.executemany('Update data (loanId, noteAmount) '
    #                  'VALUES (:loanId,:noteAmount)', json.loads(...)['myNotes'])
    con.commit()
    emit('card_discarded',{'player1cards':player1cards,'player2cards':player2cards,'deck':deck,'middle_cards':middle_cards,'player1':player1,'player2':player2,'player':player,'player1melds':player1melds,'player2melds':player2melds,'room':room},room=game_id)


@socketio.on('draw_middle_card', namespace='/online')
def draw_middle_card(data):
    # current_game = Game.query.filter_by(game_id=game_id).first()
    game_id=session.get('room')
    print('game_id',game_id)
    game_id_query = f'"{game_id}"'
    # current_game = Game.query.filter_by(game_id=game_id).first()

    work_dir = os.path.dirname(os.path.realpath(__file__))
    work_dir = work_dir[:-4]
    print('work_dir',work_dir)
    con = sqlite3.connect(work_dir + "/site.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # game_id = '"6a6af791519774d7"'
    query = """
        SELECT
            *
        FROM
            Game
        WHERE
            game_id = {game_id_query}
    """.format(game_id_query=game_id_query)
    cur.execute(query)
    current_game = cur.fetchall()
    #we request the players name from the frontend, we define the form as "discard"
    player_name = request.sid
    room=game_id
    player = ""

# if request.method == 'POST':
    #finding the player who did this action
    # player_name = request.form["draw_card"]
    game_data=[]
    for row in current_game:
        print(row[0],row[1])
        print(row[2])
        game_data = row[2]
    game_data = (json.loads(game_data))

    player1 = game_data['player1']
    player2 = game_data['player2']
    if player_name == player1:
        player="player1"
        player1cards = data['current_hand']
        player2cards = game_data['player2cards']
    if player_name == player2:
        player="player2"
        player2cards = data['current_hand']
        player1cards = game_data['player1cards']
    player1melds = best_hand(possible_hands(player1cards))
    player2melds = best_hand(possible_hands(player2cards))
    #deconstructing the JSON
    deck = game_data['deck']
    print('deck ',deck)
    middle_cards = game_data['middle_cards']
    # player1cards = game_data['player1cards']
    print('player1 Cards',player1cards)
    print ('card 1 ', player1cards[0])
    # player2cards = game_data['player2cards']
    print('player2 Cards',player2cards)
    player1score = game_data['player1_score']
    player2score = game_data['player2_score']
    play_to = game_data['play_to']
    #finding which player did this action

    if player_name == player1:
        #appending the middle card to the list
        #not defining a card above such as we did with discard
        player1cards.append(middle_cards[len(middle_cards)-1:len(middle_cards)][0])
    if player_name == player2:
        player2cards.append(middle_cards[len(middle_cards)-1:len(middle_cards)][0])
    del middle_cards[len(middle_cards)-1:len(middle_cards)]
    game = {
    "deck":deck,
    "player1cards":player1cards,
    "player2cards":player2cards,
    "middle_cards":middle_cards,
    "player1_score": player1score,
    "player2_score": player2score,
    "player1melds": player1melds,
    "player2melds": player2melds,
    "player1":player1,
    "player2":player2,
    "play_to": play_to,
    "endgame" : False
    }
    # player1melds = game['player1melds']
    # player2melds = game['player2melds']
    game_data = game
    cur.execute('''UPDATE Game SET game_data = ? WHERE game_id = ? ''', (json.dumps(game_data,), game_id))
    middle_cards = game['middle_cards']

    # curs.executemany('Update data (loanId, noteAmount) '
    #                  'VALUES (:loanId,:noteAmount)', json.loads(...)['myNotes'])
    con.commit()
    emit('drawn_middle_card',{'player1cards':player1cards,'player2cards':player2cards,'deck':deck,'middle_cards':middle_cards,'player1':player1,'player2':player2,'player':player,'player1melds':player1melds,'player2melds':player2melds,'room':room},room=game_id)




@socketio.on('knock', namespace='/online')
def knock(data):
    # current_game = Game.query.filter_by(game_id=game_id).first()
    #initilze points for each user for this round to 0

    game_id=session.get('room')
    print('game_id',game_id)
    game_id_query = f'"{game_id}"'
    # current_game = Game.query.filter_by(game_id=game_id).first()

    work_dir = os.path.dirname(os.path.realpath(__file__))
    work_dir = work_dir[:-4]
    print('work_dir',work_dir)
    con = sqlite3.connect(work_dir + "/site.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # game_id = '"6a6af791519774d7"'
    query = """
        SELECT
            *
        FROM
            Game
        WHERE
            game_id = {game_id_query}
    """.format(game_id_query=game_id_query)
    cur.execute(query)
    current_game = cur.fetchall()
    #we request the players name from the frontend, we define the form as "discard"
    player_name = request.sid
    room=game_id
    player = ""

# if request.method == 'POST':
    #finding the player who did this action
    # player_name = request.form["draw_card"]
    game_data=[]
    for row in current_game:
        print(row[0],row[1])
        print(row[2])
        game_data = row[2]
    game_data = (json.loads(game_data))

    player1 = game_data['player1']
    player2 = game_data['player2']
    if player_name == player1:
        player="player1"
        player1cards = data['current_hand']
        player2cards = game_data['player2cards']
    if player_name == player2:
        player="player2"
        player2cards = data['current_hand']
        player1cards = game_data['player1cards']
    print('cards', player1cards, player2cards)
    player1melds = best_hand(possible_hands(player1cards))
    player2melds = best_hand(possible_hands(player2cards))
    knocker_points = 0
    opponent_points = 0
    print('player',player)
    deck = game_data['deck']
    print('deck ',deck)
    middle_cards = game_data['middle_cards']
    print('player1 Cards',player1cards)
    print ('card 1 ', player1cards[0])
    print('player2 Cards',player2cards)
    player1score = game_data['player1_score']
    player2score = game_data['player2_score']
    play_to = game_data['play_to']

    #finding the player who did this action
    knock_name = request.sid
    #player hand should be of JSON format {meld1:[CA,CA,CA], meld2: [CA,CA,CA,CA], meld3: [] , deadwood:[CA,CA,CA]}
    if player=='player1':
        knocker_hand = player1melds
        opponent_hand = player2melds
    if player=='player2':
        knocker_hand = player2melds
        opponent_hand = player1melds
    #if there is no deadwood, player has called gin
    print('knockerhand',knocker_hand)
    print('opponent_hand',opponent_hand)
    if len(knocker_hand['deadwood']) == 0:
        knocker_points = 25 + count_cards(opponent_hand['deadwood'])


    else:
        if len(knocker_hand['meld1']) == 3:
            possible_melds_1 = possible_melds(knocker_hand['meld1']+ opponent_hand['deadwood'])
            if possible_melds_1[0] == knocker_hand['meld1']:
                pass
            else:
                for meld in possible_melds_1:
                    for card in meld:
                        if card in opponent_hand['deadwood']:
                            opponent_hand['deadwood'].remove(card)


        if len(knocker_hand['meld2']) == 3:
            possible_melds_1 = possible_melds(knocker_hand['meld2']+ opponent_hand['deadwood'])
            if possible_melds_1 == knocker_hand['meld2']:
                pass
            else:
                for meld in possible_melds_1:
                    for card in meld:
                        if card in opponent_hand['deadwood']:
                            opponent_hand['deadwood'].remove(card)


        if len(knocker_hand['meld3']) == 3:
            possible_melds_1 = possible_melds(knocker_hand['meld3']+ opponent_hand['deadwood'])
            if possible_melds_1 == knocker_hand['meld3']:
                pass
            else:
                for meld in possible_melds_1:
                    for card in meld:
                        if card in opponent_hand['deadwood']:
                            opponent_hand['deadwood'].remove(card)

        #logic had to be added for your animations, showing who won and lost, after this stage
        if count_cards(knocker_hand['deadwood']) < count_cards(opponent_hand['deadwood']):
            print('knocker<opponent',knocker_hand['deadwood'],opponent_hand['deadwood'])
            knocker_points = (count_cards(opponent_hand['deadwood']) - count_cards(knocker_hand['deadwood']))
            print('knocker<opponent',count_cards(knocker_hand['deadwood']),count_cards(opponent_hand['deadwood']))


        if count_cards(knocker_hand['deadwood']) > count_cards(opponent_hand['deadwood']):
            opponent_points = count_cards(knocker_hand['deadwood']) - count_cards(opponent_hand['deadwood'])+10
            # opponent_points = knocker_points + 10
            print('knocker<opponent',knocker_hand['deadwood'],opponent_hand['deadwood'])
            print('knocker<opponent',count_cards(knocker_hand['deadwood']),count_cards(opponent_hand['deadwood']))
        if count_cards(knocker_hand['deadwood']) == count_cards(opponent_hand['deadwood']):
            pass


    # game_data = current_game.game_data()
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
    print('scores',player1score,player2score)
    endgame = game_data['endgame']
    if player1score > game_data['play_to']:
        endgame == True
    if player2score > game_data['play_to']:
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
        game_data = game
        cur.execute('''UPDATE Game SET game_data = ? WHERE game_id = ? ''', (json.dumps(game_data,), game_id))
        middle_cards = game['middle_cards']

        # curs.executemany('Update data (loanId, noteAmount) '
        #                  'VALUES (:loanId,:noteAmount)', json.loads(...)['myNotes'])
        con.commit()
        emit('knocked',{'player1cards':player1cards,'player2cards':player2cards,'deck':deck,'middle_cards':middle_cards,'player1':player1,'player2':player2,'player':player,'player1melds':player1melds,'player2melds':player2melds,'player1score':player1score,'player2score':player2score,'knocker_points':knocker_points,'opponent_points':opponent_points,'room':room},room=game_id)
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


    if endgame == True:
        game = {"player1_score": player1score,
        "player2_score": player2score,
        "play_to": play_to,
        "player1":player1,
        "player2":player2}
        game_data = game
        cur.execute('''UPDATE Game SET game_data = ? WHERE game_id = ? ''', (json.dumps(game_data,), game_id))
        middle_cards = game['middle_cards']

        # curs.executemany('Update data (loanId, noteAmount) '
        #                  'VALUES (:loanId,:noteAmount)', json.loads(...)['myNotes'])
        con.commit()
        emit('knocked',{'player1cards':player1cards,'player2cards':player2cards,'deck':deck,'middle_cards':middle_cards,'player1':player1,'player2':player2,'player':player,'player1melds':player1melds,'player2melds':player2melds,'player1score':player1score,'player2score':player2score,'room':room},room=game_id)

@socketio.on('redeal', namespace='/online')
def redeal(data):
        # current_game = Game.query.filter_by(game_id=game_id).first()
    game_id=session.get('room')
    print('game_id',game_id)
    game_id_query = f'"{game_id}"'
    # current_game = Game.query.filter_by(game_id=game_id).first()

    work_dir = os.path.dirname(os.path.realpath(__file__))
    work_dir = work_dir[:-4]
    print('work_dir',work_dir)
    con = sqlite3.connect(work_dir + "/site.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # game_id = '"6a6af791519774d7"'
    query = """
        SELECT
            *
        FROM
            Game
        WHERE
            game_id = {game_id_query}
    """.format(game_id_query=game_id_query)
    cur.execute(query)
    current_game = cur.fetchall()
    #we request the players name from the frontend, we define the form as "discard"
    player_name = request.sid
    room=game_id
    player = ""

# if request.method == 'POST':
    #finding the player who did this action
    # player_name = request.form["draw_card"]
    game_data=[]
    for row in current_game:
        print(row[0],row[1])
        print(row[2])
        game_data = row[2]
    game_data = (json.loads(game_data))

    player1 = game_data['player1']
    player2 = game_data['player2']

    deck = ['AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH',
    'AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC',
    'AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS',
    'AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD']
    random.shuffle(deck)
    player1cards = deck[:10]
    player2cards = deck[11:21]
    middle_cards = deck[22:23]
    player1score = game_data['player1_score']
    player2score = game_data['player2_score']
    play_to = game_data['play_to']
    # store the game parameters in JSON

    #take in values from websockets to find the score to
    play_to = game_data['play_to']
    player1melds = best_hand(possible_hands(player1cards))
    player2melds = best_hand(possible_hands(player2cards))
    game = {
    "deck":deck[24:52],
    "player1cards":player1cards,
    "player2cards":player2cards,
    "middle_cards":middle_cards,
    "player1_score": player1score,
    "player2_score": player2score,
    "play_to":play_to,
    "player1melds": player1melds,
    "player2melds": player2melds,
    "player1":player1,
    "player2":player2,
    #checking in the knocking screen, if someones score is greater than play to, it will return true
    "endgame" : False
    }
    game_data = game
    cur.execute('''UPDATE Game SET game_data = ? WHERE game_id = ? ''', (json.dumps(game_data,), game_id))
    middle_cards = game['middle_cards']

    # curs.executemany('Update data (loanId, noteAmount) '
    #                  'VALUES (:loanId,:noteAmount)', json.loads(...)['myNotes'])
    con.commit()
    emit('redeal_cards',{'player1cards':player1cards,'player2cards':player2cards,'deck':deck,'middle_cards':middle_cards,'player1':player1,'player2':player2,'player':player,'player1melds':player1melds,'player2melds':player2melds,'player1score':player1score,'player2score':player2score,'room':room},room=game_id)
