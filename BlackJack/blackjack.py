from card import Card;
from deck import Deck;
import people;
import chip;
import sys;
import time;

def display_instructions() :
    print('\nInstructions: The objective of this game is to obtain a hand of cards whose value is as close to 21 ');
    print('as possible without going over. The numbered cards have the value of their number, face cards have ');
    print('a value of 10 each, and the ace can either be counted as 1 or 11 (player\'s choice)\n');
    print('Each round of the game begins with each player placing a bet. Then, the dealer passes out two cards to ');
    print('each player (up to 7 players) and to the dealer. The player\'s cards will be face up while one of the ');
    print('dealer\'s cards will be face down. Then, each player will choose to either hit, stand, split, or double down: \n');
    print('     Hit:         when a player \'hits,\' he or she is dealt another card. A player can hit as many ');
    print('                  times as wanted, up until the player busts (goes over 21). \n');
    print('     Stand:       To \'stand\' means to stay with the current cards. \n');
    print('     Split:       A player can \'split\' only when the first two cards of his or her hand are the ');
    print('                  same. When this occurs, the player makes two separate piles, one with each ');
    print('                  identical card, and places a bet identical to the initial bet for the second ');
    print('                  pile. Then, the player can hit or stand with each pile as in a normal round.\n');
    print('     Double Down: When a player chooses to \'double down\', he or she can increase the current bet ');
    print('                  by 100% in exchange for agreeing to stand after being dealt one more card.\n');
    input('Ready to play? Hit any key to continue: ');
    print();
    
def get_num_players() :
    num = input('How many people will be playing (up to 7)? Enter a number: ');
    while not num.isdigit() or int(num) < 1 or int(num) > 7:
        num = input('Please enter a number from 1 to 7: ');
    print('\nGreat! Now decide amongst yourselves the order you all will be playing in (who will be Player 1 through 7).\n');
    time.sleep(1);
    return int(num);
    
def create_players(num) :
    players_list = [];
    for i in range(num) :
        name = input(f'Player {i+1}, what is your name? ');
        while name == '':
            name = input('Please enter your name: ');
        players_list.append(people.Player(name, 1000));
    print('\nAll players will begin the game with the same amount of $1,000 dollars.\n');
    return players_list;
    
def deal(dealer, players) :
    for player in players[:-1] : 
        if not player.check_broke() : dealer.deal_card(player);
    dealer.deal_card(players[-1]); # dealer deals card to dealer, too
    
def place_bets(players) :
    print('Now, each of you must place your bets.\n');
    bets = [];
    for player in players[:-1] : # doesn't reach dealer
        if not player.check_broke() :
            bet = input(f'Bet for {player.name}: ');
            while not bet.isdigit() or int(bet) > player.money :
                msg = 'Please enter a whole number: ';
                if bet.isdigit() :
                    msg = 'You don\'t have enough money! Enter a different value: ';
                bet = input(msg);
            player.bet = int(bet);
    print(); 
    
def view_hands(players) :
    print('Here are the hands for each player: \n');
    for p in players :
        if isinstance(p, people.Dealer) :
            print(f'{p.name}: [{p.hand[0][0]}, ?]', end='');
            print();
        else :
            if not p.check_broke() :
                print(f'{p.name}: {p.hand}', end='');
                if p.check_blackjack() :
                    print(f' ==> BLACKJACK!!! -- {p.name} wins ${p.bet}!');
                else : print();
    print();
    
def do_decision(player, dealer, hand_index=0) :
    choices_dict = {'s':stand, 'h':hit, 'p':split, 'd':double_down};
    valid_choice = False;
    while not valid_choice :
        choice = input(f'{player.name}, what do you want to do (s: stand, h: hit, p: split, d: double down): ');
        while choice.lower() not in choices_dict.keys() :
            choice = input('Please enter either \'s\', \'h\', \'p\', or \'d\', corresponding to your choice: ');
        valid_choice = choices_dict.get(choice)(player, dealer, hand_index);
    
