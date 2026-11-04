import random
import sys

full_deck = [
    "A", "A", "A", "A",
    "2", "2", "2", "2",
    "3", "3", "3", "3",
    "4", "4", "4", "4",
    "5", "5", "5", "5",
    "6", "6", "6", "6",
    "7", "7", "7", "7",
    "8", "8", "8", "8",
    "9", "9", "9", "9",
    "10", "10", "10", "10",
    "J", "J", "J", "J",
    "Q", "Q", "Q", "Q",
    "K", "K", "K", "K"
]

cards = full_deck.copy()


money = 1000

def main():
    global player_value, dealer_value, money, bet, dealer_hand, player_hand
    player_hand = []
    dealer_hand = []
    bet = new_round()
    player_hand.append(pick_cards())
    dealer_hand.append(pick_cards())
    player_hand.append(pick_cards())
    dealer_hand.append(pick_cards())
    player_value = pvalue(player_hand)
    dealer_value = pvalue(dealer_hand)

    if player_value == 21:
        if dealer_value == 21:
            print(f"\nYour hand: {player_hand} - {player_value}")
            print(f"Dealer hand: {dealer_hand} - {dealer_value}")
            print("Almost. It's a Tie.")
            return
        else:
            print(f"\nYour hand: {player_hand} - {player_value}")
            print(f"Dealer hand: {dealer_hand} - {dealer_value}")
            print(f"BLACKJACK!!! You win {bet * 1.5}")
            money = bet * 1.5 + money
            return
        
    print(f"\nYour hand: {player_hand} - {player_value}")
    print(f"Dealer hand: [hole, {dealer_hand[1]}]")
    if player_hand[0] == player_hand[1]:
        print("Do you want to hit, stand, or split")
    if player_value < 21:
        hit_stand()


def pick_cards():
    card = random.choice(cards)
    cards.remove(card)
    return card

def new_round():
    global cards
    cards = full_deck.copy()
    while True:
        print("---------------------------------")
        try:
            bet = int(input(f"You have ${money}, Place bet: $"))
            if bet <= 0:
                print("Has to be positive whole number")
            elif bet > money:
                print("Can't bet that much")
            elif bet == 1:
                confirm = int(input("Can't bet $1. Type another whole number or '1' again to end "))
                if confirm == 1:
                    end()
                elif 0 < confirm <= money:
                    return confirm
                else:
                    print("Can't bet that")
            else:
                return bet
        except ValueError:
            print("Invalid. Type '1' if your done or type a whole number")

def pvalue(hand):
    value = 0
    aces = hand.count("A")
    for card in hand:
        if card == "A":
            value += 11
        elif card in ["J", "Q", "K"]:
            value += 10
        else:
            value += int(card)
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value


def hit_stand():
    global money, player_value
    while True:
        answer = input("\nHit or Stand? ").casefold().strip()
        if answer == "hit":
            player_hand.append(pick_cards())
            player_value = pvalue(player_hand)
            if player_value < 21:
                print(f"Your hand: {player_hand} - {player_value}")
                print(f"Dealer hand: [hole, {dealer_hand[1]}]")
            elif player_value == 21:
                stand()
                break
            else:
                print(f"\nYour hand: {player_hand} - {player_value}")
                print(f"Dealer hand: {dealer_hand} - {dealer_value}")
                print("You lost.")
                money -= bet
                break
        elif answer == "stand":
            stand()
            break
        else:
            print("Invalid Input")


def stand():
    global money, dealer_value
    while True:
        if dealer_value > 21:
            print(f"Your hand: {player_hand} - {player_value}")
            print(f"Dealer hand: {dealer_hand} - {dealer_value}")
            print("Dealer busted. You won, congrats!")
            money += bet
            break
        elif dealer_value >= 17:
            if player_value > dealer_value:
                print(f"\nPlayer hand: {player_hand} - {player_value}")
                print(f"Dealer hand: {dealer_hand} - {dealer_value}")
                print("You Won, Congrats!")
                money += bet
                break
            elif player_value == dealer_value:
                if len(dealer_hand) == 2 and dealer_value == 21:
                    print(f"\nPlayer hand: {player_hand} - {player_value}")
                    print(f"Dealer hand: {dealer_hand} - {dealer_value}")
                    print("You lost, dealer got a natural blackjack")
                    money -= bet
                    break
                else:
                    print(f"\nPlayer hand: {player_hand} - {player_value}")
                    print(f"Dealer hand: {dealer_hand} - {dealer_value}")
                    print("Push")
                    break
            else:
                if dealer_value <= 21:
                    print(f"\nPlayer hand: {player_hand} - {player_value}")
                    print(f"Dealer hand: {dealer_hand} - {dealer_value}")
                    print("You lost")
                    money -= bet
                    break
        else:
            dealer_hand.append(pick_cards())
            dealer_value = pvalue(dealer_hand)

def end():
    print("---------------------------------------")
    if money >= 1000:
        print(f"Congrats! Your leaving with ${money}")
        sys.exit()
    elif money == 0:
        print("You lost all your money. Type 'python3 blackjack.py' to start a new game.\n")
        sys.exit()
    elif money < 1000:
        print(f"You leaving with ${money}.")
        sys.exit()

print("\n\nWelcome to Blackjack! You start with $1000 and see how high you can go!\nPlay smart and try not to go broke!\n")

while True:
    try:
        if money == 0:
            raise IndexError
        main()
    except IndexError:
        end()
