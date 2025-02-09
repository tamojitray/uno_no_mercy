from cards import deck
import random

# Shuffle the deck function
def shuffle(deck):
    random.shuffle(deck)
    return deck

# Distribute cards to players function
def distribute_cards(no_of_players, shuffled_deck):
    players_deck = {}  # Dictionary to store players and their cards
    no_of_start_cards = 7  # Each player gets 7 cards

    for i in range(1, no_of_players + 1):
        key = f"p{i}"  # Player key (e.g., 'p1', 'p2', etc.)
        players_deck[key] = [shuffled_deck.pop() for _ in range(no_of_start_cards)]

    return players_deck, shuffled_deck

# Find valid cards to play function
def find_valid_cards(player_deck, discard_deck, playing_color):
    valid_indices = []
    top_card = discard_deck[-1]  # Get the last card (top of the discard pile)

    for i, player_card in enumerate(player_deck):
        if (player_card["color"] == playing_color or player_card["type"] == top_card["type"] or player_card["color"] == "Wild"):
            valid_indices.append(i)

    return valid_indices

# Start the game function
def start_game():

    print("No of players: ")
    no_of_players = int(input())
    discard_deck = []

    # Shuffling the deck
    shuffled_deck = shuffle(deck)

    # Draw the first card
    start_card = shuffled_deck.pop()

    # Ensure the first card is not a Wild card
    while start_card["color"] == "Wild":
        shuffled_deck.append(start_card)  # Put the Wild card back
        shuffled_deck = shuffle(shuffled_deck)  # Shuffle the deck again
        start_card = shuffled_deck.pop()  # Draw a new card

    # Initialize discard deck and add the start card
    discard_deck.append(start_card)

    # Distribute cards to players
    players_deck, shuffled_deck = distribute_cards(no_of_players, shuffled_deck)

    players_list = list(players_deck.keys())

    print("No of players: ")
    current_player = input() # user input

    playing_color = discard_deck[-1]["color"]

    while True:
        top_card = discard_deck[-1]        
        print(f"Top card: {top_card}")  

        print(f"{current_player}'s turn")

        print(f"{current_player}'s deck: {players_deck.get(current_player)}")

        if len(draw_stack) > 0:
            print(f"Draw stack: {draw_stack}")
            find_playable_cards = []
             

        valid_indices = find_valid_cards(players_deck.get(current_player), discard_deck, playing_color)
        print(f"Valid indices: {valid_indices}")

        draw_stack = []

        if len(valid_indices) == 0:
            while len(valid_indices) == 0:
                print("No valid cards to play.")
                while True:
                    print("Do you want to draw a card? (Y/N)")
                    draw_card = input()
                    if draw_card == "Y":
                        players_deck.get(current_player).append(shuffled_deck.pop())
                        print(f"{current_player}'s deck: {players_deck.get(current_player)}")
                        valid_indices = find_valid_cards(players_deck.get(current_player), discard_deck)
                        print(f"Valid indices: {valid_indices}")
                    else:
                        break
        else:
            print("Do you want to draw a card or play a card? (D/P) ")
            case = input()
            if case == "D":
                players_deck[current_player].append(shuffled_deck.pop())
                print(f"{current_player}'s deck: {players_deck.get(current_player)}")

                while True:
                    print("Do you want to draw another card? (Y/N)")
                    draw_card = input()
                    if draw_card == "Y":
                        players_deck.get(current_player).append(shuffled_deck.pop())
                        print(f"{current_player}'s deck: {players_deck.get(current_player)}")
                    else:
                        break
                continue


            elif case == "P":
                print("Select a card to play")
                selected_card_index = int(input())

                while selected_card_index not in valid_indices:
                    print("Invalid card. Please select a valid card.")
                    selected_card_index = int(input())

                selected_card = players_deck.get(current_player).pop(selected_card_index)
                print(f"Selected card: {selected_card}")

                if selected_card["color"] == "Wild" and selected_card["type"] == "Draw Six":
                    print("Select a color: Red, Green, Blue, Yellow")
                    selected_color = input()
                    print(f"Selected color: {selected_color}")
                    playing_color = selected_color
                    
                    # Next player draws 6 cards                    
                    for i in range(6):
                        draw_stack.append(shuffled_deck.pop())

                elif selected_card["color"] == "Wild" and selected_card["type"] == "Draw Ten":
                    pass

                elif selected_card["color"] == "Wild" and selected_card["type"] == "Reverse Draw Four":
                    pass

                elif selected_card["color"] == "Wild" and selected_card["type"] == "Color Roulette":
                    pass
                
                elif selected_card["type"] == "Skip":
                    pass

                elif selected_card["type"] == "Skip All":
                    pass

                elif selected_card["type"] == "Reverse":
                    pass

                elif selected_card["type"] == "Draw Two":
                    pass

                elif selected_card["type"] == "Draw Four":
                    pass

                elif selected_card["type"] == "Discard All of Color":
                    pass

                elif selected_card["type"] == "0":
                    pass

                elif selected_card["type"] == "7":
                    pass
                
                else:
                    discard_deck.append(selected_card)
                    print(f"Discard deck: {discard_deck}")


                if len(players_deck.get(current_player)) == 0:
                    print(f"{current_player} wins!")
                    break

        next_player = players_list.index(current_player) + 1
        current_player = players_list[next_player % no_of_players]









start_game()


