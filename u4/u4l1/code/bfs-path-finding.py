import time

class Node:
	def __init__(self, left_child, right_child, left_child_val, right_child_val, node_val):
		self.left_child = left_child # Node
		self.right_child = right_child # Node
		self.left_child_val = left_child_val # Integer
		self.right_child_val = right_child_val # Integer
		self.node_val = node_val # Intersection Name i.e. A,B,C,D,etc.
class Path:
	def __init__(self, existing_path, next_node, edge_weight):
		self.path = list()		
		if existing_path is None:
			self.path.append(next_node)
			self.path_val = edge_weight # Initially the cost of all paths are 0
		else:
			self.path = existing_path.get_node_list()
			self.path.append(next_node)
			self.path_val = existing_path.path_val + edge_weight  # Initially the cost of all paths are 0

	def get_last_node_on_path(self):
		return self.path[len(self.path)-1]
	
	def get_node_list(self):
		return self.path.copy()
	
	def print_path(self):
		for x in range(len(self.path)-1):
			print(self.path[x].node_val + "->", end="")
		print(self.get_last_node_on_path().node_val)
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

node_i = Node(None, None, 101, 101, "I")
node_f = Node(None, node_i, 101, 23, "F")
node_h = Node(node_i, None, 1, 101, "H")
node_g = Node(node_h, None, 27, 101, "G")
node_e = Node(node_f, node_h, 31, 3, "E")
node_d = Node(node_g, node_e, 15, 1, "D")
node_c = Node(None, node_f, 101, 20, "C")
node_b = Node(node_c, node_e, 11, 19, "B")
node_a = Node(node_d, node_b, 2, 16, "A")

def breadth_first_traversal(beginning_node, target_node):
	queue = Queue() 
	best_path_and_val = (None, 401) 
	path = Path(None, beginning_node, 0)
	queue.enqueue(path)


	while queue.size() > 0:

		dequeued_path = queue.dequeue()
		last_node = dequeued_path.get_last_node_on_path()

		if last_node is None:
			continue # This does not represent a valid path

		if last_node.node_val == target_node.node_val:
			if dequeued_path.path_val < best_path_and_val[1]:
		  		best_path_and_val = dequeued_path, dequeued_path.path_val
			continue # Reached node I
		
		if last_node.right_child is not None:
			right_path = Path(dequeued_path, last_node.right_child, last_node.right_child_val)
			queue.enqueue(right_path) # Add right path

		if last_node.left_child is not None:
			straight_path = Path(dequeued_path, last_node.left_child, last_node.left_child_val)
			queue.enqueue(straight_path) # Add straight path

	(best_path, val) = best_path_and_val
	best_path.print_path()
	print(val)


def generate_random_grid(n):
	node_arr = list()
	for y in range(n):
		internal_node_arr = [Node(None, None, 1, 1, str(y)+str(x)) for x in range(n)]
		node_arr.append(internal_node_arr)

	for x in range(n):
		for y in range(n):
			curr_node = node_arr[x][y]
			if y < (n-1):
				curr_node.right_child = node_arr[x][y+1]
			if x < (n-1):
				curr_node.left_child = node_arr[x+1][y]

	return node_arr

def time_trials(min_grid, max_grid):
	for n in range(min_grid, max_grid):
		node_arr = generate_random_grid(n)
		start = time.time()
		breadth_first_traversal(node_arr[0][0], node_arr[n-1][n-1])
		end = time.time()
		print(str(n) + " : " + str(round(end - start, 2)) + " seconds")

def main():
	# breadth_first_traversal(node_a, node_i)
	# generate_random_grid(10)
	time_trials(5, 15)

if __name__ == '__main__':
	main()