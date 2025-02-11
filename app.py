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

def find_staking_cards(player_deck, top_card, playing_color):
    valid_staking_cards = []
    
    if top_card["type"] == "Draw Two":
        for i, player_card in enumerate(player_deck):
            if player_card["type"] == "Draw Two" or player_card["type"] == "Reverse Draw Four" or player_card["type"] == "Draw Six" or player_card["type"] == "Draw Ten":
                valid_staking_cards.append(i)
            elif player_card["color"] == playing_color and player_card["type"] == "Draw Four":
                valid_staking_cards.append(i)

    elif top_card["type"] == "Draw Four":
        for i, player_card in enumerate(player_deck):
            if player_card["type"] == "Draw Four" or player_card["type"] == "Reverse Draw Four" or player_card["type"] == "Draw Six" or player_card["type"] == "Draw Ten":
                valid_staking_cards.append(i)

    elif top_card["type"] == "Reverse Draw Four":
        for i, player_card in enumerate(player_deck):
            if player_card["type"] == "Reverse Draw Four" or player_card["type"] == "Draw Six" or player_card["type"] == "Draw Ten":
                valid_staking_cards.append(i)
    
    elif top_card["type"] == "Draw Six":
        for i, player_card in enumerate(player_deck):
            if player_card["type"] == "Draw Six" or player_card["type"] == "Draw Ten":
                valid_staking_cards.append(i)

    elif top_card["type"] == "Draw Tex":
        for i, player_card in enumerate(player_deck):
            if player_card["type"] == "Draw Ten":
                valid_staking_cards.append(i)

    return valid_staking_cards

