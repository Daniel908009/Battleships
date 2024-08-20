# necessary imports
import tkinter
import random
import os
import sys

# function to start a new game
def new_game():
    # filling the buttons list based on the new map size
    global buttons
    for i in range(num_of_players):
        buttons.append([])
        for j in range(map_size):
            buttons[i].append([])
            for k in range(map_size):
                buttons[i][j].append([])
    # creating the reset button and settings button
    reset_button = tkinter.Button(button_frame, text="Reset",width=button_width, height=button_height ,command=lambda: reset())
    reset_button.grid(row=0, column=0)
    settings_button = tkinter.Button(button_frame, text="Settings", width=button_width, height=button_height, command=lambda: settings())
    settings_button.grid(row=0, column=1)

    # first faze of the game, the placement of the boats
    for i in range(num_of_players):
        current_player = players[i]
        choose_faze()
        remove_tiles()
        hold_screen()

    # half fazes of the game, deleting the buttons of the boat selection
    for widget in boat_frame.winfo_children():
        widget.destroy()

    # second faze of the game, the actual game, 
    # players will take turns to guess the possition of the boats of the other player
    # the player that guesses all of the boats/tiles of the boats of the other player wins
    for i in range(map_size):
        for j in range(map_size):
            buttons[int(current_player)-1][i][j] = tkinter.Button(frame, text=" ", width=board_button_width, height=board_button_height, command=lambda i=i, j=j: button_pressed(i, j))
            buttons[int(current_player)-1][i][j].grid(row=i, column=j)
        window.update()
        if current_player == players[0]:
            current_player = players[1]
        else:
            current_player = players[0]