def cycle_decisions(players) :
    dealer = players[-1];
    for p in players :
        if isinstance(p, people.Dealer) :
            print(f'{p.name} will hit until reaching a hand of at least \'hard\' 17 (without an ace counting for 11).');
            sys.stdout.flush();
            time.sleep(0.8);
            if not check_status(p) and not p.check_hard_17() : hit(p, dealer);
            sys.stdout.flush();
            time.sleep(0.5);
            disp_str_slow('\nEnd-of-Round Earnings: \n', 0.05);
            if p.check_bust() :
                for i in players[:-1] :
                    if not i.check_broke() :
                        sys.stdout.flush();
                        time.sleep(0.5);
                        print('    ', end='');
                        for j in range(0,len(i.hand)) : # this is to loop through each hand for a player (player would have multiple hands after splitting)
                            if not i.check_bust(j) :
                                print(f'{i.name} wins ${i.bet}! ', end='');
                                i.money += i.bet;
                            else :
                                print(f'{i.name} loses ${i.bet}! ', end='');
                                i.money -= i.bet;
                        i.chips = chip.convert_to_chips(i.money);
                        if i.check_broke() :
                            print(f'Sorry {i.name}, but you\'re out of money and can no longer play in this game');
                        else :
                            print(f'Current Balance: ${i.money} (Chips: {i.chips})');
            else :
                for i in players[:-1] :
                    if not i.check_broke() :
                        sys.stdout.flush();
                        time.sleep(0.5);
                        print('    ', end='');
                        for j in range(0,len(i.hand)) :
                            if not i.check_bust(j) :
                                if i.hand_value(j) > p.hand_value() :
                                    print(f'{i.name} wins ${i.bet}! ', end='');
                                    i.money += i.bet;
                                elif i.hand_value(j) < p.hand_value() :
                                    print(f'{i.name} loses ${i.bet}! ', end='');
                                    i.money -= i.bet;
                                else :
                                    print(f'{i.name} tied with the {p.name}! No change. ', end='');
                            else :
                                print(f'{i.name} loses ${i.bet}! ', end='');
                                i.money -= i.bet;
                        i.chips = chip.convert_to_chips(i.money);
                        if i.check_broke() :
                            print(f'Sorry {i.name}, but you\'re out of money and can no longer play in this game');
                        else :
                            print(f'Current Balance: ${i.money} (Chips: {i.chips})');
            sys.stdout.flush();
            time.sleep(0.5);
        else :
            if not p.check_blackjack() and not p.check_broke() :
                do_decision(p, dealer);
        
def stand(player, dealer, hand_index=0) :
    print(f'{player.name} stands.\n');
    return True;
        
def hit(player, dealer, hand_index=0) :
    dealer.deal_card(player, hand_index);
    done = check_status(player, hand_index);
    if isinstance(player, people.Dealer) :
        while not player.check_hard_17() and not done:
            time.sleep(0.5);
            dealer.deal_card(player, hand_index);
            done = check_status(player, hand_index);
    else :
        
        choice = '';
        if not done :
            choice = input('Do you want to hit again (\'y\' or \'n\')? ').lower();
            while choice != 'y' and choice != 'n' :
                choice = input('Enter either \'y\' or \'n\': ');
        while choice == 'y' and not done:
            dealer.deal_card(player, hand_index);
            done = check_status(player, hand_index);
            if not done :
                choice = input('Do you want to hit again (\'y\' or \'n\')? ').lower();
                while choice != 'y' and choice != 'n' :
                    choice = input('Enter either \'y\' or \'n\': ');
        if not done : print();
    return True;
     
def split(player, dealer, hand_index=0) :
    if player.hand[hand_index][0] != player.hand[hand_index][1] :
        print('You can\'t split on that hand! You need two identical cards to split. Choose again.');
        return False;
    elif player.bet*2 > player.money :
        print(f'You don\'t have enough money to split with your current bet (${player.bet} * 2 = ${player.bet*2})! Choose again.');
        return False;
    hands = [[player.hand[hand_index][0]], [player.hand[hand_index][1]]];
    player.hand = hands;
    print('Now you will play each hand separately: \n');
    for i in range(0,2) :
        print(f'For Hand #{i+1}: ');
        do_decision(player, dealer, i);  
    return True;
    
     
