##########################################################################
# File Name: connect4.py                                                 #
# Author: David Miller                                                   #
# Date: 2024-12-25                                                       #
# Description: Connect 4 Game.                                           #
# Version: 3.1 (Release)                                                 #
# Website: https://go.davidmiller.top/connect4                           #
# © 2024 David Miller. All rights reserved.                              #
##########################################################################

# Import sys in order to exit the program
from sys import exit

# Copyright notice
def copyrightNotice():
    print("")
    print("Author: David Miller")
    print("Website: https://go.davidmiller.top/connect4")
    print("Version: 3.1 (Release)")
    print("© 2024 David Miller. All rights reserved.")
    print("")

def game():
    # Create empty lists
    chess = emptyBoard()
    chessHistory = []

    # Player 1 = "X"
    # Player 2 = "O"
    turn = 1
    winner = 0
    choiceInvalid = False
    columnInvalid = False

    # Load the empty board
    UI(chess)

    # winner = -1 = Player quit the game
    # winner = 0 = Nobody wins yet
    # winner = 1 = Player 1 wins
    # winner = 2 = Player 2 wins
    # winner = 3 = Game draw
    while winner == 0:
        gameChoice = prompt(turn)
        # Resolve player's choice
        chess, chessHistory, choiceInvalid, columnInvalid, turn, winner = userChoice(chess, chessHistory, choiceInvalid, columnInvalid, gameChoice, turn, winner)
        # Define row
        row1, row2, row3, row4, row5, row6 = defRow(chess)
        # User interface
        if winner != -1:
            UI(chess)
        # Winning condition
        # 1. Vertical
        winner = winVertical(chess, winner)
        # 2. Horizontal
        winner = winHorizontal(row1, row2, row3, row4, row5, row6, winner)
        # 3. Diagonal
        winner = winDiagonal(chess, winner)

        # Check if the winner is determined
        winner = draw(row1, winner)
        if winner != 0:
            # Show who wins
            if winner == 1:
                print("Player 1 wins!")
            if winner == 2:
                print("Player 2 wins!")
            if winner == 3:
                print("Draw!")
            print("")
            menu()
        if choiceInvalid:
            print("Your choice is invalid. Please try again.")
            choiceInvalid = False
        elif columnInvalid:
            print("This column is full. Please try again.")
            columnInvalid = False

def emptyBoard():
    chess = []
    boardCounter = 6
    while boardCounter >= 0:
        chess.append([" ", " ", " ", " ", " ", " "])
        boardCounter = boardCounter - 1
    return chess

def UI(chess):
    # Print the board
    for rowUICounter in [0, 1, 2, 3, 4, 5]:
        print("+-----+-----+-----+-----+-----+-----+-----+")
        print("|  ", end="")
        for columnUICounter in [0, 1, 2, 3, 4, 5, 6]:
            if chess[columnUICounter][rowUICounter] == " ":
                print(" ", end="")
            else:
                print(chess[columnUICounter][rowUICounter], end="")
            if columnUICounter <= 5:
                print("  |  ", end="")
        print("  |")
    print("+-----+-----+-----+-----+-----+-----+-----+")
    print("|  A  |  B  |  C  |  D  |  E  |  F  |  G  |")
    print("+-----+-----+-----+-----+-----+-----+-----+")
    print("")

def prompt(turn):
    # Switch players
    if turn != 1:
        if turn % 2 == 1:
            gameChoice = input("Player 1, enter a column (A-G), undo (U) or quit (Q): ")
        else:
            gameChoice = input("Player 2, enter a column (A-G), undo (U) or quit (Q): ")
    else:
        if turn % 2 == 1:
            gameChoice = input("Player 1, enter a column (A-G) or quit (Q): ")
        else:
            gameChoice = input("Player 2, enter a column (A-G) or quit (Q): ")
    return gameChoice

def userChoice(chess, chessHistory, choiceInvalid, columnInvalid, gameChoice, turn, winner):
    columnCounter = 5
    # First and second element in the list below is a valid choice
    # Third element in the list below is its corresponding column
    for gameChoices in [["A", "a", chess[0]], ["B", "b", chess[1]], ["C", "c", chess[2]], ["D", "d", chess[3]], ["E", "e", chess[4]], ["F", "f", chess[5]], ["G", "g", chess[6]], ["Q", "q"], ["U", "u"]]:
        # Check which column did the player chose
        if gameChoice == gameChoices[0] or gameChoice == gameChoices[1]:
            # Check if user want to undo
            if gameChoices[0] == "U" or gameChoices[1] == "u":
                if turn >= 2:
                    turn = turn - 1
                    chess = chessHistory[turn - 1]
                else:
                    choiceInvalid = True
            # Check if user want to quit
            elif gameChoices[0] == "Q" or gameChoices[1] == "q":
                if turn % 2 == 1:
                    print("The game is interrupted by player 1")
                else:
                    print("The game is interrupted by player 2")
                winner = -1
            else:
                # "[2]" means column X
                # Check if the chosen column is full
                if gameChoices[2][0] == " ":
                    # Check which is the highest marker in the chosen row
                    while columnCounter >= 0:
                        columnChess = gameChoices[2][columnCounter]
                        if columnChess == " ":
                            # Capture current board to "chessHistory"
                            # The for loop here is because "list.copy" cannot copy nested lists
                            columnsHistory = []
                            for columns in chess:
                                columnHistory = columns.copy()
                                columnsHistory.append(columnHistory)
                            if len(chessHistory) > turn - 1:
                                chessHistory[turn - 1] = columnsHistory
                            else:
                                chessHistory.append(columnsHistory)
                            # Put the marker on the top of the highest marker
                            if turn % 2 == 1:
                                gameChoices[2][columnCounter] = "X"
                            else:
                                gameChoices[2][columnCounter] = "O"
                            turn = turn + 1
                            break
                        else:
                            columnCounter = columnCounter - 1
                else:
                    columnInvalid = True
        # Check if the player made a mistake
        if gameChoice not in "AaBbCcDdEeFfGgQqUu" or gameChoice == "":
            choiceInvalid = True
    return [chess, chessHistory, choiceInvalid, columnInvalid, turn, winner]

