from player import Player;
from deck import Deck;
import sys;
import time;

class Dealer(Player) :
    def __init__(self, deck) :
        Player.__init__(self, 'Dealer', 0); # money doesn't matter for dealer
        self.deck = deck;
        self.leftover_deck = Deck(0);
    
    def deal_card(self, player) :
        try :
            player.accept_card(self.deck.get_card());
        except : 
            print('No more cards left in deck.\nShuffling ', end='');
            for i in range(0,3) :
                print('.', end='');
                sys.stdout.flush();
                time.sleep(0.5);
            self.leftover_deck.shuffle();
            print(' Done! Resume dealing.');
            tmp = self.deck;
            self.deck = self.leftover_deck;
            leftover_deck = tmp; # just swap the two decks since we know self.deck must be empty now
            player.accept_card(self.deck.get_card());
            
    def adjust_money(self, adjustment) :
        raise TypeError('\'adjust_money()\' should not be called on object of type \'Dealer\'.');
        
    def retrieve_cards(self, player) :
        self.leftover_deck.append(player.return_cards());
        
    def __str__(self) :
        personInfo = Player.__str__(self);
        return f'{personInfo}\nStart Deck: {self.deck}\nEnd Deck: {self.leftover_deck}';