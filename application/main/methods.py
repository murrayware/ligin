











def check_sets(cards):
    total_meld = []
    indv_meld = []
    cards_check = [i[0] for i in cards]
    number_list = []
    for i in cards_check:
        if cards_check.count(i) > 2:
            if i in number_list:
                pass
            if i not in number_list:
                number_list.append(i)
    if len(number_list) > 0:
        for j in number_list:
            total_meld.append([i for i in cards if i[0] in j])
    for meld in total_meld:
        if len(meld) == 4:
            total_meld.append(meld[0:3])
            total_meld.append(meld[1:4])
            total_meld.append(meld[1:2] + meld[2:4])
    return total_meld









def check_runs(cards):
    order_cards = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
    index_card = ''
    index_list = []
    count = 0
    indv_meld = []
    total_meld = []
    hearts = [i for i in cards if i[1] in 'H']
    clubs = [i for i in cards if i[1] in 'C']
    spades = [i for i in cards if i[1] in 'S']
    diamonds = [i for i in cards if i[1] in 'D']




    if len(hearts) >= 3:
        for i in hearts:
            index_list = []
            indv_meld = []
            index_card = ''
            count = 0
            index_card = order_cards[order_cards.index(i[0])]
            if (index_card == 'Q') or (index_card =='K'):
                continue
            index_list = order_cards[order_cards.index(i[0]):order_cards.index(i[0])+3]
            for item in hearts:
                if item[0] in index_list:
                    count = count + 1
                if count == 3:
                    indv_meld = [i for i in cards if i[0] in index_list ]
                    indv_meld = [i for i in indv_meld if i[1] in 'H' ]
                    if index_card != 'J':
                        count = 0
                        index_list = order_cards[order_cards.index(i[0]):order_cards.index(i[0])+4]
                        for item2 in hearts:
                            if item2[0] in index_list:
                                count = count + 1
                        if count == 4:
                            indv_meld = [i for i in cards if i[0] in index_list ]
                            indv_meld = [i for i in indv_meld if i[1] in 'H' ]
                    total_meld.append(indv_meld)



    if len(spades) >= 3:
        for i in spades:
            index_list = []
            indv_meld = []
            index_card = ''
            count = 0
            index_card = order_cards[order_cards.index(i[0])]
            if (index_card == 'Q') or (index_card =='K'):
                continue
            index_list = order_cards[order_cards.index(i[0]):order_cards.index(i[0])+3]
            for item in spades:
                if item[0] in index_list:
                    count = count + 1
                if count == 3:
                    indv_meld = [i for i in cards if i[0] in index_list ]
                    indv_meld = [i for i in indv_meld if i[1] in 'S' ]
                    if index_card != 'J':
                        count = 0
                        index_list = order_cards[order_cards.index(i[0]):order_cards.index(i[0])+4]
                        for item2 in hearts:
                            if item2[0] in index_list:
                                count = count + 1
                        if count == 4:
                            indv_meld = [i for i in cards if i[0] in index_list ]
                            indv_meld = [i for i in indv_meld if i[1] in 'S' ]
                    total_meld.append(indv_meld)


    if len(clubs) >= 3:
        for i in clubs:
            index_list = []
            indv_meld = []
            index_card = ''
            count = 0
            index_card = order_cards[order_cards.index(i[0])]
            if (index_card == 'Q') or (index_card =='K'):
                continue
            index_list = order_cards[order_cards.index(i[0]):order_cards.index(i[0])+3]
            for item in clubs:
                if item[0] in index_list:
                    count = count + 1
                if count == 3:
                    indv_meld = [i for i in cards if i[0] in index_list ]
                    indv_meld = [i for i in indv_meld if i[1] in 'C' ]
                    if index_card != 'J':
                        count = 0
                        index_list = order_cards[order_cards.index(i[0]):order_cards.index(i[0])+4]
                        for item2 in hearts:
                            if item2[0] in index_list:
                                count = count + 1
                        if count == 4:
                            indv_meld = [i for i in cards if i[0] in index_list ]
                            indv_meld = [i for i in indv_meld if i[1] in 'C' ]
                    total_meld.append(indv_meld)


    if len(diamonds) >= 3:
        for i in diamonds:
            index_list = []
            indv_meld = []
            index_card = ''
            count = 0
            index_card = order_cards[order_cards.index(i[0])]
            if (index_card == 'Q') or (index_card =='K'):
                continue
            index_list = order_cards[order_cards.index(i[0]):order_cards.index(i[0])+3]
            for item in diamonds:
                if item[0] in index_list:
                    count = count + 1
                if count == 3:
                    indv_meld = [i for i in cards if i[0] in index_list ]
                    indv_meld = [i for i in indv_meld if i[1] in 'D' ]
                    if index_card != 'J':
                        count = 0
                        index_list = order_cards[order_cards.index(i[0]):order_cards.index(i[0])+4]
                        for item2 in hearts:
                            if item2[0] in index_list:
                                count = count + 1
                        if count == 4:
                            indv_meld = [i for i in cards if i[0] in index_list ]
                            indv_meld = [i for i in indv_meld if i[1] in 'D' ]
                    total_meld.append(indv_meld)

    return total_meld



def possible_melds(cards):
    sets = check_sets(cards)
    runs = check_runs(cards)
    return (sets+runs)



