# necessary imports
import tkinter
import random
import time
import threading

# function to reset the game
def reset():
    pass

# function to open settings window
def settings():
    global map_size, number_of_boats
    # settings of the settings window
    settings_window = tkinter.Toplevel(window)
    settings_window.title("Settings")
    settings_window.geometry("400x400")
    settings_window.resizable(False, False)
    settings_window.iconbitmap("boat.ico")
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
    # creating a setting for the number of boats
    e2 = tkinter.StringVar()
    e2.set(number_of_boats)
    number_of_boats_label = tkinter.Label(settings_frame, text="Number of boats", font=("Arial", 12))
    number_of_boats_label.grid(row=1, column=0)
    number_of_boats_entry = tkinter.Entry(settings_frame, width=10, textvariable=e2)
    number_of_boats_entry.grid(row=1, column=1)

    # creating the apply button
    apply_button = tkinter.Button(settings_window, text="Apply", width=9, height=2)
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
def info_win(player, black_tiles, red_tiles, blue_tiles):
    # coloring the game board based on who won
    pass
    
# function that is called when a button is pressed, basically it handles the guess of a player
def button_pressed(x, y):
    global current_player, number_of_players_boats, buttons, players, possitions_of_boats, which_tiles_tried, tiles_hit, coords_of_boats, tiles_of_sunken_boats
    widgets = []
    #print(str(coords_of_boats) + "coords of boats")
    #print(coords_of_boats[int(current_player)-1])
    #print(coords_of_boats[int(current_player)-1][0])
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
                #print("X added")
                window.update()

    # marking the tiles that the other player has already tried in previous turns with red
    for i in range(len(which_tiles_tried[int(other_player)-1])):
        for j in range(len(widgets)):
            if which_tiles_tried[int(other_player)-1][i] == [widgets[j].grid_info()["row"], widgets[j].grid_info()["column"]]:
                # if the tile was a hit, it will be marked with red color, if it was a miss, it will be marked with blue
                if widgets[j].cget("text") == "X":
                    widgets[j].config(bg="red")
                    #print("X marked red")
                else:
                    widgets[j].config(bg="blue")
                    #print("Miss marked blue")
    # marking the tiles of the sunken boats with black
    for i in range(len(tiles_of_sunken_boats[int(other_player)-1])):
        for j in range(len(widgets)):
            if tiles_of_sunken_boats[int(other_player)-1][i] == [widgets[j].grid_info()["row"], widgets[j].grid_info()["column"]]:
                widgets[j].config(bg="black")
                #print("Sunken boat marked black")

    # checking if the player has hit a boat of the other player
    for i in range(len(possitions_of_boats[int(other_player)-1])):
        if possitions_of_boats[int(other_player)-1][i] == [x, y]:
            #widgets[x*map_size+y].config(text="X")
            answer = "Hit"
            tiles_hit[int(current_player)-1].append([x, y])
            #print(x, y)
            #print("added to tiles hit")
            # checking if there have been more than 2 hits
            if len(tiles_hit[int(current_player)-1]) > 1:
                # checking what ship has been hit
                for j in range(len(coords_of_boats[int(other_player)-1])):
                    if [x, y] in coords_of_boats[int(other_player)-1][j]:
                        #print("//////////////////////////")
                        #print(coords_of_boats[int(other_player)-1][j].index([x, y]))
                        #print("this is the index")
                        # finding how many tiles does the hit ship have
                        ship_size = len(coords_of_boats[int(other_player)-1][j])-1
                        #print(str(ship_size) + " ship size")
                        #print("//////////////////////////")
                        # checking if enough tiles have been hit to sink the ship
                        if ship_size > len(tiles_hit[int(current_player)-1]):
                            #print("Ship not sunken")
                            pass
                        else:
                            # now checking if all the ships tiles are in the tiles_hit list if so the ship is sunken
                            temp = True
                            for k in range(len(coords_of_boats[int(other_player)-1][j])-1):
                                if coords_of_boats[int(other_player)-1][j][k] not in tiles_hit[int(current_player)-1]:
                                    temp = False
                                    break
                            if temp:
                                #print("Ship sunken")
                                #number_of_players_boats[int(other_player)-1] = int(number_of_players_boats[int(other_player)-1] - 1)
                                number_of_players_boats[int(other_player)-1][0] -= 1
                                # adding the tiles of the sunken boat to the tiles_of_sunken_boats list so they can be marked with black
                                for k in range(len(coords_of_boats[int(current_player)-1][j])-1):
                                    tiles_of_sunken_boats[int(current_player)-1].append(coords_of_boats[int(current_player)-1][j][k])
                                #print("Boat sunken")
                                #print(number_of_players_boats)
                                #print(tiles_of_sunken_boats)
                                #print("//////////////////////////")
                                break
            else:
                pass
    which_tiles_tried[int(current_player)-1].append([x, y])
    print(answer + " answer is this" )
    window.update()

    # checking if the player has won
    if check_win():
        print("Player " + current_player + " wins")
        main_label.config(text="Player " + current_player + " wins")
        # disabling all the buttons so the player can't press them anymore
        for widget in frame.winfo_children():
            widget.config(state="disabled")
        # calling the info_win function to inform the players about the game result
        info_win(current_player)
        #button_pressed(x, y)
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
    #print(boat_selected)
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
    #print(temp)
    return temp

