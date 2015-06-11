# 24.04.2014

# http://www.codeskulptor.org/#user39_c8YD1uUc8M_10.py

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False

outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.list_of_card = []
        
    def __str__(self):
        ans = ""
        for i in range(len(self.list_of_card)):
            ans += self.list_of_card[i] + " "
        return ans  # return a string representation of a hand

    def add_card(self, card): 
        self.list_of_card.append(str(card))                              
        return card   # add a card object to a hand

    def get_value(self):        
        value = 0         
        for cards in range(len(self.list_of_card)):
            value += VALUES[self.list_of_card[cards][1]]
            for c in self.list_of_card:               
                if c[1] != 'A':
                    value 
                else: 
                    if value + 10 <= 21:
                        value += 10
                    else:
                        value            
        return value
   
    def draw(self, canvas, pos):
        for cards in self.list_of_card: 
            Card(cards[0], cards[1]).draw(canvas, pos)
            pos[0] += 71
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck_list = []
        for s in SUITS:
            card_suits = s
            for r in RANKS:
                self.deck_list.append(card_suits + r)
            # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck_list)

    def deal_card(self):
        select_card = self.deck_list[(len(self.deck_list)-1)]
        self.deck_list.remove(select_card)
        return select_card
    
    def __str__(self):
        deck_list_content = ""
        for i in range(len(self.deck_list)):
            deck_list_content += self.deck_list[i] + " "
        return deck_list_content
        
#define event handlers for buttons
def deal():
    global outcome, in_play, player_card, dealer_card, button_action  
    global actual_player_value, actual_dealer_value, game_play, who_win 
    
    button_action = 'DEAL'
    who_win = ""

    if not in_play: 
        actual_player_value = 0
        actual_dealer_value = 0
        
        outcome = Deck()
        outcome.shuffle()
    
        player_card = Hand()
        dealer_card = Hand()
        for i in range(2):
            player_card.add_card(outcome.deal_card())

        for i in range(2):
            dealer_card.add_card(outcome.deal_card())
        in_play = True    
    else:
        outcome = Deck()
        outcome.shuffle()
        who_win = 'Dealer win, Player chosen new game!'
        in_play = False
        
    game_play = True
    
    
    
def hit():
    global actual_player_value, in_play, button_action, who_win
    
    button_action = 'HIT'
    
    player_card.add_card(outcome.deal_card())
    actual_player_value = player_card.get_value()
    if in_play:
        if actual_player_value <= 21: 
            actual_player_value = player_card.get_value()
        else:
            who_win = 'You have busted'
            in_play = False     
            
def stand():
    global button_action, actual_player_value, actual_dealer_value, in_play
    global game_play, who_win
    
    button_action = 'STAND'
    actual_player_value = player_card.get_value()
        
    if in_play:
        actual_dealer_value = dealer_card.get_value()
        while actual_dealer_value < 17:
            dealer_card.add_card(outcome.deal_card())            
            actual_dealer_value = dealer_card.get_value()
        if actual_dealer_value <= 21 and actual_dealer_value >= actual_player_value: 
            who_win = 'Dealer win!'    
        else: 
            who_win =  'Player win!'
    else:
        who_win =  'You have busted'
    game_play = False

# draw handler    
def draw(canvas):

    player_card.draw(canvas, [50, 150])
    dealer_card.draw(canvas, [50, 350])
    canvas.draw_text(button_action, (50, 95), 25, 'White', 'sans-serif')
    canvas.draw_text('BLACK JACK', (50, 50), 35, 'White', 'sans-serif')
    if game_play:
        canvas.draw_image(card_back, (72/2, 96/2), (72, 96), (86, 398), (72, 96))
    canvas.draw_text(who_win, (150, 305), 25, 'White', 'sans-serif')
    result = str(actual_player_value) + ':' + str(actual_dealer_value)
canvas.draw_text(result, (50, 305), 25, 'White', 'sans-serif')
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()

frame.start()



