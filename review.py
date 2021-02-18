import sys
import string
import os
import random
from time import sleep
from copy import deepcopy


BLUE = "\033[0;34;1m"
GREEN = "\033[1;32m"
END = "\033[0m"
SIGN = "0"
SIGN2 = "X"

# function for collecting data from user
def player_input(text):
    player_text = input(text)
    if len(player_text) > 0 and player_text[0].lower() == "q":
        sys.exit("You quit the game")
    return player_text


# function for initializing board used in game
def init_board(size):
    board = []
    for i in range(0,size):
        board.append(["0"]*size)
    return board


# function that prepares content of board for printing
def prepare_board_for_printing(board,color,player):
    column_name_list = [number for number in range(1,len(board)+1)]
    row_name_list = list(string.ascii_uppercase[:len(board)])

    column_name_row =" "*5
    for column in column_name_list:
        column_name_row += f"{column} "

    # name_row = f"{color}{player}{END}"
    center_num = 2*len(board)+8
    name_row = player.center(center_num," ")

    name_row_content = f"{color}{name_row}{END}"

    board_content = {"name_row" : name_row_content }
    board_content["heading_row"] = f"{color}{column_name_row}{END}"
    for i in range(len(board)):
        row_content = f"  {color}{row_name_list[i]}{END}  "
        for j in range(len(board)):
            row_content += f"{board[i][j]} "
        board_content[i] = row_content

    return board_content


#function for printing 1 or 2 boards
def print_two_boards(board,color, player1, player2=None, board2=None,color2=None):  # jako parametr board2 True?
    board1_dict = prepare_board_for_printing(board,color,player1)

    if board2:
        board2_dict = prepare_board_for_printing(board2,color2,player2)
        print(board1_dict["name_row"]," "*(5),board2_dict["name_row"])
        print(" ")
        print(board1_dict["heading_row"]," "*7,board2_dict["heading_row"])
        for i in range(len(board)):
            print(board1_dict[i]," "*7,board2_dict[i])
    else:
        print(board1_dict["name_row"])
        print(" ")
        print(board1_dict["heading_row"])
        for i in range(len(board)):
            print(board1_dict[i])


def get_move(board, player_name, user_input):
    row, col = 100, 100 #these coordinates are for sure outside the board
    count = 0
    #TODO: zabezpiecz się na ujemne cyfry
    # keep asking as long as row, col are invalid
    # TODO: zmienna True/ False zamiast row == 100
    while row == 100 or col == 100:
        if count > 0:
            user_input = player_input(f"\n{player_name} specify coordinates of your move on board: ")

        # user can write only 2 signs - letters and numbers
        if len(user_input) != 2 or not user_input.isalnum():
            print("Invalid input!")
            count += 1
            continue
        else: #i have valid coordinates
            # decode input into coordinates
            for sign in user_input:
                unicode = ord(sign.lower())
                if sign.isalpha():
                    row = unicode - 97
                    continue
                elif sign.isdigit():
                    col = unicode - 49
                    continue
        # check if coordinates are on board
        # TODO: zmień try na if
        try:
            board[row][col]
            return row, col
        except IndexError:
            print("Invalid input!")
            row, col = 100, 100
            count += 1
            continue

def get_placing_move(board,player_name,ship_length=0,direction="",color =""): #TODO usun puste stringi
    row, col = 100, 100 #TODO: wartosc logiczna True/False w while
    while row == 100 or col == 100:

        choosen_direction = f" in {color}{direction}{END} direction"
        if ship_length == 1:
            choosen_direction = ""
        user_input = player_input(f"\nSpecify beginning coordinates for your ship of {color}{ship_length}{END} length{choosen_direction}: ")

        if user_input.lower() == "p":
            return -1,-1
        if user_input.lower() == "d":
            return -2,-2

        row, col = get_move(board, player_name, user_input)

        if  direction == "vertical": #try zamień na if #zmienna is_vertical == True
            try:
                board[row+ship_length-1][col]
                # return row, col
            except IndexError:
                print("Invalid input!")
                row, col = 100, 100
                continue
        if direction == "horizontal": #zmienna is_vertical == False
            try:
                board[row][col+ship_length-1]
                # return row, col
            except IndexError:
                print("Invalid input!")
                row, col = 100, 100
                continue
    return row, col


