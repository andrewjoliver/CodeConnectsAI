import random 
import re

class AdjacencyMatrix:
	def __init__(self, n):
		# Create an NxN matrix with no values initially
		self.adj_m = [ [None for y in range(n)] for z in range(n)]
		self.size = n
	
	def add_edge(self, i, j, val):
		self.adj_m[i][j] = val

	def get_edge_val(self, i,j):
		return self.adj_m[i][j]

	def generate_rand_matrix(self):
		self.adj_m = [ [(random.randint(1,100),random.randint(1,100)) for y in range(self.size)] for z in range(self.size)]
		self.adj_m[0][0] = None
		self.adj_m[self.size-1][self.size-1] = None

	def print_matrix(self):
		dash = '--------------' * self.size
		# 0,1,2,3,4,..., etc.
		print("\t", end="")
		for x in range(self.size):
			print(str(x) + "\t\t", end="")
		print("")
		print("\t" + dash)
		for x in range(self.size):
			print(str(x) + " |\t", end="")
			for y in range(self.size):
				if self.adj_m[x][y] == None:
					print("*\t\t", end="")
				else:
					val_1 = str(self.adj_m[x][y][0]).zfill(2)
					val_2 = str(self.adj_m[x][y][1]).zfill(2)
					str_val = "(" + str(val_1) + ", " + str(val_2) + ")"
					print(str(str_val) + "\t", end="")
			print("")
class Node:
	def __init__(self, value, adjacent_nodes):
		self.value = value # String e.g. A,B,C
		self.adjacent_nodes = adjacent_nodes # List
class NodeCell:
	def __init__(self, x, y, n):
		self.node_val = str("(" + str(x) + ", " + str(y) +")")
		self.x = x
		self.y = y
		if x == (n-1):
			self.right_child = None
		else:
			x_child = x+1
			self.right_child = NodeCell(x_child, y, n)

		if y == (n-1):
			self.left_child = None
		else:
			y_child = y+1
			self.left_child = NodeCell(x, y_child, n)	
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
	def __init__(self, existing_path, next_node, edge_weight):
		self.path = list()		
		if existing_path is None:
			self.path.append(next_node)
			self.path_val = edge_weight # Initially the cost of all paths are 0
		else:
			self.path = existing_path.get_node_list()
			self.path.append(next_node)
			self.path_val = existing_path.path_val + edge_weight  # Initially the cost of all paths are 0

	def get_node_list(self):
		return self.path.copy()

	def get_last_node_on_path(self):
		return self.path[len(self.path)-1]
	
	def print_path(self):
		for x in range(len(self.path)-1):
			print(self.path[x].node_val + "->", end="")
		print(self.path[-1].node_val)

def create_graph_of_nodes():
	node_a = Node("A", None)
	node_b = Node("B", None)
	node_c = Node("C", None)
	node_d = Node("D", None)
	node_h = Node("H", None)
	node_i = Node("I", None)

	node_a.adjacent_nodes = [node_b, node_c, node_d, node_i]
	node_b.adjacent_nodes = [node_a, node_b, node_c]
	node_c.adjacent_nodes = [node_b, node_c]
	node_d.adjacent_nodes = [node_a, node_h]
	node_h.adjacent_nodes = [node_d]
	node_i.adjacent_nodes = [node_a, node_i]

	return node_a


def create_and_print_adj_m():
	adj_m = AdjacencyMatrix(7)
	adj_m.add_edge(3,4,10)
	print(adj_m.get_edge_val(3,4))
	print(adj_m.get_edge_val(4,3))
	adj_m.print_matrix()


def convert_graph_to_adj_m(root_node, num_nodes):
	node_int_map = dict()
	node_num = 0
	
	queue = Queue()
	visited_nodes = set()
	queue.enqueue(root_node)
	
	adj_m = AdjacencyMatrix(num_nodes)
	while queue.size() > 0:
		curr_node = queue.dequeue()
		visited_nodes.add(curr_node)

		if curr_node not in node_int_map.keys():
			node_int_map[root_node] = node_num
			node_num += 1
		
		for adjacent_node in curr_node.adjacent_nodes:
			i = node_int_map[curr_node]
			if adjacent_node not in node_int_map.keys():
				node_int_map[adjacent_node] = node_num
				node_num += 1
			j = node_int_map[adjacent_node]
			adj_m.add_edge(i,j,1)

		for adjacent_node in curr_node.adjacent_nodes:
			if adjacent_node not in visited_nodes:
				queue.enqueue(adjacent_node)


	return node_int_map,adj_m


def generate_rand_adj_m(n):
	adj_m = AdjacencyMatrix(n)
	adj_m.generate_rand_matrix()
	return adj_m


