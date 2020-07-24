from copy import deepcopy

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

def get_move(board_state):
	valid_selection, move = False, None
	
	while not valid_selection:
		print("Where would you like to move? Please enter a move in the form \"A,B\": ", end="")
		move_input = input()
		try:
			split_input = move_input.split(",")
			x_coord = int(split_input[0])
			y_coord = int(split_input[1])
			if 0 <= x_coord <= 3 and 0 <= y_coord <= 3 and board_state[x_coord][y_coord] == None:
				return x_coord, y_coord
		except:
			pass

def has_winner(curr_state):
	for x in range(3):
		if curr_state[x][0] == curr_state[x][1] == curr_state[x][2] and curr_state[x][0] is not None:
			return True, curr_state[x][0]
	
	for y in range(3):
		if curr_state[0][y] == curr_state[1][y] == curr_state[2][y] and curr_state[0][y] is not None:
			return True, curr_state[0][y]

	if curr_state[0][0] == curr_state[1][1] == curr_state[2][2] and curr_state[x][0] is not None:
		return True, curr_state[0][0]

	if curr_state[2][0] == curr_state[1][1] == curr_state[0][2] and curr_state[x][0] is not None:
		return True, curr_state[0][0]

	return False, None

def full_board(curr_state):
	for x in range(3):
		for y in range(3):
			if curr_state[x][y] == None:
				return False

	return True

def generate_future_moves(board_state, move):
	# Move is X or O
	future_states = []

	for x in range(3):	
		for y in range(3):
			future_state = deepcopy(board_state)

			if future_state[x][y] == None:
				future_state[x][y] = move
				future_states.append((future_state, (x,y)))
				
	return future_states

def calculate_win_prob(future_move, computer_selection):
	num_wins_X = 0
	num_wins_O = 0
	num_ties = 0
	
	numerator = num_wins_X if computer_selection == "X" else num_wins_O
	next_move = "O" if computer_selection == "X" else "X"

	stack = Stack()
	stack.push(future_move)

	while not stack.is_empty():
		curr_state = stack.pop()
		curr_state_has_winner, curr_state_winner = has_winner(curr_state)
		
		if curr_state_has_winner:
			if curr_state_winner == "X":
				num_wins_X += 1
			else:
				num_wins_O += 1

		elif full_board(curr_state):
			num_ties += 1



		future_moves = generate_future_moves(curr_state, next_move)
		next_move = "O" if next_move == "X" else "X"

		for future_move in future_moves:
			stack.push(future_move[0])

	win_prob = float(numerator) / float(num_wins_X + num_ties + num_wins_O)
	return win_prob

def find_best_move(board_state, player_selection):
	computer_selection = "O" if player_selection == "X" else "O"

	future_moves = generate_future_moves(board_state, computer_selection)
	best_move, highest_prob = None, -1
	
	# print("Num possible moves: " + str(len(future_moves)))
	for x in range(len(future_moves)):
		curr_prob = calculate_win_prob(future_moves[x][0], computer_selection)
		curr_move = future_moves[x][1]
		
		# print("Curr Prob: " + str(curr_prob), end="")
		# print(" Curr Move: " + str(curr_move), end="")
		# print("")

		if curr_prob > highest_prob:
			highest_prob = curr_prob
			best_move = future_moves[x][1]

	return best_move

def main():
	game_board = 	[	[None, None, None],
						[None, None, None],
						[None, None, None]
					]
	
	player_selection = start_game()
	computer_selection = "X" if player_selection == "O" else "O"
	turn = 0

	board_has_winner, winner_val = False, None

	while True:
		board_has_winner, winner_val = has_winner(game_board)
		if board_has_winner:
			break

		if turn % 2 == 0:
			x_coord, y_coord = get_move(game_board)
			print("YOUR MOVE:")
			game_board[x_coord][y_coord] = player_selection
		else:
			print("COMPUTER MOVE (Calculating):")
			x_coord, y_coord = find_best_move(game_board, player_selection)
			game_board[x_coord][y_coord] = computer_selection

		turn += 1

		print_board(game_board)
		print("")


	if winner_val == player_selection:
		print("Congratulations! You win.")
	elif winner_val == computer_selection:
		print("Tough one! Computer wins.")
	else:
		print("Fairly matched! It's a tie.")

	print("Thank you for playing. Bye bye!")

if __name__ == '__main__':
	main()