# function that receives length of ship from user
def get_ship_length(size_list):
    ship_length = 0
    print(f"\nYou have {len(size_list)} ship(s) left to place on the board." )
    if len(size_list)== 1 or all(position == 1 for position in size_list):
        ship_length = size_list[0]
        print(f"Length of the ship is {ship_length}.")
        return ship_length

    while ship_length not in size_list:
        try:
            ship_length = int(player_input(f"\nSpecify the length of your ship \
from {'/'.join(str(x) for x in size_list)}: "))
        except ValueError:
            print("Invalid input!")
            continue
        if ship_length not in size_list:
            print("Invalid input!")

    return ship_length

# function that receives direction of ship from user
def get_direction(ship_length):
    direction =""
    if ship_length == 1:
        direction = "vertical"
    else:
        while direction.lower() not in ["horizontal","h","v","vertical"]:
            direction = player_input(f"\nSpecify direction of your ship (v for vertical, h for horizontal): ")
            if direction.lower().startswith("h"):
                direction = "horizontal"
            elif direction.lower().startswith("v"):
                direction = "vertical"
            else:
                print("Invalid input!")
                continue

    return direction

# function that cleans screen after Player1 placed his ships on board
def clean_screen(player_dict, player1, player2):
    if player_dict['name'] != "AI":
        player_input("\n\nPress any key for cleaning screen ")
        clear_terminal()

        game_text = f"\n{'>'*14}{player_dict['color']} BATTLESHIP {END}{'<'*14}\n"
        game_text1 = f"\n{' '*2}{'>'*10}{player_dict['color']} READY FOR WAR {END}{'<'*10}"
        print()
        print(game_text.center(144," "))
        print()
        print(game_text1.center(144," "))
        print("\n\n\n")
        sleep(0.5)

        if player_dict["name"] == player1 and player2 != 'AI':
            action = input(f"Press any key if {player2} is ready for placing ships ")
        else:
            action = input("Press any key if You are ready for battle! ")

    clear_terminal()



#function for clearing terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# function for placement phase of game
def placing_ships(board,setup_dict, SIGN,color, player_name):
    ships_size = setup_dict["ships_sizes"].copy()  # uzależnić od wersji 5 lub 10 pól
    ships_number = 1
    ships_dict= {}

    while ships_number <= setup_dict["ships_number"]:
        # os.system("clear")
        clear_terminal()
        print_two_boards(board,color,player_name)
        ship_length = get_ship_length(ships_size)
        direction = get_direction(ship_length)

        is_space = False
        while not is_space :
            row,col = get_placing_move(board,True,ship_length,direction,color)
            if row == -1:
                break
            '''do czyszczenia ekranu i ponownego rozlozenia statkow'''
            if row == -2:
                ships_dict.clear()
                return ships_dict

            if is_space_for_ship(board,row,col,ship_length,direction,SIGN):
                ship = mark_ships(board,row,col,direction,ship_length,SIGN2,ships_number)
                ships_dict.update(ship)
                ships_size.remove(ship_length)
                ships_number += 1
                is_space = True
            else:
                print("There should be at least 1 empty field between two ships.Try again.")
                print("Press 'p' to pick another ship, 'd' for discard all ships and start again.")
                print("Enter 'quit' to end the game.")
                continue

    # os.system("clear")
    clear_terminal()
    print_two_boards(board,color,player_name)

    return ships_dict


#function that creates board for checking shots
def init_board_for_shooting(size,ships_dict):
    board_for_shooting = init_board(size)
    for key in ships_dict:
        for (i,j) in ships_dict[key]:
            board_for_shooting[i][j] = key
    return board_for_shooting


# function that creates for each ship in ships_dictionary equivalent in signs X
#and put them to another dictionary, both dictionaries have the same keys
def create_ships_for_shooting(ships_dict):
    ships_for_shooting = {}
    for key in ships_dict:
        ships_for_shooting[key] = [SIGN2 for position in ships_dict[key]]

    return ships_for_shooting


