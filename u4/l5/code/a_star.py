import heapq 

class PriorityQueue:
	def __init__(self):
		self.elements = []
	
	def size(self):
		return len(self.elements)
	
	def put(self, item, priority):
		heapq.heappush(self.elements, ((priority, id(item)), item))
	
	def get(self):
		return heapq.heappop(self.elements)[1]

class Node:
	def __init__(self, val, adj_list, coords):
		self.val = val
		self.adj_list = adj_list
		self.coords = coords

	def evaluate_heuristic(self, goal_state):
		goal_state_x, goal_state_y = goal_state.coords
		curr_x, curr_y = self.coords
		manhattan_dist = abs(goal_state_x - curr_x) + abs(goal_state_y - curr_y)
		return manhattan_dist

class FifteensNode:
	def __init__(self, board_state):
		self.board_state = board_state

	def generate_future_state(self):
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
			
			return new_board_state

		# The free space moves are up, down, left, and right
		free_space_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
		for move in free_space_moves:
			row, col = move
			# Ensure that the move is a valid move
			if row < 0 or row > 3 or col < 0 or col > 3:
				continue
			else:
				future_boards.append(create_new_board(move))
		return future_boards

	def evaluate_heuristic(self):
		curr_values = self.board_state
		location_map = {0: (0,0),  1: (0,1),  2: (0,2),  3: (0,3),
						4: (1,0),  5: (1,1),  6: (1,2),  7: (1,3),
						8: (2,0),  9: (2,1),  10: (2,2), 11: (2,3),
						12: (3,0), 13: (3,1), 14: (3,2), -1: (3,3)} # Define a location map

		manhattan_dist = 0
		for x in range(len(curr_values)):
			correct_row = int(x/4) # Division and rounding gives us the row
			correct_col = x%4	# Modulus operator gives us the column

			curr_val = curr_values[x]
			curr_row, curr_col = location_map[curr_val] # Get the current location of the tile

			curr_dist = abs(curr_row - correct_row) + abs(curr_col - correct_col)
			manhattan_dist += curr_dist

		return manhattan_dist

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
	frontier = PriorityQueue() # Create priority queue
	frontier.put(initial_state, 0) # Add the initial state with 0 priority
	parent_child_dict = {} 
	dist = {} # Create dist dictionary as in Dijkstra's Algorithm
	parent_child_dict[initial_state] = None
	dist[initial_state] = 0
	
  # Iterate while there are still nodes
  # Similar to BFS/DFS
	while frontier.size() > 0: 
		curr_state = frontier.get()
		
		for key in dist:
			print(dist[key], end=", ")
		print()

		if curr_state == goal_state: # Exit the while loop
			break

    # Iterate over all children and calculate the cost to reach these nodes
    # from the current node
    # If it is lower than our current cost, update the value
    # Add these nodes to our priority queue with the priority of their weight
		for next_state in curr_state.adj_list.keys():

			new_cost = dist[curr_state] + curr_state.adj_list[next_state]
			
			if next_state not in dist or new_cost < dist[next_state]:
				dist[next_state] = new_cost
				priority = new_cost + next_state.evaluate_heuristic(goal_state)
				frontier.put(next_state, priority)
				parent_child_dict[next_state] = curr_state
	
	return parent_child_dict

def reconstruct_path(parent_child_dict, goal_state):
	path = []
	# Convert dictionary entries to an array
	curr_node = goal_state
	while curr_node != None:
		path.append(curr_node)
		curr_node = parent_child_dict[curr_node]

	# This array is backwards (i.e. the target node is the last element)
	# So we will print it in reverse
	index = len(path)-1
	while index >= 0:
		if index == 0:
			print(path[index].val)
			break
		print(path[index].val, end="->")
		index -= 1

def main():
	node_a = Node("A", None, (0,2))
	node_b = Node("B", None, (3,5))
	node_c = Node("C", None, (5,5))
	node_d = Node("D", None, (4,0))
	node_e = Node("E", None, (7,2))
	node_f = Node("F", None, (9,0))
	node_g = Node("G", None, (9,2))
	node_h = Node("H", None, (11,2))

	node_a.adj_list = {node_b:20, node_c:28, node_d:33}
	node_b.adj_list = {node_a:20, node_b:17}
	node_c.adj_list = {node_b:17, node_e:16, node_h:71}
	node_d.adj_list = {node_a:33, node_f:58}
	node_e.adj_list = {node_c:16, node_g:9, node_f:12}
	node_f.adj_list = {node_d:58, node_e:12, node_h:14}
	node_g.adj_list = {node_e:9, node_h:38}
	node_h.adj_list = {node_c:71, node_g:38, node_f:14}

	parent_child_dict = a_star(node_a, node_h)
	reconstruct_path(parent_child_dict, node_h)

if __name__ == '__main__':
	main()