# function to check if all the tiles form a straight line(horizontal or vertical)
def is_straight(possitions):
    temp = True
    main_tile = possitions[0]
    # checking if the tiles are in a straight line with the first tile being the main tile
    for i in range(1, len(possitions)):
        if possitions[i][0] == main_tile[0] and possitions[i][1] == main_tile[1] + 1:
            temp = True
        elif possitions[i][0] == main_tile[0] and possitions[i][1] == main_tile[1] - 1:
            temp = True
        elif possitions[i][0] == main_tile[0] + 1 and possitions[i][1] == main_tile[1]:
            temp = True
        elif possitions[i][0] == main_tile[0] - 1 and possitions[i][1] == main_tile[1]:
            temp = True
        else:
            temp = False
            break
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
        print("No boat selected")
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
                #print("Boat already placed here") eventually add a label that will inform the player that the boat is already placed here
                is_empty = True
            else:
                number_of_tiles_selected += 1
                possitions_of_boats_temp.append([x, y])
                buttons[int(current_player)-1][x][y].config(bg="green")
                if number_of_tiles_selected == boat_size and tile_next_to_each_other(possitions_of_boats_temp):
                    boats_placed += 1
                    #print("Boat placed")
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
                if tile_next_to_each_other(possitions_of_boats_temp) == False:
                    print("Tiles are not next to each other")
                    buttons[int(current_player)-1][x][y].config(bg="white")
                    #print(possitions_of_boats_temp)
                    possitions_of_boats_temp.clear()
                    #print("temp cleared")
                    break
            window.update()

        # add the possitions of the boats to the actual list of the possitions of the boats(this is done because the positions are first checked if they are next to each other)    
        for i in range(len(possitions_of_boats_temp)):
            possitions_of_boats[int(current_player)-1].append(possitions_of_boats_temp[i])
            #print(possitions_of_boats_temp[i])
        # getting the coordinates of the boats in groups
        #for i in range(0, len(possitions_of_boats_temp), 2):
            #coords_of_boats[int(current_player)-1].append(possitions_of_boats_temp[i:i+2])

        #print(possitions_of_boats_temp)
        #print(coords_of_boats)
            # checking if all the boats are placed, if so the function will return None
        if boats_placed == len(boat_types)-1:
            #print(boats_placed, len(boat_types))
            possitions_of_boats_temp.clear()
            #print("temp cleared")
            number_of_tiles_selected = 0
            #print("All boats placed")
            return None
        possitions_of_boats_temp.clear()
        #print("temp cleared")
        number_of_tiles_selected = 0

# function to remove the tiles from the game board
def remove_tiles():
    #print(coords_of_boats)
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
    ready_button = tkinter.Button(button_frame, text="Ready", width=9, height=2, command=lambda: ready_button_change())
    ready_button.grid(row=0, column=2)
    ready_label = tkinter.Label(button_frame, text="Press the ready button once you switched places with your oponent", font=("Arial", 12))
    ready_label.grid(row=0, column=3)
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
        boat_button[i] = tkinter.Button(boat_frame, text=boat_types[i] + " (" + str(boat_sizes[i]) + ")", width=10, height=2, command=lambda i=i: select_boat(boat_types[i]))
        boat_button[i].grid(row=0, column=i)

    # creating the chossing buttons for the selected player, basically the game board for the ships of the player
    for i in range(map_size):
        for j in range(map_size):
            buttons[int(current_player)-1][i][j] = tkinter.Button(frame, text=" ", width=10, height=5, command=lambda i=i, j=j: place_boat(i, j))
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
window.resizable(False, False)
window.iconbitmap("boat.ico")

# creating a top label for the game, displaying the current player
main_label = tkinter.Label(window, text="Player " + current_player + "'s turn", font=("Arial", 20))
main_label.pack(side="top")

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
reset_button = tkinter.Button(button_frame, text="Reset",width=9, height=2 ,command=lambda: reset())
reset_button.grid(row=0, column=0)
settings_button = tkinter.Button(button_frame, text="Settings", width=9, height=2, command=lambda: settings())
settings_button.grid(row=0, column=1)


# first faze of the game, the placement of the boats
for i in range(num_of_players):
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
        buttons[int(current_player)-1][i][j] = tkinter.Button(frame, text=" ", width=10, height=5, command=lambda i=i, j=j: button_pressed(i, j))
        buttons[int(current_player)-1][i][j].grid(row=i, column=j)
    window.update()
    if current_player == players[0]:
        current_player = players[1]
    else:
        current_player = players[0]


window.mainloop()