# function that allows players to choose and put ships on board,creates dict of boards and ships for each player
def placement_phase(setup_dict,player_dict, player1, player2):
    ships_player = {}


    while len(ships_player) == 0:
        board_player = init_board(setup_dict["board_sizes"])
        if player_dict['name'] != 'AI':
            ships_player = placing_ships(board_player,setup_dict,SIGN,player_dict["color"], player_dict["name"])
        else:
            ships_player = AI_put_ships(board_player, setup_dict, SIGN, player_dict["color"])

    board_for_shooting = init_board_for_shooting(setup_dict["board_sizes"],ships_player)
    ships_for_shooting = create_ships_for_shooting(ships_player)
    player_dict.update( {"board" : board_player ,\
    "ships": ships_player, "board_for_shooting" : board_for_shooting, \
    "ships_for_shooting" : ships_for_shooting})
    clean_screen(player_dict, player1, player2)

    return player_dict



# function that marks ships on board in placement phase
def mark_ships(board,row,col,direction,length,sign,ships_number):

    ship = {str(ships_number): []}
    if direction  == "vertical":
        for i in range(row, row+length):
            board[i][col] = sign
            ship[str(ships_number)] += [(i,col)]

    if direction == "horizontal":
        for i in range(col,col + length):
            board[row][i] = sign
            ship[str(ships_number)] += [(row,i)]

    return ship



# function that returns if the ship can be placed on board
def is_space_for_ship(board,row,col,length,direction, sign):
    if direction == "vertical":
        space_for_ship = checking_space_vertical(board,row,col,length)
    elif direction == "horizontal":
        space_for_ship = checking_space_vertical(board,row,col,length,True)
    if all(position == sign for position in space_for_ship):
        return True
    else:
        return False



# function that checks sings of positions and neighbour's positions for ship that user wants to mark in vertical direction
def checking_space_vertical(board,row,col,length,is_reversed = False):

    row_start, col_start = specify_edge_start_row_col(board,row,col,length)
    if is_reversed:
        row_end, col_end = specify_edge_end_row_col(board,row,col,length,True)
    else:
        row_end, col_end = specify_edge_end_row_col(board,row,col,length,is_reversed=False)

    neighbours_positions = []

    if is_reversed:
        neighbours_positions += [board[row][i] for i in range(col_start,col_end+1)]
        if row_start != row:
            neighbours_positions += [board[row_start][i] for i in range(col,col+length)]
        if row_end != row:
            neighbours_positions += [board[row_end][i] for i in range(col,col+length)]
    else:
        neighbours_positions += [board[i][col] for i in range(row_start,row_end+1)]
        if col_start != col:
            neighbours_positions += [board[i][col_start] for i in range(row,row+length)]
        if col_end != col:
            neighbours_positions += [board[i][col_end] for i in range(row,row+length)]

    return neighbours_positions

#function that specify start position for checking if is space for ship
def specify_edge_start_row_col(board,row,col,length):
    if row == 0:
        row_start = row
    else:
        row_start = row-1
    if col == 0:
        col_start = col
    else:
        col_start = col-1

    return row_start, col_start

def specify_edge_end_row_col(board,row,col,length,is_reversed=False):
    if is_reversed:
        if col + length-1 == len(board)-1:
            col_end = col + length-1
        else:
            col_end = col + length
        if row == len(board)-1:
            row_end = row
        else:
            row_end = row + 1

    else:
        if row + length-1 == len(board)-1:
                row_end = row + length-1
        else:
            row_end = row + length
        if col == len(board)-1:
            col_end = col
        else:
            col_end = col + 1

    return row_end, col_end



'''AI module - w pętli poniżej'''
# ships_AI = {}
# while len(ships_AI) == 0:
#     board = init_board(6)
#     ships_AI = battleship_AI.AI_put_ships(board,setup_dict,SIGN,player2_dict['color'])

# battleship_AI.print_two_boards(board,player2_dict['color'])


# function that put ships on board and create dictionary of ships
def AI_put_ships(board,setup_dict,SIGN,color):
    directions = ["vertical", "horizontal"]
    ship_sizes_AI = sorted(setup_dict['ships_sizes'],reverse=True)
    ships_number = 1
    ships_dict = {}
    board_coords = [(i,j) for j in range(0,len(board)) for i in range(0,len(board))]

    while ships_number <=setup_dict['ships_number']:
        ship_length = ship_sizes_AI[0]
        direction = random.choice(directions)
        row, col = AI_get_placing_move(board,board_coords,ship_length,direction)

        try_number = 0
        is_space = False
        while not is_space and try_number <26:
            if is_space_for_ship(board,row,col,ship_length,direction,SIGN):
                ship = mark_ships(board,row,col,direction,ship_length,SIGN2,ships_number)
                ships_dict.update(ship)
                ship_sizes_AI.remove(ship_length)
                board_coords.remove((row,col))
                ships_number += 1
                is_space = True

            else:
                try_number += 1
                continue

        if try_number == 26:
            ships_dict.clear()
            board = init_board(len(board))
            break

    return ships_dict