def merge_paths(path_1, path_2, n):
	path_1_node_list = path_1.get_node_list()
	path_2_node_list = path_2.get_node_list()
	final_path_list = list()

	for x in range(len(path_1_node_list)-1):
		final_path_list.append(path_1_node_list[x].node_val)

	for x in range(len(path_2_node_list)):
		x_val, y_val = path_2_node_list[x].x, path_2_node_list[x].y
		# x_val += (n-1)
		# y_val += (n-1)
		final_path_list.append(str((x_val, y_val)))

	final_val = path_1.path_val + path_2.path_val
	return (final_path_list, final_val)


def breadth_first_search(beginning_node, target_node, adj_m, top_left):
	n = adj_m.size
	queue = Queue() 
	best_path_and_val = None
	
	if top_left:
		best_path_and_val = dict()
		for node in target_node.keys():
			best_path_and_val[node] = (None, 100*n+1)
	else:
		best_path_and_val = (None, 100*n+1) 
	
	path = Path(None, beginning_node, 0)
	queue.enqueue(path)

	while queue.size() > 0:

		dequeued_path = queue.dequeue()
		last_node = dequeued_path.get_last_node_on_path()

		if top_left:
			if last_node.node_val in target_node.keys():
				if dequeued_path.path_val < best_path_and_val[last_node.node_val][1]:
			  		best_path_and_val[last_node.node_val] = dequeued_path, dequeued_path.path_val
				continue
		else:
			if last_node.node_val == target_node.node_val:
				if dequeued_path.path_val < best_path_and_val[1]:
			  		best_path_and_val = dequeued_path, dequeued_path.path_val
				continue # Reached target
				
		if last_node.right_child is not None:
			init_x = last_node.x
			curr_x = last_node.right_child.x
			tuple_loc = 1 if curr_x != init_x else 0
			
			path_cost = adj_m.get_edge_val(last_node.right_child.x, last_node.right_child.y)
			path_cost = 0 if path_cost is None else path_cost[tuple_loc]

			right_path = Path(dequeued_path, last_node.right_child, path_cost)
			queue.enqueue(right_path) # Add right path

		if last_node.left_child is not None:
			init_x = last_node.x
			curr_x = last_node.left_child.x
			tuple_loc = 1 if curr_x != init_x else 0
			
			path_cost = adj_m.get_edge_val(last_node.left_child.x, last_node.left_child.y)
			path_cost = 0 if path_cost is None else path_cost[tuple_loc]
			
			straight_path = Path(dequeued_path, last_node.left_child, path_cost)
			queue.enqueue(straight_path) # Add straight path

	return best_path_and_val


def bidi_search(n):
	cityville = generate_rand_adj_m(n)
	cityville.print_matrix()

	beginning_node = NodeCell(0, 0, n)
	
	middle_nodes = dict()
	for x in range(n):
		y_val = n-x-1
		node_val = str("(") + str(x) + str(", ") + str(y_val) + str(")")
		middle_nodes[node_val] = NodeCell(x, y_val, n)

	target_node = NodeCell(n-1, n-1, n)
	
	best_tl_paths = breadth_first_search(beginning_node, middle_nodes, cityville, True)
	
	best_br_paths = list()
	for node in middle_nodes:
		x,y = node.split(",")
		x = re.sub('[^0-9]','', x)
		y = re.sub('[^0-9]','', y)
		node_cell = NodeCell(int(x), int(y), n)
		best_path_and_val = breadth_first_search(node_cell, target_node, cityville, False)
		best_br_paths.append(best_path_and_val)

	best_path, best_val = None, 100*n+1
	tl_keys = list(best_tl_paths.keys())
	
	for x in range(len(tl_keys)):
		path = tl_keys[x]
		curr_path = best_tl_paths[path][0]
		curr_path, curr_val = merge_paths(curr_path, best_br_paths[x][0], n)
		if curr_val < best_val:
			best_path, best_val = curr_path, curr_val

	print(str("Final Path: ") + "->".join(best_path))
	print(str("Final Path Value: " + str(best_val)))


def main():
	# create_and_print_adj_m()
	# root_node = create_graph_of_nodes()
	# node_int_map,adj_m = convert_graph_to_adj_m(root_node, 6)
	# adj_m = generate_rand_adj_m(5)
	# adj_m.print_matrix()
	# for key in node_int_map.keys():
	# 	print("{" + str(key.value) + ": " + str(node_int_map[key]) + "}, ", end="")
	# print("")
	# adj_m.print_matrix()
	# bidirectional_search(adj_m)
	bidi_search(13)
	

if __name__ == '__main__':
	main()