


def check_sets(cards):
    total_meld = []
    indv_meld = []
    possible_pair = ''
    counter = 0
    for i in cards:
        counter = 0
        indv_meld = []
        for j in cards:
            if i[0] == j[0]:
                possible_pair = j[0]
                for x in cards:
                    if x[0] == possible_pair:
                        counter = counter + 1
        if counter >= 3:
            print("Meld found at " + possible_pair)
            indv_meld = [i for i in cards if i[0] in possible_pair ]
            print(indv_meld)
            total_meld.append(indv_meld)
            print(total_meld)
            cards = [x for x in cards if x[0] != possible_pair]
            print(total_meld)


    return total_meld

def check_runs(cards):
    order_cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
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
