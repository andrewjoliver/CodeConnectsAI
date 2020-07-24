from copy import deepcopy


# Basic Stack class as implemented in U2L3 - DFS
class Stack:
	def __init__(self):
		self.stack = []
	
	def push(self, e):
		self.stack.append(e)
	
	def pop(self):
		if self.is_empty():
			return None
		return self.stack.pop()
	
	def peek(self):
		if self.is_empty():
			return None
		return self.stack[-1]

	def is_empty(self):
		return len(self.stack) == 0


# Given a Tic-Tac-Toe board, this method prints out the board in a well-formatted well
def print_board(board_state):
	dashes = "---" * 6
	
	print(dashes)
	for x in range(3):
		print("|", end="")
		for y in range(3):
			board_elt = " " if board_state[x][y] == None else board_state[x][y] 
			board_elt += " \t" if y != 2 else ""
			print(board_elt, end="")
		print("| ")
	print(dashes)


# This method prints out the diagram below, which helps player input their move choices correctly
# This is because players will have to type "1,1" if they'd like to place an X or an O
# in the center of the board. 
# Diagram:
# -------------------------
# | 0,0      0,1      0,2 | 
# | 1,0      1,1      1,2 | 
# | 2,0      2,1      2,2 | 
# -------------------------
def print_board_vals():
	dashes = "-----" * 5
	
	print(dashes)
	for x in range(3):
		print("|", end="")
		for y in range(3):
			board_elt = " " + str(x) + "," + str(y)
			board_elt += "     " if y != 2 else " "
			print(board_elt, end="")
		print("| ")
	print(dashes)


# This code starts the game by asking a player to choice if they'd like to be Xs or Os.
# It then returns this choice to be used later throughout the game.
def start_game():
	print("Welcome to Tic-Tac-Toe!")
	print("You'll play by entering the value where you'd like to make your move.")
	print("These values are below.\n")
	print_board_vals()
	print("")

	valid_selection, move = False, None
	
	while not valid_selection:
		print("Would you like to be Xs or Os? Enter X or O: ", end="")
		move_input = input()
		if move_input == "X" or move_input == "O":
			valid_selection, move = True, move_input


	print("\nGot it! You'll be " + str(move) + "s. Let the game begin!")
	
	return move


# This function prompts a player for their move choices and verifies this choice is a valid
# position on the board. For example 2,1 is accepted by 3,1 is not. This is because there is
# no 3rd row. This method continually prompts the user until a valid selection is made.
# It returns the move the player has accepted as a tuple. The first element of this tuple
# is the row and the second element is the column. So, if the user inputs 2,2, this function
# would return the tuple (2,2)
def get_move(board_state):

	# The while loop below will continue to run until the player has inputted a valid move.
	while True:
		# The print state and input() function allow the user to enter any text
		print("Where would you like to move? Please enter a move in the form \"A,B\": ", end="")
		move_input = input()
		
		# This is a try/catch block. If there are any errors thrown, they will be caught.
		# After they are caught, the while loop will continue until the user inputs a valid move.
		try:
			# The code below splits the input on the comma and coverts each input to an integer
			split_input = move_input.split(",")
			row = int(split_input[0])
			col = int(split_input[1])
			# This ensures the row,col are in bounds and that the board is currently empty at that location
			if 0 <= row <= 3 and 0 <= col <= 3 and board_state[row][col] == None:
				return row, col
		except:
			# Pass is a keyword that does nothing and lets the code continue to run
			pass


