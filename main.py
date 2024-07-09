# necessary imports
import tkinter
import random
import time
import threading

# function to reset the game
def reset():
    pass

# function to open the settings window
def settings():
    pass

# function to check if someone has won
def check_win():
    pass

# function that is called when a button is pressed, basically the main game logic loop
def button_pressed(x, y):
    pass

# function to select a boat type from the boat selection
def select_boat(boat_type):
    boat_selected = boat_type

# function that will continuously check mouse coordinates, this will be used to place the boats on the game board
def check_mouse_coordinates():
    while running:
        x, y = window.winfo_pointerxy()
        print(x, y)
        time.sleep(2)
    return None

# function to place the boats on the game board
def place_boat(x, y):
    global boats_placed
    boats_placed += 1

# function for a checking thread
def check_thread():
    pass

# function for the placement of the boats faze
def choose_faze():
    global current_player, boats_placed
    #thread1 = threading.Thread(target=check_thread)
    #if thread1.is_alive() == False:
     #   thread1.start()
    # filling the boat selection frame with buttons representing the boats
    for i in range(number_of_boats):
        boat_button = tkinter.Button(boat_frame, text=boat_types[i] + " (" + str(boat_sizes[i]) + ")", width=10, height=2, command=lambda i=i: select_boat(boat_types[i]))
        boat_button.grid(row=0, column=i)

    # creating the chossing buttons for the selected player, basically the game board for the ships of the player
    for i in range(map_size):
        for j in range(map_size):
            buttons[int(current_player)-1][i][j] = tkinter.Button(frame, text=" ", width=10, height=5, command=lambda i=i, j=j: place_boat(i, j))
            buttons[int(current_player)-1][i][j].grid(row=i, column=j)
    while running:
        if boats_placed == len(boat_types):
            boats_placed = 0
            if current_player == players[0]:
                current_player = players[1]
            else:
                current_player = players[0]
            main_label.config(text="Player " + current_player + "'s turn")
            print("function ended")
        else:
            pass
        print("function ended with a problem")


# variables for the map, players, buttons, etc.
running = True
map_size = 5
number_of_tiles = map_size * map_size
num_of_players = 2
number_of_boats = 5
boats_placed = 0
boat_types = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
boat_sizes = [5, 4, 3, 3, 2]
players = ["1", "2"]
current_player = random.choice(players)
buttons = []
for i in range(num_of_players):
    buttons.append([])
    for j in range(map_size):
        buttons[i].append([])
        for k in range(map_size):
            buttons[i][j].append([])
#print(buttons)
#print(len(buttons))
#print(len(buttons[0]))
#print(len(buttons[1]))
#print(len(buttons[0][0]))
#print(len(buttons[1][0]))

# creating a thread for the mouse coordinates checking
mouse_thread = threading.Thread(target=check_mouse_coordinates)
chose_thread = threading.Thread(target=choose_faze)

# creating the main window of the game
window = tkinter.Tk()
window.title("Battleships")
window.geometry("800x600")
window.resizable(False, False)
#window.iconbitmap("battleship.ico")

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


for i in range(num_of_players):
    chose_thread.start()
    chose_thread.join()
    print("thread ended")
# filling the boat selection frame with buttons representing the boats
#for i in range(number_of_boats):
 #   boat_button = tkinter.Button(boat_frame, text=boat_types[i] + " (" + str(boat_sizes[i]) + ")", width=10, height=2, command=lambda i=i: select_boat(boat_types[i]))
  #  boat_button.grid(row=0, column=i)

# creating the chossing buttons for the selected player, basically the game board for the ships of the player
#for i in range(map_size):
 #   for j in range(map_size):
  #      buttons[int(current_player)-1][i][j] = tkinter.Button(frame, text=" ", width=10, height=5, command=lambda i=i, j=j: button_pressed(i, j))
   #     buttons[int(current_player)-1][i][j].grid(row=i, column=j)


# creating the reset button and settings button
reset_button = tkinter.Button(button_frame, text="Reset",width=9, height=2 ,command=lambda: reset())
reset_button.grid(row=0, column=0)
settings_button = tkinter.Button(button_frame, text="Settings", width=9, height=2, command=lambda: settings())
settings_button.grid(row=0, column=1)




#mouse_thread.join()
window.mainloop()