# function that random row,col and check if the ship is in board
def AI_get_placing_move(board,board_coords,ship_length,direction):
    row, col = 100,100
    while row == 100 or col == 100:
        row, col = list(random.choice(board_coords))
        if  direction == "vertical":
            try:
                board[row+ship_length-1][col]
            except IndexError:
                row, col = 100, 100
                continue
        if direction == "horizontal":
            try:
                board[row][col+ship_length-1]
            except IndexError:
                row, col = 100, 100
                continue
    return row, col

''' AI shooting phase '''
def return_occurance(board, sign):
    occurance_on_board = []
    for i in board:
        occurrences = lambda sign, lst: (i for i,e in enumerate(lst) if e == sign)

        row = board.index(i)
        col = list(occurrences(sign,i))
        for i in col:
            occurance_on_board.append([row, i])
    return occurance_on_board


def find_neighbour_cells(board, row, col):
    if row == 0 and col == 0:
        board_neighbours = {
            (row+1, col): board[row+1][col],
            (row, col+1): board[row][col+1]}
    elif row == len(board)-1 and col == len(board)-1:
        board_neighbours = {
            (row-1, col): board[row-1][col],
            (row, col-1): board[row][col-1]}
    elif row == len(board)-1 and col == 0:
        board_neighbours = {
            (row-1, col): board[row-1][col],
            (row, col+1): board[row][col+1]}
    elif row == 0 and col == len(board)-1:
        board_neighbours = {
            (row+1, col): board[row+1][col],
            (row, col-1): board[row][col-1]}
    elif row == 0 and col != (0, len(board)-1):
        board_neighbours = {
            (row+1, col): board[row+1][col],
            (row, col-1): board[row][col-1],
            (row, col+1): board[row][col+1]}
    elif row != (0, len(board)-1) and col == 0:
        board_neighbours = {
            (row-1, col): board[row-1][col],
            (row+1, col): board[row+1][col],
            (row, col+1): board[row][col+1]}
    elif row == len(board)-1 and col != (0,len(board)-1):
        board_neighbours = {
            (row-1, col): board[row-1][col],
            (row, col-1): board[row][col-1],
            (row, col+1): board[row][col+1]}
    elif row != (0,len(board)-1) and col == len(board)-1:
        board_neighbours = {
            (row-1, col): board[row+-1][col],
            (row+1, col): board[row+1][col],
            (row, col-1): board[row][col-1]}
    elif row != (0,len(board)-1) and col != (0,len(board)-1):
        board_neighbours = {
            (row-1, col): board[row-1][col],
            (row+1, col): board[row+1][col],
            (row, col-1): board[row][col-1],
            (row, col+1): board[row][col+1]}
    return board_neighbours

def AI_random_shot(board): #opponent["board_visible"], setup_dict['ships_sizes']
    # TODO znajac jakiej dlugosci sa statki nie szukaj tam, gdzie sie nie zmieszcza

    row, col = 100, 100

    ## H: sprawdz, czy gdzieś jest H
    H_on_board = return_occurance(board,'H')
    if H_on_board != []:
        for i in H_on_board:
            row, col = i[0], i[1]

        # sprawdzam czy po sasiedzku jest juz H - wtedy celuj w lini
            board_neighbours = find_neighbour_cells(board, row, col)
            # print(board_neighbours)
            row_neighbour, col_neighbour = 500,500

            for k, v in board_neighbours.items():
                if v == "H":
                    row_neighbour, col_neighbour = k[0], k[1]
            if row_neighbour == row:
                board_neighbours.pop((row-1, col), None)
                board_neighbours.pop((row+1, col), None)
            elif col_neighbour == col:
                board_neighbours.pop((row, col-1), None)
                board_neighbours.pop((row, col+1), None)
            # print(board_neighbours)

        # celuję w pierwsze sąsiadujące okienko, gdzie nie ma jeszcze strzału (=0)
            # board_neighbours = find_neighbour_cells(board, row, col)

            for k, v in board_neighbours.items():
                if v == "0":
                    row, col = k[0], k[1]
                    return row, col

    ## S: znajdź S-ki na planszy i zwróć listę lokalizacji
    S_on_board = return_occurance(board, 'S') #znajduje S jest na planszy
    S_neighbours = []

    if S_on_board:
        for i in S_on_board:
            for k in find_neighbour_cells(board, i[0], i[1]).keys():
                S_neighbours.append(k)

    # # Randomowy strzał w niezajęte pole
    row,col = 100, 100
    while row == 100 or col == 100:
        row, col = random.randint(0, len(board)-1), random.randint(0, len(board)-1)

        if board[row][col] in ["M", "H", "S"]:
            row, col = 100, 100
            continue
        elif (row, col) in S_neighbours:
            row,col = 100, 100
            continue
        return row, col