# The function below takes the current state of a given board as an input parameter.
# It returns a tuple. The first element is True/False, and this represents if the board
# has a winner in its current state. The second element in the tuple represents the current
# winner, so it will be a string "X" or "O".
def has_winner(curr_state):
	# Each if condition below follows a similar pattern.
	# It checks that all that elements match and then it checks that the first element in not None.
	# Note that if the first element is not None and all the elements in the row match, all elements must be not None
	# If this condition is met, there is a winner - so we return True.
	# The winner will be the element in the row we just checked, so we return this element by indexing our array

	# The code below checks every row in the current board
	for x in range(3):
		if curr_state[x][0] == curr_state[x][1] == curr_state[x][2] and curr_state[x][0] is not None:
			return True, curr_state[x][0]
	
	# The code below checks every column in the current board
	for y in range(3):
		if curr_state[0][y] == curr_state[1][y] == curr_state[2][y] and curr_state[0][y] is not None:
			return True, curr_state[0][y]

	# The code below checks the asacending diagonal along (0,0), (1,1), and (2,2)
	if curr_state[0][0] == curr_state[1][1] == curr_state[2][2] and curr_state[x][0] is not None:
		return True, curr_state[0][0]

	# The code below checks the descending diagonal
	if curr_state[2][0] == curr_state[1][1] == curr_state[0][2] and curr_state[x][0] is not None:
		return True, curr_state[2][0]

	# If all of the above conditions fail, we will reach the code below.
	# At this point, the board has no winner so we return False.
	# Since there is no winner, we simply return None to represent the winner
	return False, None


# This function takes the current state of a board as an input.
# It returns True if the board is full. However, if at least one element is None, the board is not full
# and the function returns False,
def full_board(curr_state):
	# We can simply iterate over the entire board
	# If we find one element that is None, we know we do not have a full board
	for x in range(3):
		for y in range(3):
			if curr_state[x][y] == None:
				return False

	# Here we have determined every element in our board is not None
	# Thus we have a full board so we can return True
	return True


# This function takes the current state of a board as an input.
# It also takes an input move, which is a string that has value either X or O.
# This value determines if an X or an O is being placed on the board.
# It returns an array of tuples. The first element in each tuple is a future board state that can be reached 
# in one move. The second element in the tuple is the location where we placed the most recent X or O.
def generate_future_moves(board_state, move):
	# Initialize an empty array to hold all future boards
	future_states = []

	# We can iterate over each element in our board. If it is empty, we fill it with the move input
	# and add it to the future_states array, along with the corresponding coordinates where the
	# move input was placed
	for x in range(3):	
		for y in range(3):
			future_state = deepcopy(board_state)

			if future_state[x][y] == None:
				future_state[x][y] = move
				future_states.append((future_state, (x,y)))
				
	return future_states


# The input future_move is a current state of a Tic-Tac-Toe board. The computer_selection parameter defines which piece (i.e. X or O)
# the computer is playing. # Given this board state, the method below generates all possible future boards. This generation stops when
# a board is full or when there is a winner on the board. At this point, this method records if X won the game, if O won the game, or
# if there was a tie. It then calculates the percentage of wins for the computer's selected piece over the total numeber of games that
# were generated. It then returns this value as a float.
def calculate_win_prob(future_move, computer_selection):
	# Set up variables to keep track of wins
	num_wins_X = 0
	num_wins_O = 0
	num_ties = 0
	
	# Since the computer has just played, the next move will be played by the player's piece.
	# The code below records keeps track of the next_move variable
	next_move = None
	if computer_selection == "X":
		next_move = "O"
	else:
		next_move = "X"

	# The code below expands on DFS but the structure is largely the same

	# Create a stack and push on the initial state
	stack = Stack()
	stack.push(future_move)

	while not stack.is_empty():

		# Remove the current element from our stack
		curr_state = stack.pop()

		# Check if this state has a winner, and if it does, check who is the winner
		# Remember the has_winner() method returns a tuple
		curr_state_has_winner, curr_state_winner = has_winner(curr_state)
		
		# If there was a winner, then either X or O must have won the game
		# Record this by increment the relevant variable by 1
		if curr_state_has_winner:
			if curr_state_winner == "X":
				num_wins_X += 1
			else:
				num_wins_O += 1
			# We don't need to generate any future states since the game ends
			# The continue keyword brings us back to the while loop
			continue

		# At this point, the board has no winner
		# However, if the board is full then it must be a tie
		# Increment the tie variable by 1
		elif full_board(curr_state):
			num_ties += 1
			# Since the board is full, we don't need to generate any future states
			# See above note on continue keyword
			continue


		# At this point, there is no winner and the board is not full, so we can continue
		# to generate future states, which we do by calling the function below.
		# We have defined next_move appropriately so we simply call the method below
		future_moves = generate_future_moves(curr_state, next_move)

		# Add all future game boards to our stack
		for future_move in future_moves:
			stack.push(future_move[0])

		# We'll need to update the next_move value since it is time for the other person to play
		# This code is "ternary operator" - it is shorthand that does the exact same thing as lines
		# 211-214
		next_move = "O" if next_move == "X" else "X"

	# If the computer is playing X then the numerator of our percentage will be num_wins_x
	# Otherwise the computer is playing O and the numerator should be num_wins_O
	numerator = None
	if computer_selection == "X":
		numerator = num_wins_X
	else:
		numerator = num_wins_O

	# Once DFS terminates, we have simulated all future games and can simply return
	# the ratio as described above
	win_prob = float(numerator) / float(num_wins_X + num_ties + num_wins_O)
	return win_prob