def find_valid_color_index(player_deck, color):
    valid_color_indexes = []
    for i, player_card in enumerate(player_deck):
        if player_card["color"] == color:
            valid_color_indexes.append(i)
    return valid_color_indexes

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
        start_card = shuffled_deck.pop()  # Draw a new card3


    # Initialize discard deck and add the start card
    discard_deck.append(start_card)

    # Distribute cards to players
    players_deck, shuffled_deck = distribute_cards(no_of_players, shuffled_deck)

    print(players_deck)

    players_list = list(players_deck.keys())

    
    current_player = players_list[0]

    playing_color = discard_deck[-1]["color"]

    draw_stack  = []

    Roulette = False

    while True:
        top_card = discard_deck[-1]        
        print(f"Top card: {top_card}")  

        print(f"{current_player}'s turn")

        print(f"{current_player}'s deck: {players_deck.get(current_player)}")

        if top_card["color"] != "Wild":
            playing_color = top_card["color"]
        
        print(f"Playing color: {playing_color}")

        if Roulette == True:
            print("Select a color: Red, Green, Blue, Yellow")
            selected_color = input()
            print(f"Selected color: {selected_color}")
            playing_color = selected_color
            players_deck.get(current_player).append(shuffled_deck.pop())
            print(f"Cards picked : {players_deck.get(current_player)[-1]}")
            while players_deck.get(current_player)[-1]["color"] != selected_color:
                players_deck.get(current_player).append(shuffled_deck.pop())
                print(f"Cards picked : {players_deck.get(current_player)[-1]}")
            Roulette = False
        
        else:
            if len(draw_stack) > 0:
                print(f"Draw stack: {draw_stack}")
                print("Do you want to draw card or stack? (D/S)")
                draw_stack_choice = input()
                if draw_stack_choice == "D":
                    players_deck.get(current_player).extend(draw_stack)
                    draw_stack = []
                else:
                    valid_staking_cards = find_staking_cards(players_deck.get(current_player), top_card, playing_color)
                    print(f"Valid indices: {valid_staking_cards}")
                    if len(valid_staking_cards) > 0:
                        print("Select a card to play")
                        selected_card_index = int(input())
                        while selected_card_index not in valid_staking_cards:
                            print("Invalid card. Please select a valid card.")
                            selected_card_index = int(input())
                        selected_card = players_deck.get(current_player).pop(selected_card_index)
                        print(f"Selected card: {selected_card}")

                        if selected_card["type"] == "Draw Two":
                            # Next player draws 2 cards                    
                            for i in range(2):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Draw Four":
                            # Next player draws 4 cards                    
                            for i in range(4):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Reverse Draw Four":
                            print("Select a color: Red, Green, Blue, Yellow")
                            selected_color = input()
                            print(f"Selected color: {selected_color}")
                            playing_color = selected_color

                            if len(players_list) >= 3:
                                players_list = [players_list[0]] + players_list[:0:-1] 
                            else:
                                players_list.reverse()

                            # Next player draws 4 cards                    
                            for i in range(4):
                                draw_stack.append(shuffled_deck.pop())
                            

                        elif selected_card["type"] == "Draw Six":
                            print("Select a color: Red, Green, Blue, Yellow")
                            selected_color = input()
                            print(f"Selected color: {selected_color}")
                            playing_color = selected_color
                            
                            # Next player draws 6 cards                    
                            for i in range(6):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Draw Ten":
                            print("Select a color: Red, Green, Blue, Yellow")
                            selected_color = input()
                            print(f"Selected color: {selected_color}")
                            playing_color = selected_color
                            
                            # Next player draws 10 cards                    
                            for i in range(10):
                                draw_stack.append(shuffled_deck.pop())

                        discard_deck.append(selected_card)
                        print(f"Discard deck: {discard_deck}")
                        
                    else:
                        print("No valid cards to play. Drawing Cards")
                        players_deck.get(current_player).extend(draw_stack)
                        draw_stack = []
                
            else:                                   
                valid_indices = find_valid_cards(players_deck.get(current_player), discard_deck, playing_color)
                print(f"Valid indices: {valid_indices}")            

                if len(valid_indices) == 0:
                    while len(valid_indices) == 0:
                        print("No valid cards to play.")
                        while True:
                            print("Do you want to draw a card? (Y/N)")
                            draw_card = input()
                            if draw_card == "Y":
                                players_deck.get(current_player).append(shuffled_deck.pop())
                                print(f"{current_player}'s deck: {players_deck.get(current_player)}")
                                valid_indices = find_valid_cards(players_deck.get(current_player), discard_deck, playing_color)
                                print(f"Valid indices: {valid_indices}")
                            else:
                                break
                    continue

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
                                valid_indices = find_valid_cards(players_deck.get(current_player), discard_deck, playing_color)
                                print(f"Valid indices: {valid_indices}")
                            else:
                                break
                        continue
                    
                    else:
                        print("Select a card to play")
                        selected_card_index = int(input())

                        while selected_card_index not in valid_indices:
                            print("Invalid card. Please select a valid card.")
                            selected_card_index = int(input())

                        selected_card = players_deck.get(current_player).pop(selected_card_index)
                        print(f"Selected card: {selected_card}")

                        if selected_card["type"] == "Draw Six":
                            print("Select a color: Red, Green, Blue, Yellow")
                            selected_color = input()
                            print(f"Selected color: {selected_color}")
                            playing_color = selected_color
                            
                            # Next player draws 6 cards                    
                            for i in range(6):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Draw Ten":
                            print("Select a color: Red, Green, Blue, Yellow")
                            selected_color = input()
                            print(f"Selected color: {selected_color}")
                            playing_color = selected_color
                            
                            # Next player draws 10 cards                    
                            for i in range(10):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Reverse Draw Four":
                            print("Select a color: Red, Green, Blue, Yellow")
                            selected_color = input()
                            print(f"Selected color: {selected_color}")
                            playing_color = selected_color

                            if len(players_list) >= 3:
                                players_list = [players_list[0]] + players_list[:0:-1] 
                            else:
                                players_list.reverse()
                            
                            # Next player draws 4 cards                    
                            for i in range(4):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Color Roulette":
                            Roulette = True
                        
                        elif selected_card["type"] == "Skip":
                            players_list.append(players_list.pop(0))
                            current_player = players_list[0]

                        elif selected_card["type"] == "Skip All":
                            players_list.insert(0, players_list.pop())

                        elif selected_card["type"] == "Reverse":
                            if len(players_list) >= 3:
                                players_list = [players_list[0]] + players_list[:0:-1] 
                            else:
                                players_list.reverse()

                        elif selected_card["type"] == "Draw Two":
                            for i in range(2):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Draw Four":
                            for i in range(4):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Discard All of Color": 
                            valid_color_indexes = find_valid_color_index(players_deck.get(current_player), selected_card["color"])
                            print(f"Valid color indexes: {valid_color_indexes}")

                            for i in valid_color_indexes:
                                print(f"{i}: {players_deck.get(current_player)[i]}")
                                print("Do you want to discard this card? (Y/N)")
                                discard_card = input()
                                if discard_card == "Y":
                                    discard_deck.append(players_deck.get(current_player)[i])
                                    players_deck.get(current_player).pop(i)
                                else:
                                    continue

                        elif selected_card["type"] == "0": 
                            # Get list of current hands
                            hands = [players_deck[player] for player in players_list]

                            # Rotate hands to the left
                            rotated_hands = hands[1:] + [hands[0]]

                            # Assign the rotated hands back to players
                            for i, player in enumerate(players_list):
                                players_deck[player] = rotated_hands[i]

                            print("Players' hands have been rotated!")

                        elif selected_card["type"] == "7": 
                            # Prompt the current player to choose another player
                            print(f"Choose a player to swap hands with (available players: {[p for p in players_list if p != current_player]}):")
                            chosen_player = input()
                            
                            # Validate the chosen player
                            while chosen_player not in players_list or chosen_player == current_player:
                                print("Invalid player. Please choose a valid player.")
                                chosen_player = input()
                            
                            # Swap hands between the current player and the chosen player
                            current_player_hand = players_deck[current_player]
                            chosen_player_hand = players_deck[chosen_player]
                            
                            players_deck[current_player] = chosen_player_hand
                            players_deck[chosen_player] = current_player_hand
                            
                            print(f"{current_player} and {chosen_player} have swapped hands!")

                        discard_deck.append(selected_card)
                        print(f"Discard deck: {discard_deck}")
                        
        if len(players_deck.get(current_player)) == 0:
            print(f"{current_player} wins!")
            break

        if len(discard_deck > 1):
            shuffled_deck.extend(discard_deck[:-1])
            shuffle(shuffled_deck)
            discard_deck = discard_deck[-1:]

        if len(players_deck.get(current_player) >= 25):
            print(f"{current_player} has 25 cards. {current_player} loses!")
            shuffled_deck.extend(players_deck.get(current_player))
            shuffled_deck = shuffle(shuffled_deck)
            del players_deck[current_player]
            players_list.remove(current_player)
            break            
        
        # Pop the 1st player and add to the end of the list
        players_list.append(players_list.pop(0))
        current_player = players_list[0]        

        print()        
        print()
        print()

start_game()

# TODO: Implement the following special cards:
# - Implement Uno callout