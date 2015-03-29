from random import randint

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Set Up Board
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
dims = 0
while dims % 2 == 0 or dims < 6:
    dims = int(raw_input("How many tiles long do you want your board (choose an odd number > 5)? "))

board = []
for x in range(dims):
    board.append(["O "] * dims)

# Print the board with unit and shop locations
def spawn_player(player):
    if player.health > 0:
        board[player.x][player.y] = player.mark
    else:
        board[player.x][player.y] = '0 '
        player.x = player.home_x
        player.y = player.home_y
        board[player.x][player.y] = player.mark


def print_board(board, player_count):
    if boss.health > 0:
        board[boss.x][boss.y] = boss.mark
    spawn_player(p1)
    if player_count > 1:
        spawn_player(p2)
    if player_count > 2:
        spawn_player(p3)
    if player_count > 3:
        spawn_player(p4)
    for row in board:
        print " ".join(row)
    print "---"

def print_stats(player_count):
    print "P1 - Level: " + str(p1.lvl) + ", HP/ATK/DEF: " + str(p1.health) + "/" + str(p1.atk) + "/" + str(p1.dfn)
    if player_count > 1:
        print "P2 - Level: " + str(p2.lvl) + ", HP/ATK/DEF: " + str(p2.health) + "/" + str(p2.atk) + "/" + str(p2.dfn)
    if player_count > 2:
        print "P3 - Level: " + str(p3.lvl) + ", HP/ATK/DEF: " + str(p3.health) + "/" + str(p3.atk) + "/" + str(p3.dfn)
    if player_count > 3:
        print "P4 - Level: " + str(p4.lvl) + ", HP/ATK/DEF: " + str(p4.health) + "/" + str(p4.atk) + "/" + str(p4.dfn)
    print "---"


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Auxiliary Functions
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Check if a space is vacant
def movable(player, x, y):
    if player.x + x >= 0 and player.x + x < 9 and player.y + y >= 0 and player.y + y < 9:
        if board[player.x + x][player.y + y] == 'O ':
            return True
        else:
            return False
    else:
        return False

def attackable(player):
    targets = []
    x = player.x
    y = player.y
    if x - 1 >= 0:
        if 'P' in board[x - 1][y]:
            targets.append(board[x-1][y])
    if x + 1 <= dims - 1:
        if 'P' in board[x + 1][y]:
            targets.append(board[x-1][y])
    if y - 1 >= 0 :
        if 'P' in board[x][y - 1]:
            targets.append(board[x-1][y])
    if y + 1 <= dims - 1:
        if 'P' in board[x][y + 1]:
            targets.append(board[x-1][y])
    return targets

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Create the character classes
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class unit(object):
    def __init__(self, row, col, mark, level):
        self.x = row
        self.y = col
        self.mark = mark
        self.health = level
        self.atk = level / 2
        self.dfn = level / 2
    def add_item(self, item):
        self.items.append(item)
    def remove_item(self, item):
        self.items.delete(item)

class hero(unit):
    def __init__(self, row, col, mark, level, health, items, n_items, n_rolls, n_moves, n_battles, n_buys):
        self.x = row                # x position of hero
        self.y = col                # y position of hero
        self.home_x = row           # x starting position
        self.home_y = col           # y starting position
        self.mark = mark            # hero label (P#)
        self.lvl = level            # hero level
        self.health = health        # hero current health
        self.fullhealth = health    # hero max health
        self.atk = level            # hero base attack power
        self.dfn = level            # hero base defense power
        self.items = items          # hero items inventory
        self.n_items = n_items      # number of items
        self.n_rolls = n_rolls      # number of rolls remaining
        self.n_moves = n_moves      # number of spaces able to move
        self.n_battles = n_battles  # number of battles able to commence
        self.n_buys = n_buys        # number of buys able to perform
        self.revenge = ""           # change to player who previous attacked this hero
    def acts_remaining(self):
        return self.n_items + n_moves + n_battles + n_buys
    def move(self, x, y):
        if abs(x) + abs(y) <= self.n_moves and movable(self, x, y):
            board[self.x][self.y]= 'O '
            self.x += x
            self.y += y
            board[self.x][self.y]= self.mark
            self.n_moves -= abs(x + y)
        else:
            print
            print "You can't move there!"
            print
    def attack(self,target):
        print self.mark + " attacked " + target.mark + "!"
        roll1 = randint(1,3)
        print self.mark + " rolls a " + str(roll1)
        roll2 = randint(1,3)
        print target.mark + "The defender rolls a " + str(roll2)
        if self.revenge == target.mark:
            atk = self.atk + roll1 + 1
            print "<< " + self.mark + " has a revenge bonus of +1 ATK! >>"
        else:
            atk = self. atk + roll1
        print "<< " + self.mark + " has an ATK power of " + str(atk) + "! >>"
        dfn = target.dfn + roll2
        print "<< " + target.mark + " has an DEF power of " + str(dfn) + "! >>"
        if atk > dfn:
            print "<< " + target.mark + " took " + str(atk-dfn) + " damage! >>"
        else:
            print "<< " + target.mark + " absorbed all the damage! >>"
        target.health -= (atk - dfn)
        self.revenge = ""
        target.revenge = self.mark


