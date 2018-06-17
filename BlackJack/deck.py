from card import Card;
from random import shuffle;

class Deck() :
    def __init__(self, num_decks=1) : 
        self.deck_list = [];
        for i in range(0, num_decks) :
            self.deck_list += Deck.create_card_list();
        self.shuffle();
    
    def create_card_list() :
        suits = ['clubs', 'diamonds', 'hearts', 'spades'];
        card_list = [];
        for suit in suits :
            for num in range(1, 14) :
                card_list.append(Card(suit, num));
        return card_list;
        
    def append(self, new_cards) :
        if isinstance(new_cards, Deck) :
            self.deck_list = self.deck_list + new_cards.deck_list;
        elif isinstance(new_cards, list) : 
            self.deck_list += new_cards;
        else :
            self.deck_list.append(new_cards); # assuming it's a single card
    
    def __str__(self) :
        length = len(self.deck_list);
        return f'Length: {length}\nDeck: {self.deck_list}';
        
    def shuffle(self) :
        shuffle(self.deck_list);
    
    def get_card(self) :
        return self.deck_list.pop();