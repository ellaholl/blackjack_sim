import random

# basic strategy : https://www.instructables.com/Card-Counting-and-Ranging-Bet-Sizes/

# Parameters

# SET TO STRATEGY YOU WANT TO TEST:
strategyName = "basic strategy"

numberOfDecks = 1
sSoft17 = False
DAS = True
earlySurrender = False
cc = 0  # card count that will be accumlated using updateCC(strategy_name, args**)

bettingUnit = 10

# Set up deck of cards
initialDeck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4 * numberOfDecks
deck = initialDeck;


# Function to calculate the value of a hand
def hand_value(hand):
    value = 0
    num_aces = 0
    for card in hand:
        if card == 'A':
            num_aces += 1
            value += 11
        elif card in ['K', 'Q', 'J']:
            value += 10
        else:
            value += int(card)
    while num_aces > 0 and value > 21:
        value -= 10
        num_aces -= 1
    return value


# Function to deal a card
def deal(deck):
    card = deck[0]
    deck.remove(card)
    deal.counter += 1
    return card


def sum_cards(hand):
    sum = 0
    for card in hand:
        sum += hand_value(card)


def dealer_strat(hand, dealerUpCard, splitCounter=0):
    while True:
        if sum_cards(hand) < 16:
            hand.append(deal(deck))  # hit
        else:
            return "stand"

# TODO: fix logic
def get_player_index(hand):
    # print(hand[0])
    # print(hand[1])
    # print(hand_value(hand))
    if hand[0] == hand[1]:  # match cases
        for c in range(2, 11):
            if hand_value([hand[0]]) == c:
                return 24 + (c - 2)
    if hand[0] == 'A' or hand[1] == 'A': # ace cases
        for c in range(2, 11):
            if hand_value([hand[0]]) == c and hand_value([hand[1]]) == 'A':
                return 15 + (c-2)
            if hand_value([hand[0]]) == 'A' and hand_value([hand[1]]) == c:
                return 15 + (c-2)
    if 5 >= hand_value(hand) <= 7: # remaining cases
        return 0
    for c in range(8, 21):
        if hand_value(hand) == c:
            return 1 + (c-8)
    print("error!")


def get_dealer_index(hand):
    if hand[0] == 'A':
        return 9
    else:
        return hand_value(hand[0]) - 2


# https://www.888casino.com/blog/blackjack-strategy-guide/blackjack-charts
def play_basic_strategy(hand, dealerUpCard, splitCounter=0):
    # implement basic strategy grid here
    # return options: hit, stand, dobule, split, surrender, double
    array2D = []

    filename = 'basic_strategy.txt'

    with open(filename, 'r') as f:
        for line in f.readlines():
            array2D.append(line.split(','))

    while True:

        move = array2D[get_player_index(hand)][get_dealer_index(dealerUpCard)]
        if move == 'H':
            hand.append(deal(deck))  # hit
            print("H")
            print("Your hand:" + str(hand))
            print("Value: " + str(hand_value(hand)))
            if hand_value(hand) > 21:
                return 'B'
        else:
            # try:
            print(move)
            return move
            # except:
            #     print("error reading strategy card")
            #     exit(1)


# TEMPLATE FOR ARGS THAT STRATEGY SHOULD UTILIZE
def play_hand(deck, hand, bankroll, bet, splitCounter=0):
    while True:
        action = input('Do you want to hit, stand, double, split, or surrender? ')
        if action == 'hit':
            hand.append(deal(deck))
            print('Your hand:', hand)
            print('Value:', hand_value(hand))
            if hand_value(hand) > 21:
                print('Bust!')
                return -1, bankroll, bet, hand
        elif action == 'stand':
            return 1, bankroll, bet, hand
        elif action == 'double':
            if len(hand) == 2 and DAS == True:
                bankroll -= bet;
                bet *= 2
                hand.append(deal(deck))

                print('Your hand:', hand)
                print('Value:', hand_value(hand))

                if hand_value(hand) > 21:
                    print('Bust!')
                    return -1, bankroll, bet, hand
                else:
                    return 2, bankroll, bet, hand
            elif (splitCounter > 0 and DAS == False):
                print('You cannot double after splitting')
            else:
                print('You can only double down on your first two cards.')
        elif action == 'split':
            if len(hand) == 2 and hand_value(hand[0]) == hand_value(hand[1]) and splitCounter <= 2:
                # Create two new hands
                splitHand1 = [hand.pop(), deal(deck)]
                splitHand2 = [hand.pop(), deal(deck)]

                hand = [splitHand1, splitHand2]
                bankroll -= bet

                return 0, bankroll, bet, hand
            else:
                print('You can only split on your first two cards if they have the same value.')
                print('You can only split a total of 3 times on a given initial hand.')

        elif action == 'surrender':

            return -0.5, bankroll, bet, hand
        else:
            print('Invalid action.')


