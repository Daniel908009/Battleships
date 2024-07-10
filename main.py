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
    global number_of_players_boats
    for i in range(num_of_players):
        if number_of_players_boats[i] == 0:
            return True

# function that is called when a button is pressed, basically it handles the guess of a player
def button_pressed(x, y):
    global number_of_players_boats, current_player
    if [x, y] in possitions_of_boats[int(current_player)-1]:
        number_of_players_boats[int(current_player)-1] -= 1
        print("Hit")
    else:
        print("Miss")
    if check_win():
        print("Player " + current_player + " has won")
    else:
        if current_player == players[0]:
            current_player = players[1]
        else:
            current_player = players[0]
        main_label.config(text="Player " + current_player + "'s turn")
        window.update()

# function to select a boat type from the boat selection
def select_boat(boat_type):
    #global boat_button
    boat_selected = boat_type
    # making the selected boat button stay pressed
    #print(boat_button)
    print(boat_selected)
    #boat_button[i].config(relief="sunken")
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


    

# function that will continuously check mouse coordinates, this will be used to place the boats on the game board
def check_mouse_coordinates():
    while running:
        x, y = window.winfo_pointerxy()
        print(x, y)
        time.sleep(2)
    return None

# function to place the boats on the game board
def place_boat(x, y):
    global boats_placed, current_player, boat_sizes, number_of_tiles_selected, buttons
    is_empty = True
    # finding the size of the selected boat, this will be used to check if the entire boat has been placed
    for i in range(len(boat_types)):
        if boat_button[i].config("relief")[-1] == "sunken":
            boat_size = boat_sizes[i]
    print(boat_size)
    while number_of_tiles_selected != boat_size:
        print(boat_size, number_of_tiles_selected)
        # checking if the boat is already placed on the selected tile
        for i in range(len(possitions_of_boats[int(current_player)-1])):
            if possitions_of_boats[int(current_player)-1][i] == [x, y]:
                is_empty = False
        if is_empty == False:
            print("Boat already placed here")
            is_empty = True
        #possitions_of_boats[int(current_player)-1].append([x, y])
        else:
            number_of_tiles_selected += 1
            possitions_of_boats[int(current_player)-1].append([x, y])
            if number_of_tiles_selected == boat_size:
                boats_placed += 1
                #number_of_tiles_selected = 0
                # dissabling the boat select button and changing the relief of the selected button and making it red
                for i in range(len(boat_types)):
                    if boat_button[i].config("relief")[-1] == "sunken":
                        boat_button[i].config(relief="raised")
                        boat_button[i].config(state="disabled")
                        boat_button[i].config(bg="red")
                print("Boat placed")
                break
            #print(number_of_tiles_selected)
        print(possitions_of_boats)
        window.update()
        time.sleep(1)
    number_of_tiles_selected = 0

# function for a checking thread
#def check_thread():
    #pass

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
                #boat_button.clear()
            else:
                current_player = players[0]
                temp = False
                #boat_button.clear()
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
boat_sizes = [5, 4, 3, 3, 2]
players = ["1", "2"]
current_player = random.choice(players)
possitions_of_boats = []
number_of_players_boats = [[number_of_boats],[number_of_boats]]
for i in range(num_of_players):
    possitions_of_boats.append([])
buttons = []
for i in range(num_of_players):
    buttons.append([])
    for j in range(map_size):
        buttons[i].append([])
        for k in range(map_size):
            buttons[i][j].append([])

# creating a thread for the mouse coordinates checking
mouse_thread = threading.Thread(target=check_mouse_coordinates)

# creating the main window of the game
window = tkinter.Tk()
window.title("Battleships")
window.geometry("800x600")
window.resizable(False, False)
window.iconbitmap("boat.ico")

# starting the mouse thread
#mouse_thread.start()

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

# second faze of the game, the actual game(guessing the possition of the ships)
#while True:
 #   for i in range(map_size):
  #      for j in range(map_size):
   #         buttons[int(current_player)-1][i][j] = tkinter.Button(frame, text=" ", width=10, height=5, command=lambda i=i, j=j: button_pressed(i, j))
    #        buttons[int(current_player)-1][i][j].grid(row=i, column=j)
   # if check_win():
    #    break
    #else:
    #    pass
    #try:
    #    main_label.config(text="Player " + current_player + "'s turn")
    #except:
    #    pass
    #window.update()



#mouse_thread.join()
window.mainloop()
