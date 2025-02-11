import socket
from cards import deck
import random

# Get number of players from server terminal
p = int(input("Enter number of players: "))

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(p)

clients = []
players_list = [f'p{i+1}' for i in range(p)]

# Accept clients up to the specified number
for i in range(p):
    client_socket, addr = server_socket.accept()
    assigned_name = players_list[i]
    
    # Create reader and writer for the client socket
    reader = client_socket.makefile('r')
    writer = client_socket.makefile('w')
    
    # Send welcome message with assigned name
    writer.write(f"Welcome! You are {assigned_name}\n")
    writer.flush()
    
    # Store client details
    clients.append((assigned_name, client_socket, reader, writer))
    print(f"Player {assigned_name} connected from {addr}")

server_socket.close()

# Wait for server to start the game
input("All players joined. Press Enter to start the game...")

# Prepare game variables
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

no_of_players = p

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
# Game loop
try:
    while True:        
        # Find current player's reader and writer
        current_reader = None
        current_writer = None
        for name, sock, reader, writer in clients:
            if name == current_player:
                current_reader = reader
                current_writer = writer
                break
        
        top_card = discard_deck[-1]  

        current_writer.write(f"Top card: {top_card}\n")
        

        current_writer.write(f"{current_player}'s turn\n")
        

        current_writer.write(f"{current_player}'s deck: {players_deck.get(current_player)}\n")
        

        if top_card["color"] != "Wild":
            playing_color = top_card["color"]
        
        current_writer.write(f"Playing color: {playing_color}\n")
        

        if Roulette == True:
            current_writer.write("Select a color: Red, Green, Blue, Yellow\n")

            #selected_color = input()
            current_writer.flush() 
            try:
                response = current_reader.readline().strip()
                selected_color = response
            except ConnectionResetError:
                print(f"{current_player} disconnected. Exiting.")
                break
            
            current_writer.write(f"Selected color: {selected_color}\n")
            

            playing_color = selected_color
            players_deck.get(current_player).append(shuffled_deck.pop())

            current_writer.write(f"Cards picked : {players_deck.get(current_player)[-1]}\n")
            

            while players_deck.get(current_player)[-1]["color"] != selected_color:
                players_deck.get(current_player).append(shuffled_deck.pop())

                current_writer.write(f"Cards picked : {players_deck.get(current_player)[-1]}\n")
                

            Roulette = False
        
        else:
            if len(draw_stack) > 0:

                current_writer.write(f"Draw stack: {draw_stack}\n")



                current_writer.write("Do you want to draw card or stack? (D/S)\n")


                #draw_stack_choice = input()
                current_writer.flush()
                try:
                    response = current_reader.readline().strip()
                    draw_stack_choice = response
                except ConnectionResetError:
                    print(f"{current_player} disconnected. Exiting.")
                    break

                if draw_stack_choice == "D":
                    players_deck.get(current_player).extend(draw_stack)
                    draw_stack = []
                else:
                    valid_staking_cards = find_staking_cards(players_deck.get(current_player), top_card, playing_color)

                    current_writer.write(f"Valid indices: {valid_staking_cards}\n")


                    if len(valid_staking_cards) > 0:

                        current_writer.write("Select a card to play\n")


                        #selected_card_index = int(input())
                        current_writer.flush() 
                        try:
                            response = current_reader.readline().strip()
                            selected_card_index = int(response)
                        except ConnectionResetError:
                            print(f"{current_player} disconnected. Exiting.")
                            break
            
                        while selected_card_index not in valid_staking_cards:

                            current_writer.write("Invalid card. Please select a valid card.\n")


                            #selected_card_index = int(input())
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                selected_card_index = int(response)
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                        selected_card = players_deck.get(current_player).pop(selected_card_index)
                    
                        current_writer.write(f"Selected card: {selected_card}\n")


                        if selected_card["type"] == "Draw Two":
                            # Next player draws 2 cards                    
                            for i in range(2):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Draw Four":
                            # Next player draws 4 cards                    
                            for i in range(4):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Reverse Draw Four":

                            current_writer.write("Select a color: Red, Green, Blue, Yellow\n")


                            #selected_color = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                selected_color = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                            current_writer.write(f"Selected color: {selected_color}\n")


                            playing_color = selected_color

                            if len(players_list) >= 3:
                                players_list = [players_list[0]] + players_list[:0:-1] 
                            else:
                                players_list.reverse()

                            # Next player draws 4 cards                    
                            for i in range(4):
                                draw_stack.append(shuffled_deck.pop())
                            

                        elif selected_card["type"] == "Draw Six":

                            current_writer.write("Select a color: Red, Green, Blue, Yellow\n")

                            #selected_color = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                selected_color = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                            current_writer.write(f"Selected color: {selected_color}\n")

                            playing_color = selected_color
                            
                            # Next player draws 6 cards                    
                            for i in range(6):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Draw Ten":

                            current_writer.write("Select a color: Red, Green, Blue, Yellow\n")

                            #selected_color = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                selected_color = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                            current_writer.write(f"Selected color: {selected_color}\n")


                            playing_color = selected_color
                            
                            # Next player draws 10 cards                    
                            for i in range(10):
                                draw_stack.append(shuffled_deck.pop())

                        discard_deck.append(selected_card)

                        current_writer.write(f"Discard deck: {discard_deck}\n")

                        
                    else:

                        current_writer.write("No valid cards to play. Drawing Cards\n")


                        players_deck.get(current_player).extend(draw_stack)
                        draw_stack = []
                
            else:                                   
                valid_indices = find_valid_cards(players_deck.get(current_player), discard_deck, playing_color)

                current_writer.write(f"Valid indices: {valid_indices}\n")
      

                if len(valid_indices) == 0:
                    while len(valid_indices) == 0:

                        current_writer.write("No valid cards to play.\n")


                        while True:

                            current_writer.write("Do you want to draw a card? (Y/N)\n")


                            #draw_card = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                draw_card = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                            if draw_card == "Y":
                                players_deck.get(current_player).append(shuffled_deck.pop())

                                current_writer.write(f"{current_player}'s deck: {players_deck.get(current_player)}\n")


                                valid_indices = find_valid_cards(players_deck.get(current_player), discard_deck, playing_color)

                                current_writer.write(f"Valid indices: {valid_indices}\n")

                            else:
                                break
                    continue

                else:

                    current_writer.write("Do you want to draw a card or play a card? (D/P) \n")


                    #case = input()
                    current_writer.flush() 
                    try:
                        response = current_reader.readline().strip()
                        case = response
                    except ConnectionResetError:
                        print(f"{current_player} disconnected. Exiting.")
                        break

                    if case == "D":
                        players_deck[current_player].append(shuffled_deck.pop())

                        current_writer.write(f"{current_player}'s deck: {players_deck.get(current_player)}\n")


                        while True:

                            current_writer.write("Do you want to draw another card? (Y/N)\n")


                            #draw_card = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                draw_card = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                            if draw_card == "Y":
                                players_deck.get(current_player).append(shuffled_deck.pop())

                                current_writer.write(f"{current_player}'s deck: {players_deck.get(current_player)}\n")


                                valid_indices = find_valid_cards(players_deck.get(current_player), discard_deck, playing_color)

                                current_writer.write(f"Valid indices: {valid_indices}\n")


                            else:
                                break
                        continue
                    
                    else:

                        current_writer.write("Select a card to play\n")


                        #selected_card_index = int(input())
                        current_writer.flush() 
                        try:
                            response = current_reader.readline().strip()
                            selected_card_index = int(response)
                        except ConnectionResetError:
                            print(f"{current_player} disconnected. Exiting.")
                            break

                        while selected_card_index not in valid_indices:

                            current_writer.write("Invalid card. Please select a valid card.\n")


                            # selected_card_index = int(input())
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                selected_card_index = int(response)
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                        selected_card = players_deck.get(current_player).pop(selected_card_index)

                        current_writer.write(f"Selected card: {selected_card}\n")


                        if selected_card["type"] == "Draw Six":

                            current_writer.write("Select a color: Red, Green, Blue, Yellow\n")


                            #selected_color = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                selected_color = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                            current_writer.write(f"Selected color: {selected_color}\n")


                            playing_color = selected_color
                            
                            # Next player draws 6 cards                    
                            for i in range(6):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Draw Ten":

                            current_writer.write("Select a color: Red, Green, Blue, Yellow\n")


                            #selected_color = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                selected_color = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                            current_writer.write(f"Selected color: {selected_color}\n")


                            playing_color = selected_color
                            
                            # Next player draws 10 cards                    
                            for i in range(10):
                                draw_stack.append(shuffled_deck.pop())

                        elif selected_card["type"] == "Reverse Draw Four":
                            
                            current_writer.write("Select a color: Red, Green, Blue, Yellow\n")


                            #selected_color = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                selected_color = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break

                            current_writer.write(f"Selected color: {selected_color}\n")


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

                            current_writer.write(f"Valid color indexes: {valid_color_indexes}\n")


                            for i in valid_color_indexes:

                                current_writer.write(f"{i}: {players_deck.get(current_player)[i]}\n")


                                current_writer.write("Do you want to discard this card? (Y/N)\n")


                                #discard_card = input()
                                current_writer.flush() 
                                try:
                                    response = current_reader.readline().strip()
                                    discard_card = response
                                except ConnectionResetError:
                                    print(f"{current_player} disconnected. Exiting.")
                                    break

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

                            current_writer.write("Players' hands have been rotated!\n")
                            current_writer.flush()

                        elif selected_card["type"] == "7": 
                            # Prompt the current player to choose another player

                            current_writer.write(f"Choose a player to swap hands with (available players: {[p for p in players_list if p != current_player]}):\n")


                            #chosen_player = input()
                            current_writer.flush() 
                            try:
                                response = current_reader.readline().strip()
                                chosen_player = response
                            except ConnectionResetError:
                                print(f"{current_player} disconnected. Exiting.")
                                break
                            
                            # Validate the chosen player
                            while chosen_player not in players_list or chosen_player == current_player:

                                current_writer.write("Invalid player. Please choose a valid player.\n")

                                #chosen_player = input()
                                current_writer.flush() 
                                try:
                                    response = current_reader.readline().strip()
                                    chosen_player = response
                                except ConnectionResetError:
                                    print(f"{current_player} disconnected. Exiting.")
                                    break
                            
                            # Swap hands between the current player and the chosen player
                            current_player_hand = players_deck[current_player]
                            chosen_player_hand = players_deck[chosen_player]
                            
                            players_deck[current_player] = chosen_player_hand
                            players_deck[chosen_player] = current_player_hand
                            
                            current_writer.write(f"{current_player} and {chosen_player} have swapped hands!\n")


                        discard_deck.append(selected_card)

                        current_writer.write(f"Discard deck: {discard_deck}\n")

                        
        if len(players_deck.get(current_player)) == 0:

            current_writer.write(f"{current_player} wins!\n")

            break

        if len(discard_deck > 1):
            shuffled_deck.extend(discard_deck[:-1])
            shuffle(shuffled_deck)
            discard_deck = discard_deck[-1:]

        if len(players_deck.get(current_player) >= 25):

            current_writer.write(f"{current_player} has 25 cards. {current_player} loses!\n")


            shuffled_deck.extend(players_deck.get(current_player))
            shuffled_deck = shuffle(shuffled_deck)
            del players_deck[current_player]
            players_list.remove(current_player)
            break            
        
        # Pop the 1st player and add to the end of the list
        players_list.append(players_list.pop(0))
        current_player = players_list[0]

finally:
    # Close all client connections
    for name, sock, reader, writer in clients:
        writer.close()
        reader.close()
        sock.close()
    print("Server shutdown. All connections closed.")