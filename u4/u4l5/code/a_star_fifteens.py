class Queue:
	def __init__(self):
		self.q = []
	def enqueue(self, val):
		self.q.append(val)
	def dequeue(self):
		if self.size() == 0:
			return None
		else:
			return self.q.pop(0)	
	def peek(self):
		if self.size() == 0:
			return None
		return self	
	def size(self):
		return len(self.q)

class FifteensNode:
	def __init__(self, board_state):
		self.board_state = board_state

	def generate_future_state(self, visited_states):
		# Find where the free space currently is
		free_space_index = -1
		for x in range(len(self.board_state)):
			if self.board_state[x] == -1:
				free_space_index = x
				break

		# Conver the free space to the appropriate row and column
		row, col = int(free_space_index/4), free_space_index%4
		future_boards = []

		location_map = {(0,0):0,  (0,1): 1,  (0,2): 2,  (0,3): 3,
				  		(1,0):4,  (1,1): 5,  (1,2): 6,  (1,3): 7,
				  		(2,0):8,  (2,1): 9,  (2,2): 10, (2,3): 11,
				  		(3,0):12, (3,1): 13, (3,2): 14, (3,3): 15}

		# This takes a two dimensional coordinate like (1,2)
		# It switches the value in (1,2) with the free space
		# It updates the value of the free space acoordingly
		def create_new_board(board_loc):
			switch_index = location_map[board_loc]
			new_board_state = self.board_state.copy()
			
			switch_val = new_board_state[switch_index]
			new_board_state[switch_index] = -1
			new_board_state[free_space_index] = switch_val
			
			hash_val = "".join(str(x) for x in new_board_state)
			if hash_val not in visited_states:
				return new_board_state
			else:
				return None

		# The free space moves are up, down, left, and right
		free_space_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
		for move in free_space_moves:
			row, col = move
	  		# Ensure that the move is a valid move
			if row < 0 or row > 3 or col < 0 or col > 3:
				continue
			else:
				board_val = create_new_board(move)
				if board_val is not None:
					future_boards.append(board_val)
		return future_boards

	def evaluate_heuristic(self):
		location_map = {0: (0,0),  1: (0,1),  2: (0,2),  3: (0,3),
					  	4: (1,0),  5: (1,1),  6: (1,2),  7: (1,3),
					  	8: (2,0),  9: (2,1),  10: (2,2), 11: (2,3),
					  	12: (3,0), 13: (3,1), 14: (3,2), -1: (3,3)} # Define a location map

		manhattan_dist = 0
		for x in range(len(self.board_state)):
			correct_row = int(x/4) # Division and rounding gives us the row
			correct_col = x%4	# Modulus operator gives us the column

			curr_val = self.board_state[x]
			curr_row, curr_col = location_map[curr_val] # Get the current location of the tile

			curr_dist = abs(curr_row - correct_row) + abs(curr_col - correct_col)
			manhattan_dist += curr_dist

		return manhattan_dist

	def hash(self):
		return "".join(str(x) for x in self.board_state)

  	# Simple method to print out the board in a clean
	def pretty_print(self):
		top = "-------" * 6
		print(top)
		for x in range(4):
			print("| ", end="")
			index = 4*x
			for y in range(4):
				print("\t" + str(self.board_state[index]), end="")
				index += 1
			print("\t|")
		print(top)

def a_star(initial_state, goal_state):
	queue = Queue() 
	visited_states = set()
	visited_states.add(initial_state.hash())
	path = [initial_state]
	queue.enqueue(initial_state)

	while queue.size() > 0:
		curr_state = queue.dequeue()
		future_states = curr_state.generate_future_state(visited_states)
		min_hueristic_val, min_state = float('inf'), None

		for future_state in future_states:
			future_state = FifteensNode(future_state)
			hueristic_val = future_state.evaluate_heuristic()
			if hueristic_val < min_hueristic_val:
				min_hueristic_val, min_state = hueristic_val, future_state

		next_state = FifteensNode(min_state.board_state)
		path.append(next_state)
		queue.enqueue(next_state)
		visited_states.add(next_state.hash())

		if min_hueristic_val == 0:
			return path

def main():
	board_state = [x for x in range(16)]
	board_state[3] = -1
	board_state[15] = 3
	initial_state = FifteensNode(board_state)
	initial_state.pretty_print()

	goal_board = [x for x in range(16)]
	goal_board[15] = -1
	goal_state = FifteensNode(goal_board)

	path = a_star(initial_state, goal_state)
	print(len(path))
	for path_elt in path:
		print(path_elt.board_state)



if __name__ == '__main__':
	main()