def double_down(player, dealer, hand_index=0) :
    if player.bet*2 > player.money :
        print(f'You don\'t have enough money to do that (${player.bet} * 2 = ${player.bet*2})! Choose again.');
        return False;
    elif player.did_double_down :
        print('You can double down only once! Choose a different option.');
        return False;
    player.bet *= 2;
    player.did_double_down = True;
    print(f'Bet increased to ${player.bet}!.');
    do_decision(player, dealer, hand_index);
    return True;
     
def check_status(player, hand_index=0) :
    done = False;
    hand_string = '[';
    for card in player.hand[hand_index][:-1] :
        hand_string += card.__str__() + ', ';
    print(f'Current Hand: {hand_string}', end='');
    sys.stdout.flush();
    time.sleep(0.5);
    disp_str_slow(f'{player.hand[hand_index][-1].__str__()}]', 0.05);
    time.sleep(0.5);
    if player.check_blackjack(hand_index) :
        disp_str_slow(' ==> BLACKJACK!!! ', 0.05);
        if not isinstance(player, people.Dealer) : 
            disp_str_slow(f'-- {player.name} wins ${player.bet}!', 0.05);
        print('\n\n', end='');
        done = True;
        sys.stdout.flush();
        time.sleep(0.5);
    elif player.check_bust(hand_index) :
        disp_str_slow(' ==> BUST! ', 0.05);
        if not isinstance(player, people.Dealer) : 
            disp_str_slow(f'-- {player.name} loses ${player.bet}!', 0.05);
        print('\n\n', end='');
        done = True;
        sys.stdout.flush();
        time.sleep(0.5);
    else :
        print();
    return done;
    
def play_again(players) :
    print();
    all_broke = True;
    for i in players :
        if not i.check_broke() : all_broke = False;
    if not all_broke :
        choice = input('Do you all want to play another round? Enter \'y\' or \'n\': ').lower();
        while choice != 'y' and choice != 'n' :
            choice = input('Enter either \'y\' or \'n\': ');
        print();
        return choice;
    else :
        print();
        return 'n';
    
def reset(players) :
    dealer = players[-1];
    for player in players : 
        dealer.retrieve_cards(player);
        player.bet = 0;
        
def display_accounts(players) :
    for player in players[:-1] :
        change = player.money - player.initial_money;
        word = 'gain';
        if change < 0 : 
            word = 'loss';
        print(f'    {player.name}: ${player.money} (Chips: {player.chips}), net {word} of ${abs(change)}\n');
        sys.stdout.flush();
        time.sleep(0.5);
        
def disp_str_slow(phrase, t) :
    for i in phrase :
        print(i, end='');
        sys.stdout.flush();
        time.sleep(t);

def print_players(players) :
    for player in players :
        print(player);

def main() :
    display_instructions();
    num_players = get_num_players();
    players = create_players(num_players);
    dealer = people.Dealer(Deck(6));
    players.append(dealer);
    
    replay_choice = 'y';
    while replay_choice == 'y' :
        reset(players);
        place_bets(players);
        for i in range(0,2) :
            deal(dealer, players);
        view_hands(players);    
        cycle_decisions(players);
        replay_choice = play_again(players);  
        
    print('------------------------------------------------------------------------------------------------\n');
    disp_str_slow('FINAL PLAYER ACCOUNTS\n\n', 0.05);
    sys.stdout.flush();
    time.sleep(0.5)
    display_accounts(players);
    sys.stdout.flush();    
    time.sleep(0.2)
    print('------------------------------------------------------------------------------------------------\n');
    print('Goodbye!');
    
if __name__ == '__main__' :
    main();