''' playing stage '''

# function check if a ship is sunk and return modified list of ships
def check_sunk(ship):
    if all(e == 'H' for e in ship):
        return True


# function marks a sunk ship with "S"
def mark_sunk_ship(row,col,lista,board_visible):
    for (i,j) in lista:
        board_visible[i][j] = "S"

    return board_visible

# function colors hit or sunk ships
def color_board_visible(board_visible,color):
    colored_board_visible = deepcopy(board_visible)
    for i in range(len(board_visible)):
        for j in range(len(board_visible)):
            if board_visible[i][j] == "H" or board_visible[i][j] == "S":
                colored_board_visible[i][j] = f"{color}{board_visible[i][j]}{END}"

    return colored_board_visible


# function checks if I hit a ship and updates boards
def check_hitting(shot,row,col,board_for_shooting,ships_dict,ships_for_shooting):
    #shot = ['X', 'X']
    # check if I hit the sea
    result = []
    if shot == "0":
        shot = 'M'
        sign_for_visible_board = "M"
        result.append(sign_for_visible_board)
    #  now I'm sure I hit a ship
    else:
        for key in ships_dict:
            if (row,col) in ships_dict[key]:
                el = 0
                for e in ships_for_shooting[key]:
                    if e == 'X':
                        break
                    el += 1
                ships_for_shooting[key][el] = 'H'
                sign_for_visible_board = 'H'
                ship_key = key

                result += [sign_for_visible_board,ship_key]
    return result

def has_won(ships_for_shooting):
    winning_list = []
    for ship in ships_for_shooting:
        for part in ships_for_shooting[ship]:
            winning_list.append(part)
    if all(part == "S" for part in winning_list):
        return True


def battleship_game(board, board_visible,board_for_shooting, ships_dict,ships_for_shooting, player_name,color):

    if player_name != "AI":
        user_input = player_input(f"\n{player_name} specify coordinates of your move on board: ")
        row, col = get_move(board, player_name, user_input) #dostaje input z wspolrzednymi
    else:
        row, col = AI_random_shot(board_visible)

    shot = board[row][col]

    # jesli strzal znowu w to samo miejsce, to kolejny ruch
    if board_visible[row][col] != "0":
        print("\nYou've already shot here...\n")
        return False

    result = check_hitting(shot,row,col,board_for_shooting,ships_dict,ships_for_shooting)
    board_visible[row][col] = result[0]
    if len(result)>1:
        ship_key = result[1]

    # board_visible[row][col] = check_hitting(shot,row,col,board_for_shooting,ships_dict,ships_for_shooting)
    if board_visible[row][col] == 'M': #pudlo
            print(f"\n{player_name} has missed!\n")
            return False

    elif board_visible[row][col] == 'H': #trafiony
        if check_sunk(ships_for_shooting[ship_key]): #zatopiony
            ships_for_shooting[ship_key] = ["S" for e in ships_for_shooting[ship_key]]
            board_visible = mark_sunk_ship(row,col,ships_dict[ship_key],board_visible)
            print(f"\n{player_name} has sunk a ship!\n")
            return True

        else:
            print(f"\n{player_name} has hit a ship!\n")
            return False


    # os.system("cls")

# function allows user to change default board size, to implement in main_menu
def set_user_board_size(setup_dictionaries):
    user_board = ""
    while user_board not in range(5, 11):
        try :
            user_board = int(player_input("\nDefault board side is 5. Write any number from 5 to 10 to set a new value: "))
        except ValueError:
            print("Invalid input!")
            continue
    return setup_dictionaries[user_board -5] #setup_dict =