# function to reset the game
def reset():
    global board_button_height,board_button_width, button_height, button_width, select_height, select_width, main_label_size
        # READJUSTING THE BUTTONS AND LABELS
    # readjust the bottom buttons
    button_width = int(window.winfo_height() // map_size /10)
    button_height = int(button_width // 5)
    # readjust the main label
    main_label_size = int(window.winfo_height() // 20-2)
    # readjust the board button size
    board_button_width = int(window.winfo_height() // map_size /11)
    board_button_height = int(board_button_width // 2)
    # readjust the boat selection buttons
    select_width = int(window.winfo_height() // number_of_boats / 11)
    select_height = int(select_width // 5)
    # readjust the labels based on new information
    main_label.config(font=("Arial", main_label_size))
    info_label_main.config(font=("Arial", main_label_size-5), text="Info")
        # READJUSTING THE GAME
    # deleting all the different widgets in the windows and frames
    for widget in frame.winfo_children():
        widget.destroy()
    for widget in boat_frame.winfo_children():
        widget.destroy()
    for widget in button_frame.winfo_children():
        widget.destroy()
    
    # clearing the lists and variables and resetting them to their default values
    global boats_placed, current_player, possitions_of_boats, coords_of_boats, possitions_of_boats_temp, which_tiles_tried, tiles_hit, tiles_of_sunken_boats, number_of_players_boats, buttons
    # clearing the variables and lists
    possitions_of_boats.clear()
    coords_of_boats.clear()
    possitions_of_boats_temp.clear()
    which_tiles_tried.clear()
    tiles_hit.clear()
    tiles_of_sunken_boats.clear()
    number_of_players_boats.clear()
    buttons.clear()
    # setting to default values
    boats_placed = 0
    current_player = random.choice(players)
    possitions_of_boats = []
    coords_of_boats = []
    possitions_of_boats_temp = []
    which_tiles_tried = []
    tiles_hit = []
    tiles_of_sunken_boats = []
    number_of_players_boats = [[number_of_boats],[number_of_boats]]
    for i in range(num_of_players):
        tiles_hit.append([])
        which_tiles_tried.append([])
        possitions_of_boats.append([])
        coords_of_boats.append([])
        tiles_of_sunken_boats.append([])
    # starting a new game, this time with the new settings applied
    new_game()

# function that applies the settings that the player has chosen
def apply_settings(size_entry, resizable):
    # checking if the size of the map is in the correct range
    if int(size_entry) > 10 or int(size_entry) < 5:
        info_label_main.config(text="Map size must be between 5 and 10!")
        return None
    # if player checked the resizable checkbutton, the window will now be resizable
    if resizable:
        window.resizable(True, True)
    else:
        window.resizable(False, False)
    # changing the map size based on the entry of the player
    global map_size
    map_size = int(size_entry)
    # resetting the game so the changes can take effect
    reset()
    
# function to open settings window
def settings():
    global map_size, number_of_boats
    # settings of the settings window
    settings_window = tkinter.Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("400x400")
    settings_window.resizable(False, False)
    settings_window.iconbitmap(os.path.join(base_path, "boat.ico"))
    # creating the main settings label
    settings_label = tkinter.Label(settings_window, text="Settings", font=("Arial", 20))
    settings_label.pack(side="top")
    # creating the frame for the settings
    settings_frame = tkinter.Frame(settings_window)
    settings_frame.pack()
    # creating a setting for the map size
    e1 = tkinter.StringVar()
    e1.set(map_size)
    map_size_label = tkinter.Label(settings_frame, text="Map size", font=("Arial", 12))
    map_size_label.grid(row=0, column=0)
    map_size_entry = tkinter.Entry(settings_frame, width=10, textvariable=e1)
    map_size_entry.grid(row=0, column=1)
    # creating a label informing the player about the max value and the min value of the map size
    map_size_info_label = tkinter.Label(settings_frame, text="Max: 10, Min: 5", font=("Arial", 10))
    map_size_info_label.grid(row=0, column=2)
    # creating a checkbutton, that can be selected when player wants to have a resizable window
    resizable = tkinter.BooleanVar()
    if window.resizable():
        resizable.set(True)
    else:
        resizable.set(False)
    resizable_checkbutton = tkinter.Checkbutton(settings_frame, variable=resizable)
    resizable_checkbutton.grid(row=1, column=1)
    # creating a label for the resizable checkbutton
    resizable_label = tkinter.Label(settings_frame, text="Resizable window", font=("Arial", 10))
    resizable_label.grid(row=1, column=0)

    # creating the apply button
    apply_button = tkinter.Button(settings_window, text="Apply", width=9, height=2, command=lambda: apply_settings(map_size_entry.get(), resizable.get()))
    apply_button.pack(side="bottom")

    settings_window.mainloop()
    

# function to check if someone has won
def check_win():
    global number_of_players_boats, current_player
    other_player = 0
    if current_player == players[0]:
        other_player = players[1]
    else:
        other_player = players[0]
    if number_of_players_boats[int(other_player)-1][0] == 0:
        return True
    else:
        return False

# function to inform the players about the game results 
def info_win():
    # creating a win info window with 4 button frames, two for each player, first window shows their possitions of the boats
    # the second window shows the guesses the boats by the other player
    win_info_window = tkinter.Toplevel(window)
    win_info_window.title("Game results")
    win_info_window.geometry("800x800")
    win_info_window.resizable(False, False)
    win_info_window.iconbitmap("boat.ico")
    # creating the main label for the win info window
    win_info_label = tkinter.Label(win_info_window, text="Game results", font=("Arial", 20))
    win_info_label.pack(side="top")
    # creating the labels for the different frames
    top_label = tkinter.Label(win_info_window, text="Player 1 boats X Player 2 boats", font=("Arial", 12))
    top_label.pack(side="top")
    # creating a frame for the frames and labels
    win_info_frame = tkinter.Frame(win_info_window)
    win_info_frame.pack()
    # creating the frames for the boat placement of the players
    player1_frame = tkinter.Frame(win_info_frame)
    player1_frame.grid(row=0, column=0)
    between_frame = tkinter.Frame(win_info_frame)
    between_frame.grid(row=0, column=1)
    player2_frame = tkinter.Frame(win_info_frame)
    player2_frame.grid(row=0, column=2)
    # horizontal line of labels filled with the text - to separate the frames
    text = "- - - - - - - - - - - - - - - -"
    between_label = tkinter.Label(win_info_frame, text=text, font=("Arial", 12))
    between_label.grid(row=1, column=0, columnspan=3)
    # creating the frames for the guesses of the players
    player1_guesses_frame = tkinter.Frame(win_info_frame)
    player1_guesses_frame.grid(row=2, column=0)
    between_frame2 = tkinter.Frame(win_info_frame)
    between_frame2.grid(row=2, column=1)
    player2_guesses_frame = tkinter.Frame(win_info_frame)
    player2_guesses_frame.grid(row=2, column=2)
    # filling the between frames with labels, 1 line of buttons, filled with the text |
    for i in range(map_size):
        between_label = tkinter.Label(between_frame, text="|", font=("Arial", 12))
        between_label.grid(row=i+1, column=0)
        between_label2 = tkinter.Label(between_frame2, text="|", font=("Arial", 12))
        between_label2.grid(row=i+1, column=0)
    # creating the buttons for the boat placement of the players
    for i in range(map_size):
        for j in range(map_size):
            player1_button = tkinter.Button(player1_frame, text=" ", width=2, height=1, state="disabled")
            player1_button.grid(row=i+1, column=j)
            player2_button = tkinter.Button(player2_frame, text=" ", width=2, height=1, state="disabled")
            player2_button.grid(row=i+1, column=j)
    # creating the buttons for the guesses of the players
    for i in range(map_size):
        for j in range(map_size):
            player1_guesses_button = tkinter.Button(player1_guesses_frame, text=" ", width=2, height=1, state="disabled")
            player1_guesses_button.grid(row=i+1, column=j)
            player2_guesses_button = tkinter.Button(player2_guesses_frame, text=" ", width=2, height=1, state=  "disabled")
            player2_guesses_button.grid(row=i+1, column=j)
    # changing the color of the buttons based on the lists coords_of_boats, the tiles that are in that list will be marked with green
    for i in range(len(coords_of_boats[0])):
        for j in range(len(coords_of_boats[0][i])-1):
            player1_frame.winfo_children()[coords_of_boats[0][i][j][0]*map_size+coords_of_boats[0][i][j][1]].config(bg="green")
    # the same goes for the second player
    for i in range(len(coords_of_boats[1])):
        for j in range(len(coords_of_boats[1][i])-1):
            player2_frame.winfo_children()[coords_of_boats[1][i][j][0]*map_size+coords_of_boats[1][i][j][1]].config(bg="green")

    # coloring the buttons based on the lists of the guesses of the players, tiles_hit will be marked with red, which_tiles_tried with blue and the sunken boats with black
    # blue missed first
    for i in range(len(which_tiles_tried[0])):
        player1_guesses_frame.winfo_children()[which_tiles_tried[0][i][0]*map_size+which_tiles_tried[0][i][1]].config(bg="blue")
    for i in range(len(which_tiles_tried[1])):
        player2_guesses_frame.winfo_children()[which_tiles_tried[1][i][0]*map_size+which_tiles_tried[1][i][1]].config(bg="blue")
    # red hits second
    for i in range(len(tiles_hit[0])):
        player1_guesses_frame.winfo_children()[tiles_hit[0][i][0]*map_size+tiles_hit[0][i][1]].config(bg="red")
    for i in range(len(tiles_hit[1])):
        player2_guesses_frame.winfo_children()[tiles_hit[1][i][0]*map_size+tiles_hit[1][i][1]].config(bg="red")
    # black sunken boats last
    for i in range(len(tiles_of_sunken_boats[0])):
        player1_guesses_frame.winfo_children()[tiles_of_sunken_boats[0][i][0]*map_size+tiles_of_sunken_boats[0][i][1]].config(bg="black")
    for i in range(len(tiles_of_sunken_boats[1])):
        player2_guesses_frame.winfo_children()[tiles_of_sunken_boats[1][i][0]*map_size+tiles_of_sunken_boats[1][i][1]].config(bg="black")

    # creating a bottom label for the win info window
    bottom_label = tkinter.Label(win_info_window, text="Player 1 guesses X Player 2 guesses", font=("Arial", 12))
    bottom_label.pack()
    
    # creating the bottom button for the win info window
    close_button = tkinter.Button(win_info_window, text="Close", width=button_width, height=button_height, command=lambda: win_info_window.destroy())
    close_button.pack(side="bottom")
    
# function that is called when a button is pressed, basically it handles the guess of a player
def button_pressed(x, y):
    global current_player, number_of_players_boats, buttons, players, possitions_of_boats, which_tiles_tried, tiles_hit, coords_of_boats, tiles_of_sunken_boats
    widgets = []
    # creating a variable to hold the answer
    answer = "Miss"
    # creating a variable to hold the other player
    other_player = 0
    if current_player == players[0]:
        other_player = players[1]
    else:
        other_player = players[0]

    # clearing the widgets list before filling it with the widgets in the frame again
    widgets.clear()
    # getting all the widgets in the frame and adding them to the widgets list
    for widget in frame.winfo_children():
        widgets += [widget]
        widget.configure(bg="SystemButtonFace")
        widget.configure(text=" ")

    # all the tiles hit by the player that had a ship in them will be marked with an X
    for i in range(len(tiles_hit[int(other_player)-1])):
        for j in range(len(widgets)):
            if tiles_hit[int(other_player)-1][i] == [widgets[j].grid_info()["row"], widgets[j].grid_info()["column"]]:
                widgets[j].config(text="X")
                window.update()

    # marking the tiles that the other player has already tried in previous turns with red
    for i in range(len(which_tiles_tried[int(other_player)-1])):
        for j in range(len(widgets)):
            if which_tiles_tried[int(other_player)-1][i] == [widgets[j].grid_info()["row"], widgets[j].grid_info()["column"]]:
                # if the tile was a hit, it will be marked with red color, if it was a miss, it will be marked with blue
                if widgets[j].cget("text") == "X":
                    widgets[j].config(bg="red")
                else:
                    widgets[j].config(bg="blue")
    # marking the tiles of the sunken boats with black
    for i in range(len(tiles_of_sunken_boats[int(other_player)-1])):
        for j in range(len(widgets)):
            if tiles_of_sunken_boats[int(other_player)-1][i] == [widgets[j].grid_info()["row"], widgets[j].grid_info()["column"]]:
                widgets[j].config(bg="black")

    # checking if the player has hit a boat of the other player
    for i in range(len(possitions_of_boats[int(other_player)-1])):
        if possitions_of_boats[int(other_player)-1][i] == [x, y]:
            answer = "Hit"
            tiles_hit[int(current_player)-1].append([x, y])
            # checking if there have been more than 2 hits
            if len(tiles_hit[int(current_player)-1]) > 1:
                # checking what ship has been hit
                for j in range(len(coords_of_boats[int(other_player)-1])):
                    if [x, y] in coords_of_boats[int(other_player)-1][j]:
                        # finding how many tiles does the hit ship have
                        ship_size = len(coords_of_boats[int(other_player)-1][j])-1
                        # checking if enough tiles have been hit to sink the ship
                        if ship_size > len(tiles_hit[int(current_player)-1]):
                            pass
                        else:
                            # now checking if all the tiles of the hitten ship have been hit, if yes then they will be added to the list of the sunken boats
                            temp = True
                            for k in range(len(coords_of_boats[int(other_player)-1][j])-1):
                                if coords_of_boats[int(other_player)-1][j][k] not in tiles_hit[int(current_player)-1]:
                                    temp = False
                                    break
                            if temp:
                                for k in range(len(coords_of_boats[int(other_player)-1][j])-1):
                                    tiles_of_sunken_boats[int(current_player)-1].append(coords_of_boats[int(other_player)-1][j][k])
                                number_of_players_boats[int(other_player)-1][0] -= 1
                                break
                            
                pass
    which_tiles_tried[int(current_player)-1].append([x, y])
    info_label_main.config(text=answer)
    window.update()

    # checking if the player has won
    if check_win():
        main_label.config(text="Player " + current_player + " wins")
        # disabling all the buttons so the player can't press them anymore
        for widget in frame.winfo_children():
            widget.config(state="disabled")
        # calling the info_win function to inform the players about the game result
        info_label_main.config(text="Player " + current_player + " wins")
        info_win()
        return None
    else:
        # changing the player
        if current_player == players[0]:
            current_player = players[1]
        else:
            current_player = players[0]
        main_label.config(text="Player " + current_player + "'s turn")

# function to select a boat type from the boat selection
def select_boat(boat_type):
    global boat_select
    boat_selected = boat_type
    boat_select = boat_selected
    # finding the index of the selected boat
    for i in range(len(boat_types)):
        if boat_selected == boat_types[i]:
            boat_index = i
    # making the button with the selected boat type stay pressed
    boat_button[boat_index].config(relief="sunken")
    # making the other buttons normal
    for i in range(len(boat_types)):
        if i != boat_index:
            boat_button[i].config(relief="raised")
    info_label_main.config(text="Boat selected" + " " + boat_selected)

# function to check if the tiles selected for the boat are next to each other
def tile_next_to_each_other(possitions):
    global boat_size, number_of_tiles_selected
    temp = True
    # checking if the tiles are next to each other
    for i in range(len(possitions)-1):
        if possitions[i][0] == possitions[i+1][0] and possitions[i][1] == possitions[i+1][1] - 1:
            temp = True
        elif possitions[i][0] == possitions[i+1][0] and possitions[i][1] == possitions[i+1][1] + 1:
            temp = True
        elif possitions[i][0] == possitions[i+1][0] - 1 and possitions[i][1] == possitions[i+1][1]:
            temp = True
        elif possitions[i][0] == possitions[i+1][0] + 1 and possitions[i][1] == possitions[i+1][1]:
            temp = True
        else:
            temp = False
            break
    return temp

# function to check if entered tiles are in a straight line(horizontal or vertical) if yes then everything is fine
# if not then the player will be informed that the boat is not straight and the tiles that have been selected for that boat will be cleared and removed from the lists
def is_straight(possitions):
    temp = True
    # checking if the tiles are in a straight line
    if len(possitions) > 1:
        if possitions[0][0] == possitions[1][0]:
            for i in range(len(possitions)-1):
                if possitions[i][0] != possitions[i+1][0]:
                    temp = False
                    break
        elif possitions[0][1] == possitions[1][1]:
            for i in range(len(possitions)-1):
                if possitions[i][1] != possitions[i+1][1]:
                    temp = False
                    break
        else:
            temp = False
    return temp

# function to place the boats on the game board
def place_boat(x, y):
    global boats_placed, current_player, boat_sizes, number_of_tiles_selected, buttons, boat_size, possitions_of_boats_temp, coords_of_boats, boat_select
    is_empty = True
    boat_size = 0
    
    # finding the size of the selected boat, this will be used to check if the entire boat has been placed
    for i in range(len(boat_types)):
        if boat_button[i].config("relief")[-1] == "sunken":
            boat_size = boat_sizes[i]

 # if no boat is selected, the player will be informed and the function will return None
    if boat_size == 0:
        info_label_main.config(text="No boat selected")
        return None
    else:
        while number_of_tiles_selected != boat_size:
            # checking if the boat is already placed on the selected tile
            for i in range(len(possitions_of_boats[int(current_player)-1])):
                if possitions_of_boats[int(current_player)-1][i] == [x, y]:
                    is_empty = False
            for i in range(len(possitions_of_boats_temp)):
                if possitions_of_boats_temp[i] == [x, y]:
                    is_empty = False
            if is_empty == False:
                is_empty = True
            else:
                number_of_tiles_selected += 1
                possitions_of_boats_temp.append([x, y])
                buttons[int(current_player)-1][x][y].config(bg="green")
                if number_of_tiles_selected == boat_size and tile_next_to_each_other(possitions_of_boats_temp) and is_straight(possitions_of_boats_temp):
                    boats_placed += 1
                    info_label_main.config(text="Boat placed")
                    #getting the coordinates of the boats stored in groups based on the size of the boat 
                    coords_of_boats[int(current_player)-1].append([])
                    for i in range(len(possitions_of_boats_temp)):
                        coords_of_boats[int(current_player)-1][boats_placed-1].append(possitions_of_boats_temp[i])
                    coords_of_boats[int(current_player)-1][boats_placed-1].append(boat_select)
                    # dissabling the boat select button and changing the relief of the selected button and making it red
                    for i in range(len(boat_types)):
                        if boat_button[i].config("relief")[-1] == "sunken":
                            boat_button[i].config(relief="raised")
                            boat_button[i].config(state="disabled")
                            boat_button[i].config(bg="red")
                    break
                if number_of_tiles_selected > 2 and is_straight(possitions_of_boats_temp) == False:
                    #reseting the tiles that have been selected for the boat and clearing the list of the selected tiles
                    for i in range(number_of_tiles_selected):
                        buttons[int(current_player)-1][possitions_of_boats_temp[i][0]][possitions_of_boats_temp[i][1]].config(bg="SystemButtonFace")
                    info_label_main.config(text="Boat is not straight")
                    # clears the lists and resets the buttons, so that the player can place all the boats again
                    possitions_of_boats_temp.clear()
                    break
                if tile_next_to_each_other(possitions_of_boats_temp) == False:
                    info_label_main.config(text="Tiles are not next to each other")
                    buttons[int(current_player)-1][x][y].config(bg="SystemButtonFace")
                    possitions_of_boats_temp.clear()
                    break
            window.update()
        # add the possitions of the boats to the actual list of the possitions of the boats(this is done because the positions are first checked if they are next to each other)    
        for i in range(len(possitions_of_boats_temp)):
            possitions_of_boats[int(current_player)-1].append(possitions_of_boats_temp[i])

        # checking if all the boats are placed, if so the function will return None
        if boats_placed == len(boat_types)-1:
            possitions_of_boats_temp.clear()
            number_of_tiles_selected = 0
            return None
        possitions_of_boats_temp.clear()
        number_of_tiles_selected = 0

# function to remove the tiles from the game board
def remove_tiles():
    for widget in frame.winfo_children():
        widget.destroy()

# function to set the button_pressed variable to True
def ready_button_change():
    global button_pressed_temp
    button_pressed_temp = True

# function to hold the screen until the bottom button is pressed
def hold_screen():
    temp2 = True
    global button_pressed_temp
    # creating the bottom button and text informing the player to press the button if he is ready
    ready_button = tkinter.Button(button_frame, text="Ready", width=button_width, height=button_height, command=lambda: ready_button_change())
    ready_button.grid(row=0, column=3)
    ready_label = tkinter.Label(button_frame, text="Press the ready button once you switched places with your oponent", font=("Arial", 12))
    ready_label.grid(row=0, column=4)
    while temp2:
        if button_pressed_temp:
            ready_button.grid_remove()
            ready_label.grid_remove()
            temp2 = False
            button_pressed_temp = False
        else:
            pass
        window.update()

# function for the placement of the boats faze
def choose_faze():
    global current_player, boats_placed, boat_button
    temp = True
    # creating the buttons list for the boat selection
    for i in range(number_of_boats):
        boat_button.append([])
    # creating the buttons for the boat selection
    for i in range(number_of_boats):
        boat_button[i] = tkinter.Button(boat_frame, text=boat_types[i] + " (" + str(boat_sizes[i]) + ")", width=select_width, height=select_height, command=lambda i=i: select_boat(boat_types[i]))
        boat_button[i].grid(row=0, column=i)

    # creating the chossing buttons for the selected player, basically the game board for the ships of the player
    for i in range(map_size):
        for j in range(map_size):
            buttons[int(current_player)-1][i][j] = tkinter.Button(frame, text=" ", width=board_button_width, height=board_button_height, command=lambda i=i, j=j: place_boat(i, j))
            buttons[int(current_player)-1][i][j].grid(row=i, column=j)

    # holding the screen until the player places all of his boats
    while temp:
        if boats_placed == len(boat_types):
            boats_placed = 0
            if current_player == players[0]:
                current_player = players[1]
                temp = False
            else:
                current_player = players[0]
                temp = False
        else:
            pass
        try:
            main_label.config(text="Player " + current_player + "'s turn")
        except:
            pass
        window.update()

# variables for the map, players, buttons, etc.
button_pressed_temp = False
boat_button = []
running = True
map_size = 5
number_of_tiles = map_size * map_size
num_of_players = 2
number_of_boats = 5
boats_placed = 0
number_of_tiles_selected = 0
boat_types = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
boat_select = ""
boat_sizes = [5, 4, 3, 3, 2]
players = ["1", "2"]
current_player = random.choice(players)
possitions_of_boats = []
coords_of_boats = []
possitions_of_boats_temp = []
which_tiles_tried = []
tiles_hit = []
tiles_of_sunken_boats = []
number_of_players_boats = [[number_of_boats],[number_of_boats]]
board_button_height = 0
board_button_width = 0
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

for i in range(num_of_players):
    tiles_hit.append([])
    which_tiles_tried.append([])
    possitions_of_boats.append([])
    coords_of_boats.append([])
    tiles_of_sunken_boats.append([])

buttons = []
for i in range(num_of_players):
    buttons.append([])
    for j in range(map_size):
        buttons[i].append([])
        for k in range(map_size):
            buttons[i][j].append([])

# creating the main window of the game
window = tkinter.Tk()
window.title("Battleships")
window.geometry("800x600")
window.resizable(True, True)
window.iconbitmap(os.path.join(base_path, "boat.ico"))
# setting the button height and width based on the window size
button_width = int(window.winfo_height() // map_size /10)
button_height = int(button_width // 5)
# setting the label size based on the window size
main_label_size = int(window.winfo_height() // 20-2)
# setting the board button height and width based on the window size and the map size
board_button_width = int(window.winfo_height() // map_size /11)
board_button_height = int(board_button_width // 2)
# setting the select button height and width based on the window size and the number of boats
select_width = int(window.winfo_height() // number_of_boats / 11)
select_height = int(select_width // 5)

# creating a top label for the game, displaying the current player
main_label = tkinter.Label(window, text="Player " + current_player + "'s turn", font=("Arial", main_label_size))
main_label.pack(side="top")

# creating an info label for the game(this label shows if player has hit a boat or not, or if there is a problem with the placement of the boats, etc.)
info_label_main = tkinter.Label(window, text="Info", font=("Arial", main_label_size-5))
info_label_main.pack(side="top")

# creating the game board
frame = tkinter.Frame(window)
frame.pack()

# creating a frame for the boat selection
boat_frame = tkinter.Frame(window)
boat_frame.pack()

# creating a frame for the buttons, representing the game board for the ships
button_frame = tkinter.Frame(window)
button_frame.pack(side="bottom")

# creating the reset button and settings button
reset_button = tkinter.Button(button_frame, text="Reset",width=button_width, height=button_height ,command=lambda: reset())
reset_button.grid(row=0, column=0)
settings_button = tkinter.Button(button_frame, text="Settings", width=button_width, height=button_height, command=lambda: settings())
settings_button.grid(row=0, column=1)

# first faze of the game, the placement of the boats
for i in range(num_of_players):
    current_player = players[i]
    choose_faze()
    remove_tiles()
    hold_screen()

# half fazes of the game, deleting the buttons of the boat selection
for widget in boat_frame.winfo_children():
    widget.destroy()

# second faze of the game, the actual game, 
# players will take turns to guess the possition of the boats of the other player
# the player that guesses all of the boats/tiles of the boats of the other player wins
for i in range(map_size):
    for j in range(map_size):
        buttons[int(current_player)-1][i][j] = tkinter.Button(frame, text=" ", width=board_button_width, height=board_button_height, command=lambda i=i, j=j: button_pressed(i, j))
        buttons[int(current_player)-1][i][j].grid(row=i, column=j)
    window.update()
    if current_player == players[0]:
        current_player = players[1]
    else:
        current_player = players[0]


window.mainloop()