def count_cards(cards):
    count = 0
    for i in cards:
        if i[0] == 'K' or i[0] == 'J' or i[0]== 'Q' or i[0]== 'T':
            count = count + 10
        if i[0] == "9":
            count = count + 9
        if i[0] == "8":
            count = count + 8
        if i[0] == "7":
            count = count + 7
        if i[0] == "6":
            count = count + 6
        if i[0] == "5":
            count = count + 5
        if i[0] == "4":
            count = count + 4
        if i[0] == "3":
            count = count + 3
        if i[0] == "2":
            count = count + 2
        if i[0] == "A":
            count = count + 1
    return count




#function to quickly remove item in the melds
def remove_meld(cards,meld):
    deadwood = []
    for i in cards:
        deadwood.append(i)
    try:
        #trying to remove all cards, if not possible meld is not possible
        for card in meld:
            deadwood.remove(card)
        return [deadwood,True]
    except:
        #no cards removed from deck, meld not possible
        return[deadwood,False]




def possible_hands(cards):
    melds = possible_melds(cards)
    possible_hands = []
    meld1 = []
    meld2 = []
    meld3 = []
    deadwood = []
    #covering the case if no melds are in deck
    if len(melds) == 0:
        deadwood = cards
        possible_hands.append({
            'meld1':meld1,
            'meld2':meld2,
            'meld3':meld3,
            'deadwood':deadwood,
            'score': count_cards(deadwood)
            })
        return possible_hands
    if len(melds) > 0:
        for meld in melds:
            meld1 = []
            meld2 = []
            meld3 = []
            meld1 = meld
            possible_hands.append({
                'meld1':meld1,
                'meld2':meld2,
                'meld3':meld3,
                'deadwood':remove_meld(cards,meld1)[0],
                'score': count_cards(remove_meld(cards,meld1)[0])
                }
    )

            print(cards)
            #case if only one meld exists -works properly
            if len(melds) == 1:
                possible_hands.append({
                                        'meld1':meld1,
                                        'meld2':meld2,
                                        'meld3':meld3,
                                        'deadwood':remove_meld(cards,meld1)[0],
                                        'score':count_cards(deadwood)
                                        }
                    )
                break

            #case if there are more melds than one
            if len(melds) > 1:
                second_melds = possible_melds(remove_meld(cards,meld1)[0])
                ##################second iteration
                for second_meld in second_melds:
                    meld2 = second_meld
                    second_deadwood = (remove_meld(cards,meld2+meld1))
                    #checking if possible to remove deadwood with this hand
                    if second_deadwood[1] == False:
                        pass
                    #if you can remove, go for a third itteration and add the third meld
                    if second_deadwood[1] == True:
                        #now we have a different hand, keep going through to see if we can add a third meld or not with these two melds
                        possible_hands.append({
                                        'meld1':meld1,
                                        'meld2':meld2,
                                        'meld3':meld3,
                                        'deadwood':remove_meld(cards,meld2+meld1)[0],
                                        'score': count_cards(remove_meld(cards,meld2+meld1)[0])
                                        }
                            )


                        #checking if we have possibility of meld in the remaining 3-4 cards
                        third_melds = possible_melds(remove_meld(cards,meld1+meld2)[0])
                        #same as second meld, check if the case can be added given the other melds
                        ################third iteration if possible
                        for third_meld in third_melds:
                            meld3 = third_meld
                            third_deadwood = remove_meld(cards,meld3+meld2+meld1)
                            if third_deadwood[1] == False:
                                #no melds, the past case is correct
                                pass
                            if third_deadwood[1] == True:
                                possible_hands.append({
                                        'meld1':meld1,
                                        'meld2':meld2,
                                        'meld3':meld3,
                                        'deadwood':remove_meld(cards,meld3+meld2+meld1)[0],
                                        'score': count_cards(remove_meld(cards,meld3+meld2+meld1)[0])
                                       }
                                    )

    return possible_hands



def best_hand(hand_dict):
    current_best = 200
    best_hand = {}
    for hand in hand_dict:
        for k,v in hand.items():
            if k == 'score':
                if v < current_best:
                    current_best = v
                    best_hand = hand
    return best_hand






###testing with various hands
#2 melds that interact with eachother
hand = ["2H", "2C", "2S", "5H", "5D", "5S", "TC", "3H", "3C", "AH"]
(possible_hands(hand))
#one meld, adds two of the same melds, can be fixed later, still functions properly
cards = ["AH", "2C", "3S", "4D", "5H", "6C", "7S", "8D", "9H", "TC"]
print('possible hands',possible_hands(cards))
#returns
#[{'meld1': ['2H', '2C', '2S'], 'meld2': [], 'meld3': [], 'deadwood': ['KH', '5D', '5S', 'TC', '3H', '3C', 'QH'], 'score': 46},
#{'meld1': ['2H', '2C', '2S'], 'meld2': [], 'meld3': [], 'deadwood': ['KH', '5D', '5S', 'TC', '3H', '3C', 'QH'], 'score': 0}]

#testing gin
cards = ["AH", "2C", "3S", "4D", "5H", "6C", "7S", "8D", "9H", "TC"]
x = possible_hands(cards)
print('best_hand',best_hand(x))
#returns
#{'meld1': ['2H', '2C', '2S'], 'meld2': ['KH', 'KD', 'KS'], 'meld3': ['TC', 'TH', 'TD', 'TS'], 'deadwood': [], 'score': 0}