def main_menu():
    # global variables
    setup_dict_5 = {"ships_number" : 2, "ships_sizes": [3,4], "board_sizes" : 5}
    setup_dict_6 = {"ships_number" : 2, "ships_sizes": [3,5], "board_sizes" : 6}
    setup_dict_7 = {"ships_number" : 3, "ships_sizes": [3,4,5], "board_sizes" : 7}
    setup_dict_8 = {"ships_number" : 3, "ships_sizes": [4,4,5], "board_sizes" : 8}
    setup_dict_9 = {"ships_number" : 4, "ships_sizes": [2,4,4,5], "board_sizes" : 9}
    setup_dict_10 = {"ships_number" : 4, "ships_sizes": [3,4,5,5], "board_sizes" : 10}
    setup_dictionaries = [setup_dict_5, setup_dict_6, setup_dict_7, setup_dict_8, setup_dict_9, setup_dict_10]
    setup_dict = setup_dict_5

    player1_dict = {"name" : "Player1", "color" : BLUE} #dodawane będzie do słownika: board, board_visible, board_for_shooting, ships_for_shooting, ships_dict
    player2_dict = {"name" : "Player2", "color" : GREEN}
    players = [player1_dict, player2_dict]


    ''' welcome! '''
    clear_terminal()
    print()
    print(f"\n{'>'*14}{BLUE} HELLO! LET'S PLAY THE BATTLESHIP GAME! {END}{'<'*14}\n")
    sleep(1)
    print("\nFollow the instructions to play. Anytime you want to quit, press 'Q'.\n")
    sleep(2)

    #AI gamemode
    gamemode = ""
    while gamemode == "":
        user_input = player_input("\nLet's choose a gamemode first.\nPress: 1. Single player or 2. Multiplayer: ")
        if user_input == '1':
            gamemode = "AI"
            player2_dict['name'] = "AI"
        elif user_input == '2':
            gamemode = "HUMAN"
        else:
            print("Invalid input!")
            continue

    # board size update
    user_input = player_input("\nPress 'S' to change default board size or any other key to play.")
    if user_input.lower() == 's':
        setup_dict = set_user_board_size(setup_dictionaries)
        sleep(0.5)
        # os.system("clear")
        clear_terminal()

    # players names
    for player in players:
        if player['name'] == "AI":
            pass
        else:
            player["name"] = player_input(f"\n{player1_dict['color']}{player['name']}{END}, please write your name: ")
    sleep(1)

    player1 = players[0]["name"]
    player2 = players[1]["name"]




    ''' placement phase'''
    print(f"\n{player1_dict['color']}{player1}{END}, it's time to place yous ships on board.\n")
    sleep(2)
    # os.system("clear")
    clear_terminal()
    count = 0
    for player in [player1_dict, player2_dict]:
            player = placement_phase(setup_dict, players[count], player1, player2)
            players[count]["board_visible"] = init_board(setup_dict["board_sizes"])
            players[count]["colored_board_visible"] = color_board_visible(players[count]["board_visible"],players[count]["color"])
            count += 1

    # print(player2_dict)


    ''' shooting phase'''
    player = players[0]
    opponent = players[1]

    while not has_won(player["ships_for_shooting"]) and not has_won(opponent["ships_for_shooting"]):
        print_two_boards(players[0]["colored_board_visible"], players[0]["color"],player1, player2, players[1]["colored_board_visible"], players[1]["color"])
        print("\nM: missed\tH: hit\t\tS - sunk")
        battleship_game(opponent["board"], opponent["board_visible"], opponent["board_for_shooting"], opponent["ships"], opponent["ships_for_shooting"], player["name"], player["color"])
        opponent["colored_board_visible"] = color_board_visible(opponent["board_visible"],opponent["color"])
        player, opponent = opponent, player
        sleep(1)
        clear_terminal()
        continue

    print_two_boards(players[0]["colored_board_visible"], players[0]["color"],player1, player2, players[1]["colored_board_visible"], players[1]["color"])
    print("\nM: missed\tH: hit\t\tS: sunk")

    print(f"\n\n! ! ! {opponent['color']}{opponent['name']} wins{END} ! ! !")
    user_input = player_input("\n\n\nPress 'y' to play again ")
    if user_input.lower() == "y":
        clear_terminal()
        main_menu()
    else:
        print("Thank you for the game.")


if __name__ == "__main__":
    main_menu()