def defRow(chess):
    # Convert columns into rows
    row = []
    rows = []
    for rowDefRowCounter in [0, 1, 2, 3, 4, 5]:
        for columnDefRowCounter in [0, 1, 2, 3, 4, 5, 6]:
            row.append(chess[columnDefRowCounter][rowDefRowCounter])
        rows.append(row)
        row = []
    return rows

def winVertical(chess, winner):
    for column in chess:
        for columnWinCounter in [0, 1, 2]:
            if column[columnWinCounter] == column[columnWinCounter + 1] == column[columnWinCounter + 2] == column[columnWinCounter + 3] == "X":
                return 1
            if column[columnWinCounter] == column[columnWinCounter + 1] == column[columnWinCounter + 2] == column[columnWinCounter + 3] == "O":
                return 2
    if winner == 0:
        return 0

def winHorizontal(row1, row2, row3, row4, row5, row6, winner):
    for row in [row1, row2, row3, row4, row5, row6]:
        for rowWinCounter in [0, 1, 2, 3]:
            if row[rowWinCounter] == row[rowWinCounter + 1] == row[rowWinCounter + 2] == row[rowWinCounter + 3] == "X":
                return 1
            if row[rowWinCounter] == row[rowWinCounter + 1] == row[rowWinCounter + 2] == row[rowWinCounter + 3] == "O":
                return 2
    return winner

def winDiagonal(chess, winner):
    diagonalPri1 = [chess[3][0], chess[4][1], chess[5][2], chess[6][3]]
    diagonalPri2 = [chess[2][0], chess[3][1], chess[4][2], chess[5][3], chess[6][4]]
    diagonalPri3 = [chess[1][0], chess[2][1], chess[3][2], chess[4][3], chess[5][4], chess[6][5]]
    diagonalPri4 = [chess[0][0], chess[1][1], chess[2][2], chess[3][3], chess[4][4], chess[5][5]]
    diagonalPri5 = [chess[0][1], chess[1][2], chess[2][3], chess[3][4], chess[4][5]]
    diagonalPri6 = [chess[0][2], chess[1][3], chess[2][4], chess[3][5]]

    diagonalSec1 = [chess[0][3], chess[1][2], chess[2][1], chess[3][0]]
    diagonalSec2 = [chess[0][4], chess[1][3], chess[2][2], chess[3][1], chess[4][0]]
    diagonalSec3 = [chess[0][5], chess[1][4], chess[2][3], chess[3][2], chess[4][1], chess[5][0]]
    diagonalSec4 = [chess[1][5], chess[2][4], chess[3][3], chess[4][2], chess[5][1], chess[6][0]]
    diagonalSec5 = [chess[2][5], chess[3][4], chess[4][3], chess[5][2], chess[6][1]]
    diagonalSec6 = [chess[3][5], chess[4][4], chess[5][3], chess[6][2]]

    diagonals = [diagonalPri1, diagonalPri2, diagonalPri3, diagonalPri4, diagonalPri5, diagonalPri6, diagonalSec1, diagonalSec2, diagonalSec3, diagonalSec4, diagonalSec5, diagonalSec6]
    
    # Use range function to deal with diagonals of varying lengths
    for diagonal in diagonals:
        for diagonalWinCounter in range(len(diagonal) - 3):
            if diagonal[diagonalWinCounter] == diagonal[diagonalWinCounter + 1] == diagonal[diagonalWinCounter + 2] == diagonal[diagonalWinCounter + 3] == "X":
                return 1
            if diagonal[diagonalWinCounter] == diagonal[diagonalWinCounter + 1] == diagonal[diagonalWinCounter + 2] == diagonal[diagonalWinCounter + 3] == "O":
                return 2
    return winner

def draw(row1, winner):
    # This if statement is to check whether a player wins when the board is full
    if winner != 1 and winner != 2:
        drawCounter = 0
        for draw in row1:
            if draw != " ":
                drawCounter = drawCounter + 1
        if drawCounter >= 7:
            return 3
    return winner

def menu():
    # Main menu
    print("Welcome to Connect 4")
    print("  1. New Two-Player Game")
    print("  2. Exit")
    menuChoice = input("Enter your choice: ")
    if menuChoice == "1":
        # Here we go!
        game()
    elif menuChoice == "2":
        # See ya
        copyrightNotice()
        # "0" = exit without any errors
        exit(0)
    elif menuChoice != "1" and menuChoice != "2":
        print ("Your choice is invalid. Please try again.")
        print("")
        menu()
menu()