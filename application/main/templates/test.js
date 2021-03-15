                socket.on('card_drawn', function(data){
                    console.log('drawing card')

                    console.log(player1_buttons)
                    console.log(player2_buttons)

                    const deck = document.getElementById('deck');
                    const player1cards = document.getElementById('player1cards');
                    const player2cards = document.getElementById('player2cards');
                    // const room_name = document.getElementById('room');
                    const middle_cards = document.getElementById('middle_cards');
                    // const player1melds = document.getElementById('player1melds');
                    // const player2melds = document.getElementById('player2melds');
                    // player1melds.innerHTML = data.player1melds
                    // player2melds.innerHTML = data.player2melds
                    // player1melds_list = data.player1melds
                    // player2melds_list = data.player2melds
                    if(data.middle_cards[data.middle_cards.length -1] !== undefined){
                        var middle_card = Flask.url_for("static", {"filename": "cards/"+data.middle_cards[data.middle_cards.length -1]+".png"})
                        middle_cards.innerHTML = "<img src="+middle_card+" class = 'draw ui-state-default' style='display:inline;'>";
                        }
                    // player1cards.innerHTML = data.player1cards;
                    // player2cards.innerHTML = data.player2cards;
                    // deck.innerHTML = data.deck;
                    // room_name.innerHTML=data.room
                    // const queNode = document.getElementById('que_list_container');
                    // current_que = data.current_que
                    // queNode.innerHTML = data.current_que
                    if (document.getElementsByClassName('draw')[0]!== undefined){
                        document.getElementsByClassName('draw')[0].classList.remove('highlighted_cards');
                        }
                    document.getElementsByClassName('deck')[0].classList.remove('highlighted_cards');

                    const player1cards_buttons = document.getElementsByClassName('player1cards_buttons')[0];
                    var player_1_cards = data.player1cards

                    const player2cards_buttons = document.getElementsByClassName('player2cards_buttons')[0];
                    var player1_buttons ='';
                    var player2_buttons ='';
                    player1cards_buttons.innerHTML ='';
                    player2cards_buttons.innerHTML = '';
                    player_1_cards.forEach(player1_card_buttons);


                    var player_2_cards = data.player2cards

                    player_2_cards.forEach(player2_card_buttons);

                    var card_backs = Flask.url_for("static", {"filename": "cards/back.png"})

                    function player1_card_buttons(value,index,array){
                        var player1_buttons =''
                        console.log(player1_buttons);
                        var card_image = Flask.url_for("static", {"filename": "cards/"+value+".png"})
                        var player1_buttons = player1_buttons + "<div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img src="+card_image+" class = 'player1card ui-state-default playingCard' style='display:inline;' id='" +value+"'></div>";
                        player1cards_buttons.innerHTML += player1_buttons;
                        console.log(player1_buttons);
                        }
                    function player2_card_buttons(value,index,array){
                        var player2_buttons =''
                        console.log(player2_buttons);
                        var card_image = Flask.url_for("static", {"filename": "cards/"+value+".png"})
                        var player2_buttons = player2_buttons + "<div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img src="+card_image+" class = 'player2card ui-state-default playingCard' style='display:inline;' id='" +value+"'></div>";
                        player2cards_buttons.innerHTML += player2_buttons;
                        console.log(player2_buttons);
                        }
                    if (this_player!==data.player){
                        $('.player1card').removeAttr('onclick');
                        $('.player2card').removeAttr('onclick');

                        }
                    if (this_player==data.player){
                        document.getElementById('draw_card').style.visibility = "visible";
                        // document.getElementById('draw_middle_card').style.visibility = "hidden";
                        $('#middle_cards').removeAttr('onclick')
                        $('#draw_card').removeAttr('onclick')
                        if (this_player == 'player1'){
                            $('.player1card').attr('onclick','discard(event)');
                            $('.player1card').addClass('highlighted_cards');
                            }
                        if (this_player == 'player2'){
                            $('.player2card').attr('onclick','discard(event)');
                            $('.player2card').addClass('highlighted_cards');
                            }
                        }
                    if (this_player=='player1'){
                        document.getElementsByClassName('player2cards_buttons')[0].innerHTML = "<div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div>"
                        document.getElementById('draw_card').style.visibility = "visible";
                        // document.getElementById('draw_middle_card').style.visibility = "visible";
                        // $('.player2card').attr('disabled','disabled');
                        // $('#middle_cards').attr('onclick','draw_middle_card()')
                        if(data.player1melds.meld1.length !== undefined){
                            if(data.player1melds.meld1.length == 3){
                                var meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld1[0]+".png"})
                                var meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld1[1]+".png"})
                                var meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld1[2]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML ="<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div></div>"
                                }
                            if(data.player1melds.meld1.length == 4){
                                var meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld1[0]+".png"})
                                var meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld1[1]+".png"})
                                var meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld1[2]+".png"})
                                var meld1_card4 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld1[3]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML = "<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card4+" alt=''></div></div>"
                                }
                            }
                        if(data.player1melds.meld2.length !== undefined){
                            if(data.player1melds.meld2.length == 3){
                                meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld2[0]+".png"})
                                meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld2[1]+".png"})
                                meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld2[2]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML ="<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div></div>"
                                }
                            if(data.player1melds.meld2.length == 4){
                                meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld2[0]+".png"})
                                meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld2[1]+".png"})
                                meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld2[2]+".png"})
                                meld1_card4 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld2[3]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML += "<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card4+" alt=''></div></div>"
                                }
                            }
                        if(data.player1melds.meld3.length !== undefined){
                            if(data.player1melds.meld3.length == 3){
                                meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld3[0]+".png"})
                                meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld3[1]+".png"})
                                meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld3[2]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML +="<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div></div>"
                                }
                            if(data.player1melds.meld3.length == 4){
                                meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld3[0]+".png"})
                                meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld3[1]+".png"})
                                meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld3[2]+".png"})
                                meld1_card4 = Flask.url_for("static", {"filename": "cards/"+data.player1melds.meld3[3]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML += "<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card4+" alt=''></div></div>"
                                }
                            }
                        }
                    if (this_player=='player2'){
                        document.getElementById('draw_card').style.visibility = "visible";
                        document.getElementsByClassName('player1cards_buttons')[0].innerHTML = "<div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div><div class='col col-lg-1 col-md-1 col-sm-1 col-xs-1'><img class='playingCard' src="+card_backs+" alt=''></div>"
                        // document.getElementById('draw_middle_card').style.visibility = "hidden";
                        if(data.player2melds.meld1.length !== undefined){
                            if(data.player2melds.meld1.length == 3){
                                var meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld1[0]+".png"})
                                var meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld1[1]+".png"})
                                var meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld1[2]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML ="<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div></div>"
                                }
                            if(data.player2melds.meld1.length == 4){
                                var meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld1[0]+".png"})
                                var meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld1[1]+".png"})
                                var meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld1[2]+".png"})
                                var meld1_card4 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld1[3]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML = "<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card4+" alt=''></div></div>"
                                }
                            }
                        if(data.player2melds.meld2.length !== undefined){
                            if(data.player2melds.meld2.length == 3){
                                meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld2[0]+".png"})
                                meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld2[1]+".png"})
                                meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld2[2]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML ="<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div></div>"
                                }
                            if(data.player2melds.meld2.length == 4){
                                meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld2[0]+".png"})
                                meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld2[1]+".png"})
                                meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld2[2]+".png"})
                                meld1_card4 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld2[3]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML += "<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card4+" alt=''></div></div>"
                                }
                            }
                        if(data.player2melds.meld3.length !== undefined){
                            if(data.player2melds.meld3.length == 3){
                                meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld3[0]+".png"})
                                meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld3[1]+".png"})
                                meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld3[2]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML +="<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div></div>"
                                }
                            if(data.player2melds.meld3.length == 4){
                                meld1_card1 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld3[0]+".png"})
                                meld1_card2 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld3[1]+".png"})
                                meld1_card3 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld3[2]+".png"})
                                meld1_card4 = Flask.url_for("static", {"filename": "cards/"+data.player2melds.meld3[3]+".png"})
                                document.getElementsByClassName('melds')[0].innerHTML += "<div class='col col-sm-auto' style='margin-right:10px;margin-left: 10px'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card3+" alt=''></div><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card1+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card2+" alt=''></div><div class='row'><div class='col col-sm-auto hud-card-container' style=''><img class='hud-card' src="+meld1_card4+" alt=''></div></div>"
                                }
                            }
                        }
                    console.log('card_drawn')
                    console.log(player1_buttons)
                    console.log(player2_buttons)
                    // socket.emit('/game/<id>',{'id':data.id})
                });