class item(object):
    def __init__(self, cost, level):
        self.cost = cost
        self.level = level


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

boss = unit((dims-1)/2, (dims-1)/2, 'X ', 5)

# Find out how many players there are

player_count = int(raw_input("How many players (1-4)? "))
if player_count > 4:
    print "Only 4 players can play at once!"
if player_count < 1:
    print "At least 1 player must be present."

# Add the appropriate number of players to the game

p1 = hero(0, 0, 'P1', 1, 5, {}, 0, 0, 0, 0, 0)
if player_count > 1:
    p2 = hero(dims-1, dims-1, 'P2', 1, 5, {}, 0, 0, 0, 0, 0)
if player_count > 2:
    p3 = hero(0, dims-1, 'P3', 1, 5, {}, 0, 0, 0, 0, 0)
if player_count > 3:
    p4 = hero(dims-1, 0, 'P4', 1, 5, {}, 0, 0, 0, 0, 0)

# Opening message, display the board

print "Let's Begin the game"
print "---"
print_board(board, player_count)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Remaining actions

def perform_turn(player):
    action = ""
    player.n_rolls = 1

    while action != "end":
        action = raw_input("> Player " + str(player_turn) + ", what action would you like to perform (roll/move/attack/buy/item/end)? ")

        # If there are items or abilities to use, perform an item phase

        # Perform a dice roll
        if action == "roll":
            if player.n_rolls == 0:
                print
                print "<< You've already rolled the dice! It was a " + str(roll) + ". >>"
                print
            else:
                # roll = randint(2,5)
                roll = 100
                print
                print "<< Player " + str(player_turn) + " has rolled a " + str(roll) + ". >>"
                print
                player.n_moves = roll
                player.n_rolls = 0

        # If there is a space to move to perform a movement phase
        if action == "move":
            if player.n_moves == 0:
                if player.n_rolls > 0:
                    print
                    print "<< You must first roll the dice. >>"
                    print
                else:
                    print
                    print "<< You cannot move any further >>"
                    print
            else:
                y = int(raw_input("Horizontal motion (+/- #)? "))
                x = int(raw_input("Vertical motion (+/- #)? "))
                player.move(x, y)
                print
                print_board(board, player_count)

        if action == "attack":
            if len(attackable(player)) > 0:
                tgt_player = raw_input("Who do you wish to attack (P#)? ")
                if tgt_player == 'P1':
                    target = p1
                elif tgt_player == 'P2':
                    target = p2
                elif tgt_player == 'P3':
                    target = p3
                elif tgt_player == 'P4':
                    target = p4
                player.attack(target)
            else:
                print "<< There are no reachable targets! >>"

        # If the unit is on a shop, perform a buy phase

        # If there is a unit to trade with, perform a trade

        # If there is a unit to attack, perform an attack phase

        # No more actions available, pass onto next turn


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""Conduct the turns and update results"""

turn = 0


# Perform a turn if the boss is still alive

while boss.health > 0:
    # Whose turn is it?
    player_turn = turn % player_count + 1

    if player_turn == 1:
        perform_turn(p1)
    elif player_turn == 2:
        perform_turn(p2)
    elif player_turn == 3:
        perform_turn(p3)
    elif player_turn == 4:
        perform_turn(p4)

    if raw_input("Would you like to exit the game ('y' to exit)? ") == 'y':
        boss.health = 0
    else:
        print"---"
        print_board(board, player_count)
        print_stats(player_count)

    turn += 1
    if boss.health < 1:
        print "Player " + str(player_turn) + " has slain the Boss and won the battle!"