# This method takes the current state of a Tic-Tac-Toe board as an input board_state
# It also takes in the player's selection (i.e. X or O)
# It generates all future moves, calculates the win probabilities for each of these future moves
# It returns the move with the highest win probability
def find_best_move(board_state, player_selection):
	# The computers selection will be the opposite of the players selection
	computer_selection = "O" if player_selection == "X" else "O"

	# Generate all possible future moves
	future_moves = generate_future_moves(board_state, computer_selection)
	# Maintain a variable to record the best move and the highest probability
	# We set the initial highest_prob to -1, so that it will be replaced by any positive probability (even 0)
	# The best_move will be a tuple represent a row and column
	best_move, highest_prob = None, -1
	
	# Iterate over each future_move, calculate the win probability
	# If this probability is better than the current highest_prob,
	# update best_move and highest_prob accordingly
	for x in range(len(future_moves)):
		curr_prob = calculate_win_prob(future_moves[x][0], computer_selection)
		curr_move = future_moves[x][1]
		if curr_prob > highest_prob:
			highest_prob = curr_prob
			best_move = future_moves[x][1]

	# After we have iterated over all possible future states, we simply return the
	# best move to make
	return best_move


def main():
	# This code sets up an initial game board.
	game_board = 	[	[None, None, None],
						[None, None, None],
						[None, None, None]
					]
	
	# This starts the game by asking users to select X or O
	player_selection = start_game()

	# This code assigns computer whichever value was not chosen by the user
	# Note that the function start_game() ensures the user picks between X or O
	# so these are the only two options.
	if player_selection == "O":
		computer_selection = "X"
	else:
		computer_selection = "O"


	# Turn will increase by 1 each time
	# The player play's first and will thus play when turn is even
	# The computer will play when turn is odd
	turn = 0

	# Create variables to record if anyone has won
	board_has_winner, winner_val = False, None

	while True:
		# Iterate until the board has a winner
		# When a winnner exists, we will break out of this while loop
		board_has_winner, winner_val = has_winner(game_board)
		if board_has_winner or full_board(game_board):
			break

		# If turn is even, the player plays
		if turn % 2 == 0:
			# Ask the player what move they would like to make
			row, col = get_move(game_board)
			print("YOUR MOVE:")
			# Update the board
			game_board[row][col] = player_selection
		
		# If turn is odd, the computer playes
		else:
			print("COMPUTER MOVE (Calculating):")
			# Find the best avaialable move
			row, col = find_best_move(game_board, player_selection)
			# Make this move
			game_board[row][col] = computer_selection

		# Increment the turn variable to switch turns
		turn += 1

		# Output the updated board and a blank line (just for readability)
		print_board(game_board)
		print("")



	# Once our while loop terminates, we know there is a winner or a full board
	# See who won (if anyone), and output this result
	# Otherwise, if there was a tie, output this
	if winner_val == player_selection:
		print("Congratulations! You win.")
	elif winner_val == computer_selection:
		print("Tough one! Computer wins.")
	else:
		print("Fairly matched! It's a tie.")

	# Thank the player for playing and end the game
	print("Thank you for playing. Bye bye!")


if __name__ == '__main__':
	main()