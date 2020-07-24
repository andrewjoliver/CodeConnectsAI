from copy import copy, deepcopy

# Implementation of the Stack class from Unit 2 Lesson 3
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

# This method prints out the board state in a nicely formatted way
# Don't worry about the implementation - it is mostly hardcoded to work
def print_towers(disk_locations):	
	l1 = l11 = "-" if 1 in disk_locations[0] else " "
	l2 = l22 = "--" if 2 in disk_locations[0] else "  "
	l3 = l33 = "---" if 3 in disk_locations[0] else "   "
	
	m1 = m11 = "-" if 1 in disk_locations[1] else " "
	m2 = m22 = "--" if 2 in disk_locations[1] else "  "
	m3 = m33 = "---" if 3 in disk_locations[1] else "   "
	
	r1 = r11 = "-" if 1 in disk_locations[2] else " "
	r2 = r22 = "--" if 2 in disk_locations[2] else "  "
	r3 = r33 = "---" if 3 in disk_locations[2] else "   "

	row_1 = "   " + l1 + "|" + l11 + "\t\t   " + m1 + "|" + m11 + "\t\t   " + r1 + "|" + r11
	row_2 = "  " + l2 + "|" + l22 + "\t\t  " + m2 + "|" + m22 + "\t\t  " + r2 + "|" + r22
	row_3 = " " + l3 + "|" + l33 + "\t " + m3 + "|" + m33 + "\t " + r3 + "|" + r33
	row_4 = "____|____ 	" + "____|____	" + "____|____"
	row_5 = "T1	        T2              T3"

	print()
	print(row_1)
	print(row_2)
	print(row_3)
	print(row_4)
	print(row_5)
	print()

def generate_next_states(current_state):
	# When generating future states, we have three possibilties.
	# We can always move the smallest disk, which we call disk 1, to the two pegs where it is currently not
	# If disk 2 does not sit under disk 1, we can move it to the peg which does not contain disk 1
	# We can only move disk 3 if no disk (i.e. disk 1 and disk 2) sit ontop of it and there is an open peg

	# Create a list to keep track of all future states 
	future_states = list()

	# Our first tasks will be to identify which peg each disk currently sits on
	# The follow for loops do that
	
	one_x_index = None
	two_x_index = None
	three_x_index = None

	for x in range(3):
		for y in range(3):
			if current_state[x][y] == 1:
				one_x_index = x
			if current_state[x][y] == 2:
				two_x_index = x
			if current_state[x][y] == 3:
				three_x_index = x

	# The code below moves disk 1 to the other two pegs
	# If disk 1 is on peg 1, we move it to peg 2 and peg 3
	# If disk 1 is on peg 2, we move it to peg 1 and peg 3
	# If disk 1 is on peg 3, we move it to peg 1 and peg 2

	# The move_vals array adds/subtracts values accordingly
	# The code below moves disk 1 to the appropriate pegs and adds these new states to
	# the array of future states
	move_vals = [[1,2], [-1,1], [-1,-2]]

	# The deepcopy() method creates a full copy of the current_state board
	# We can modify this current_state board and add it as a future state 
	future_state = deepcopy(current_state)
	move_val_1, move_val_2 = move_vals[one_x_index]
	
	future_state[one_x_index][2] = None
	future_state[one_x_index + move_val_1][2] = 1
	future_states.append(future_state)

	future_state = deepcopy(current_state)
	future_state[one_x_index][2] = None
	future_state[one_x_index + move_val_2][2] = 1
	future_states.append(future_state)


	# Now that we have moved disk 1 to the relevant pegs, we can move disk 2
	# Disk 2 can only be moved if disk 1 is not on top of it, this is checked by our if statement
	# There are three possible pegs where we can move disk 2. Since disk 2 and disk 1 aren't
	# on the same peg, they must be on different ones. This means we can move disk 1 to exactly
	# one other peg. We start with an array with values 0,1,2 and remove the indices where disk 1 and 
	# disk 2 are. Then we move disk 2 to this peg
	if one_x_index != two_x_index:
		future_state = deepcopy(current_state)
		x_indices = [0,1,2]
		x_indices.remove(one_x_index)
		x_indices.remove(two_x_index)
		future_state[two_x_index][1] = None
		future_state[x_indices[0]][1] = 2
		future_states.append(future_state)

	# Lastly, we check that disk 3 does not share a peg with disk 2 or disk 1
	# If so, we can move disk 3 to any empty peg. The code below does this
	if three_x_index != two_x_index and three_x_index != one_x_index:
		empty_peg_index = -1
		for x in range(len(current_state)):
			peg = current_state[x]
			if peg == [None, None, None]:
				empty_peg_index = x

		if empty_peg_index != -1:
			future_state = deepcopy(current_state)
			future_state[three_x_index][0] = None
			future_state[empty_peg_index][0] = 3
			future_states.append(future_state)

	# We finally return all possible future states
	return future_states

def is_goal_state(current_state):
	# We know the goal state has 3,2,1 stacked on the last ring
	# By the way we've defined our state and transition function, all other entries will be None
	# We can check if the current state equals the goal state and return this Boolean value
	goal_state = [[None,None,None], [None,None,None], [3,2,1]]
	return current_state == goal_state

def state_space_search(initial_state):
	stack = Stack()
	# Our stack will contain tuples. The first element will be the current board state
	# The second element will keep track of the current path by maintaining an array of board states
	stack.push((initial_state, [initial_state]))
	optimal_solution = None
	
	while not stack.is_empty():
		curr_node = stack.pop()

		# Check if we are at the goal state
		if is_goal_state(curr_node[0]):
			# If we have no current optimal solution
			# Or if the number of moves (which is the length) is more minimal
			# Update the optimal solution to the current path
			if optimal_solution is None or len(curr_node[1]) < len(optimal_solution):
				optimal_solution = curr_node[1]

		# Generate all future states from the current state
		for next_state in generate_next_states(curr_node[0]):
			# Make sure we have not visited this state along our current path
			# Recall that we maintain the current path as the second element in our stack
			if next_state not in curr_node[1]:
				# Add this node to our stack
				# Update the path to include the next state
				# Note: We'll need to make the next_state its own array by using [next_state]
				# and adding it to the current path
				stack.push((next_state, curr_node[1] + [next_state]))

	# Finally, return the optimal solution
	# Note that this value may be None if no solution exists
	return optimal_solution

def main():
	# Define the current state as the starting state of the board
	current_state = [[3,2,1], [None, None, None], [None,None,None]]
	# Begin state space search. Save the return value as the path
	path = state_space_search(current_state)
	# Print the board states out in the formatted way if a solution exists
	if path is None:
		print("No solution exists.")
	else:
		for state in path:
			print_towers(state)

if __name__ == '__main__':
	main()