# Function to offer insurance
def offer_insurance(strategyName, dealer_hand):
    if strategyName == "first take":
        return False  # basic strategy never takes insurance
    else:
        return False  # default case


# Function to offer early surrender
def offer_earlySurrender(strategyName, earlySurrender):
    if strategyName == "first take":
        return False  # basic strategy never surrenders
    elif strategyName == "dealers strat":
        return False
    else:
        return False  # default case


# def get_bet(bankroll):
#     while True:
#         bet = input('You have $' + str(bankroll) + ' How much do you want to bet?')
#         try:
#             bet = int(bet)
#             if bet <= 0:
#                 print('Invalid bet. Please enter a positive integer.')
#             elif bet > bankroll:
#                 print(f'You cannot bet more than ${bankroll}.')
#             else:
#                 bankroll = bankroll - bet;
#                 return bet, bankroll
#         except ValueError:
#             print('Invalid bet. Please enter a positive integer.')


def dealer_turn(dealer_hand):
    # Dealer's turn
    print('Dealer hand:', dealer_hand)
    while hand_value(dealer_hand) < 17 or (sSoft17 == False and hand_value(dealer_hand) == 17 and 'A' in dealer_hand):
        if (sSoft17 == False and hand_value(dealer_hand) == 17 and 'A' in dealer_hand):
            print("Hit on soft 17")
        dealer_hand.append(deal(deck))
        print('Dealer hand:', dealer_hand)

    print("Dealer Value:", hand_value(dealer_hand))
    print("\n")
    return dealer_hand


def determine_winner(player_value, dealer_value, action, bet, bankroll):
    if action == -0.5:
        print("You have surrendered this hand -" + + str(bet / 2))
        bankroll += bet / 2
    else:
        if dealer_value > 21:
            print('Dealer busts! You win! +' + str(bet))
            bankroll += 2 * bet
        elif dealer_value > player_value:
            print('Dealer wins! -' + str(bet))
        elif player_value > dealer_value:
            print('You win! +' + str(bet))
            bankroll += 2 * bet
        else:
            print("Push +0")
            bankroll += bet
    print("\n")
    return bankroll


def fix_split_list(lst):
    return [[item for inner in sublst for item in inner] for sublst in lst]


# Start the game
bankroll = 1000
print('Welcome to Blackjack!')

# Print Params
print("Number of Decks:" + str(numberOfDecks))

print("You have $" + str(bankroll) + " to begin with")
random.shuffle(deck)
deal.counter = 0
shoe = random.randrange(0, len(deck) - round(len(deck) * .4))  # Card that when drawn makes dealer shuffle the deck


# values to return before cards are dealt: int bet
# values to accumulate: card count
# values to return after cards are dealt: boolean insurance, string move

def get_cc_bet(strategyName, bankroll, cc):
    if strategyName == 'basic strategy':  # standard card counting bet
        return (cc - 1) * (1 / 1000) * bankroll  # betting unit = 1/1000 of bankroll
    if strategyName == 'Omega II':
        if (cc == 0):
            return (1 / 1000) * bankroll
        else:
            return cc * (1 / 1000) * bankroll
    else:
        return bettingUnit  # default case

    # TODO: add condition to make sure there's enough money for bet to be made?


def update_cc(strategyName, cards, cc):
    if strategyName == 'basic strategy':
        for card in cards:
            if 2 <= hand_value([card]) <= 6:
                cc += 1
            elif not (7 <= hand_value([card]) <= 9):
                cc -= 1
        return cc  # TODO: need to divide by the number of decks remaining
    elif strategyName == 'Omega II':
        for card in cards:
            if hand_value([card]) == 10:
                cc -= 2
            elif hand_value([card]) == 9:
                cc -= 1
            elif hand_value([card]) == 2 or hand_value([card]) == 3 or hand_value([card]) == 7:
                cc += 1
            elif 4 <= hand_value([card]) <= 6:
                cc += 2
        return cc


# TODO: return bet based upon card count
# QUESTIONS: does game stop once there no more money?
bet = get_cc_bet(strategyName, bankroll, cc)  # TODO: can replace with different optimal betting strategies
bankroll = bankroll - bet

