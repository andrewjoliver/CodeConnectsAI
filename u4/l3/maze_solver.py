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

class Path:
	def __init__(self, existing_path, next_node):
		self.path = list()		
		if existing_path is None:
			self.path.append(next_node)
		else:
			self.path = existing_path.get_node_list()
			self.path.append(next_node)

	def get_last_node_on_path(self):
		return self.path[len(self.path)-1]
	
	def get_node_list(self):
		return self.path.copy()
	
	def print_path(self, game_board):
		move_locations = list()
		for path_elt in self.path:
			move_locations.append(path_elt.node_val)
		
		top = "-" * len(game_board) * 2
		print(top)
		for row in range(len(game_board)):
			print("|", end="")
			for col in range(len(game_board[row])):
				game_board_elt = game_board[row][col]
				
				if game_board[row][col] == " " and (row, col) in move_locations:
					game_board_elt = "@"
				
				print(game_board_elt + " ", end="")
			print("|")
		print(top)

class Node:
	def __init__(self, node_val):
		self.node_val = node_val # Tuple (row, col)
		self.children = list()

	def generate_children(self, game_board):
		row, col = self.node_val
		game_board_size = len(game_board)

		# The tuples in this array correspond to moving down, right, up, and left
		possible_moves = [(1,0),(0,1),(-1,0),(0,-1)]

		# Iterate over the possible moves
		for row_move, col_move in possible_moves:
			# Calculate the corresponding index
			row_index, col_index = row + row_move, col + col_move
			
			# Check that both the row and column are in bounds
			# Check that this location on the game_board is not a *
			if row_index < game_board_size and col_index < game_board_size and game_board[row_index][col_index] != "*":
				# If the conditions are satisified, create a new Node instance
				# Append it to the children of this node
				self.children.append(Node((row_index, col_index)))

def convert_maze(maze_file, maze_size):

	row, col = 0,0
	col_index = 0
	game_board = [[None for x in range(maze_size)] for y in range(maze_size)]

	with open(maze_file, 'r') as file:
		for line in file:
			col, col_index = 0,0
			for character in line:
				if col_index % 3 == 1:
					col_index += 1	
					continue

				if character == '.':
					game_board[row][col] = "*"
				else:
					game_board[row][col] = " "
				
				col += 1
				col_index += 1
			row += 1

	return game_board

def print_maze(game_board):
	top = "-" * len(game_board) * 2
	print(top)
	for row in game_board:
		print("|", end="")
		for col in row:
			print(col + " ", end="")
		print("|")
	print(top)

# The method below searches a maze board, given as the input game_board
# It then searches from the initial_node, which is (0,0), to find a 
# path to the target_node, which is (N,N) for a maze of size N
# It returns a Path if one exists, otherwise it returns None
def bfs(game_board, initial_node, target_node):
	# Create a queue. Note our queue will hold Path objects
	queue = Queue()  
	# Enqueue the intial state and the current Path (which is initally None)
	queue.enqueue(Path(None, initial_node))

	# Create a set to keep track of visited state
	# The set below stores tuples of indices (row_index, column_index)
	visited = set()
	# Add the initial Node value to the set
	# Note initial_node.node_val = (0,0)
	visited.add(initial_node.node_val)

	# Standard BFS loop
	while queue.size() > 0:
		# Dequeue a path
		dequeued_path = queue.dequeue() 
		 # Get the last node on this path
		last_node = dequeued_path.get_last_node_on_path()
		
		# Ensure the current node is not None
		if last_node is None:
			continue

		# Check if we have reached the target state 
		# Note that the Nodes will not be equal since they are different objects
		# However both objects will have a node_val of (N,N) where N is the size
		# of the maze
		if last_node.node_val == target_node.node_val:
			return dequeued_path

		# We'll need to add all valid future children to the Queue
		# We can do this by calling the generate_children() function for the current node
		last_node.generate_children(game_board)

		# The generate_children() method updates the children vairable in the Node class
		for child in last_node.children:
			# Check that we have not visited this state
			if child.node_val not in visited:
				# Create a new path object
				new_path = Path(dequeued_path, child)
				# Add this path to the queue
				queue.enqueue(new_path) 
				# Add this node to visited
				visited.add(child.node_val)

	# Return None if no valid path exists
	return None

def main():
	maze_size = 50
	# Create a game board by concerting a maze txt file to a 2-dimensional array
	game_board = convert_maze("mazes/maze_50x50.txt", maze_size*2+1)
	print_maze(game_board)

	# The initial node will be the top left of the board at (0,0)
	initial_node = Node((0,0))
	# The target node will be the bottom right of the board at (N*2,N*2) for a maze
	# of size N
	target_node = Node((maze_size*2,maze_size*2))
	# Call our BFS method with the appropriate inputs
	path = bfs(game_board, initial_node, target_node)
	
	# Check for a valid path and output one if it exists
	if path is not None:
		path.print_path(game_board)

if __name__ == '__main__':
	main()