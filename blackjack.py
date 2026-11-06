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
test_deck = ["A", "7", "A", "8", "5", "3", "8", "4"]
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
    if player_hand[0] == player_hand[1] and money >= 2 * bet:
        action = input("Hit, split or stand? ").casefold().strip()
        if action == "split":
            split()
        elif action == "hit" or action == "stand":
            hit_stand(action)
        else:
            print("Invalid Input")
    else:
        while player_value < 21 and dealer_value <= 21:
            action = input("Hit or stand? ").casefold().strip()
            if action == "hit" or action == "stand":
                hit_stand(action)
            else:
                print("Invalid Input")


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


def hit_stand(answer):
    global money, player_value, next
    if answer == "hit":
        player_hand.append(pick_cards())
        player_value = pvalue(player_hand)
        if player_value < 21:
            print(f"\nYour hand: {player_hand} - {player_value}")
            print(f"Dealer hand: [hole, {dealer_hand[1]}]")
        elif player_value == 21:
            stand()
        else:
            print(f"\nYour hand: {player_hand} - {player_value}")
            print(f"Dealer hand: {dealer_hand} - {dealer_value}")
            print("You lost.")
            money -= bet
    if answer == "stand":
        stand()


def stand():
    global money, dealer_value, player_value
    if dealer_value > 21:
        print(f"\nYour hand: {player_hand} - {player_value}")
        print(f"Dealer hand: {dealer_hand} - {dealer_value}")
        print("Dealer busted. You won, congrats!")
        money += bet
    elif dealer_value >= 17:
        if player_value > dealer_value:
            print(f"\nPlayer hand: {player_hand} - {player_value}")
            print(f"Dealer hand: {dealer_hand} - {dealer_value}")
            print("You Won, Congrats!")
            money += bet
        elif player_value == dealer_value:
            if len(dealer_hand) == 2 and dealer_value == 21:
                print(f"\nPlayer hand: {player_hand} - {player_value}")
                print(f"Dealer hand: {dealer_hand} - {dealer_value}")
                print("You lost, dealer got a natural blackjack")
                money -= bet
            else:
                print(f"\nPlayer hand: {player_hand} - {player_value}")
                print(f"Dealer hand: {dealer_hand} - {dealer_value}")
                print("Push")
                dealer_value = 100     #sets dealer value above 21 so the same main() doesn't run and new round starts
        else:
            print(f"\nPlayer hand: {player_hand} - {player_value}")
            print(f"Dealer hand: {dealer_hand} - {dealer_value}")
            print("You lost")
            money -= bet
        dealer_value = 100          #sets dealer value above 21 so the same main() doesn't run again
    while dealer_value < 17:
        dealer_hand.append(pick_cards())
        dealer_value = pvalue(dealer_hand)
        stand()

def split():
    global player_hand, split_hand, player_value, dealer_value, money, bet, dealer_hand
    lost = 0
    tie = 0
    temp_card = player_hand[0]
    player_hand.remove(temp_card)
    split_hand = [temp_card]
    player_hand.append(pick_cards())
    split_hand.append(pick_cards())
    print("1st hand")
    player_value = pvalue(player_hand)
    print(f"Your hand: {player_hand} - {player_value}")
    print(f"Dealer hand: [hole, {dealer_hand[1]}]")
    while player_value < 21:
        action = input("Hit or stand? ").casefold().strip()
        if action == "hit":
            player_hand.append(pick_cards())
            player_value = pvalue(player_hand)
            print(f"Your 1st hand: {player_hand} - {player_value}")
        elif action == "stand":
            break
        else:
            print("Invalid Input")
    if player_value > 21:
        lost += 1
    print("2nd hand")
    split_value = pvalue(split_hand)
    dealer_value = pvalue(dealer_hand)
    print(f"Your hand: {player_hand} - {player_value}")
    print(f"Dealer hand: [hole, {dealer_hand[1]}]")
    while split_value < 21:
        action = input("Hit or stand? ").casefold().strip()
        if action == "hit":
            split_hand.append(pick_cards())
            split_value = pvalue(split_hand)
            print(f"Your 2nd hand: {split_hand} - {split_value}")
        elif action == "stand":
            break
        else:
            print("Invalid Input")
    if split_value > 21:
            lost += 1
    while dealer_value < 17:
        dealer_hand.append(pick_cards())
        dealer_value = pvalue(dealer_hand)
    if dealer_value > player_value and player_value < 21 and dealer_value < 21:
        lost += 1
    if dealer_value > split_value and split_value < 21 and dealer_value < 21:
        lost += 1
    if dealer_value == split_value and player_value <= 21:
        tie = 1
    if dealer_value == player_value and player_value <= 21:
        tie += 1
    print(f"\nYour 1st hand: {player_hand} - {player_value}")
    print(f"Your 2nd hand: {split_hand} - {split_value}")
    print(f"Dealer hand: {dealer_hand} - {dealer_value}")
    print(f"You won {2 - lost} hands and tied {tie} hands")
    if lost == 2:
        money -= 2 * bet
    if lost == 1 and tie == 1:
        money -= bet
    if lost == 0 and tie == 0:
        money += 2 * bet
    if lost == 0 and tie == 1:
        money += bet


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