while True:

    player_hand = [deal(deck), deal(deck)]
    player_initial_hand = player_hand[:]  # For checking split aces

    dealer_hand = [deal(deck), deal(deck)]
    print('Your hand:', player_hand)
    print('Value:', hand_value(player_hand))
    print('Dealer hand:', [dealer_hand[0], 'X'])

    # remember to reset when deck is shuffled
    cc = update_cc(strategyName, player_initial_hand, cc)
    cc = update_cc(strategyName, dealer_hand, cc)

    # Offer insurance if the dealer has an Ace
    if offer_insurance(strategyName, dealer_hand):  # TODO: update function to decide on insurance depending on strategy
        print('You have taken insurance.')
        bankroll = bankroll - bet / 2;

        # Check if the dealer has blackjack
        if hand_value(dealer_hand) == 21:
            print('Dealer has blackjack! Insurance hits')
            bankroll += bet;
        else:
            print('Dealer does not have blackjack. You lose your insurance bet. Play continues.')

    # Check for blackjack
    if hand_value(player_hand) == 21 or hand_value(dealer_hand) == 21:
        if hand_value(player_hand) == 21 and hand_value(dealer_hand) == 21:
            print('The player and the dealer have blackjack')
            print('Push\n')
            bankroll += bet
        elif hand_value(player_hand) == 21 and hand_value(dealer_hand) != 21:
            print('You have Blackjack!')
            print('You win! Blackjack pays out 3/2 +' + str(1.5 * bet) + '\n')
            bankroll += bet + bet * (1.5)
        elif hand_value(player_hand) != 21 and hand_value(dealer_hand) == 21:
            print('Dealer has Blackjack')
            print('Dealer wins\n')
    elif offer_earlySurrender(strategyName,
                              earlySurrender):  # TODO: update function to decide on insurance depending on strategy
        print("You have surrendered this hand -" + str(bet / 2))
        bankroll += bet / 2;

    else:
        # Player's turn

        if strategyName == "basic strategy":
            action = play_basic_strategy(player_initial_hand, player_hand, False)
        elif strategyName == "dealers strat":
            action = play_basic_strategy(player_initial_hand, player_hand, False)
        else:
            print("invalid strategy")
            exit(1)
        # list all strategies here...

        # If player busts, end the game
        if action == "B":
            print('You lose! -' + str(bet))
        else:

            if action == 'P':  # Split
                splitPlayer_hand = [player_hand[0], player_hand[1]]
                holder_hand = ['x', 'x']
                bet_holder = [bet, bet]
                action_holder = [1, 1]
                i = 0
                splitCount = 1;

                if (player_initial_hand == ['A', 'A']):  # Split aces
                    print("\n")
                    print("Player cannot do anything else after splitting aces")
                    print("Your hands: ", splitPlayer_hand)
                    print('Hand ' + str(1) + ':', splitPlayer_hand[0])
                    print('Value:', hand_value(splitPlayer_hand[0]))
                    print('Hand ' + str(2) + ':', splitPlayer_hand[1])
                    print('Value:', hand_value(splitPlayer_hand[1]))
                    print('Dealer hand:', [dealer_hand[0], 'X'])
                else:  # Split anything else

                    while i < len(splitPlayer_hand):

                        print("\n")
                        print("Your hands: ", splitPlayer_hand)
                        print('Hand ' + str(i + 1) + ':', splitPlayer_hand[i])
                        print('Value:', hand_value(splitPlayer_hand[i]))
                        print('Dealer hand:', [dealer_hand[0], 'X'])
                        bet_holder.append(bet)
                        action_holder.append(1)

                        action_holder[i], bankroll, bet_holder[i], holder_hand = play_hand(deck, splitPlayer_hand[i],
                                                                                           bankroll, bet_holder[i],
                                                                                           splitCount)

                        splitPlayer_hand[i] = holder_hand;
                        if type(splitPlayer_hand[i][0]) == type([]):
                            splitPlayer_hand.append(splitPlayer_hand[i][1])
                            splitPlayer_hand[i] = splitPlayer_hand[i][0]

                        if (action_holder[i] == 0):
                            splitCount += 1
                            i = 0
                        else:
                            i = i + 1

                for i in range(0, len(splitPlayer_hand)):
                    if action_holder[i] == -1:
                        print("Hand " + str(i + 1) + " loses -" + str(bet_holder[i]))

                dealer_hand = dealer_turn(dealer_hand);
                dealer_value = hand_value(dealer_hand)

                for i in range(0, len(splitPlayer_hand)):
                    if action_holder[i] != -1:
                        print("Hand " + str(i + 1) + ":")
                        player_value = hand_value(splitPlayer_hand[i])
                        bankroll = determine_winner(player_value, dealer_value, action_holder[i], bet_holder[i],
                                                    bankroll)



            else:
                dealer_hand = dealer_turn(dealer_hand);
                player_value = hand_value(player_hand)
                dealer_value = hand_value(dealer_hand)
                print("determining winner")
                bankroll = determine_winner(player_value, dealer_value, action, bet, bankroll)

                print("\n \n")

    if deal.counter >= shoe:
        deck = initialDeck
        random.shuffle(deck)
        shoe = random.randrange(0,
                                len(deck) - round(len(deck) * .4))  # Card that when drawn makes dealer shuffle the deck
        deal.counter = 0
        print("Shuffling the deck...")
