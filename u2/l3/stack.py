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

class Node:
	def __init__(self, val):
		self.val = val
		self.c = []
  
	def value(self):
		return self.val
  
	def children(self):
		return self.c

	def add_children(self, children):
		self.c.extend(children)

def flip_string(string_input):
	my_stack = Stack()
	for char in string_input:
		my_stack.push(char)
	output_string = ""
	while not my_stack.is_empty():
		curr_char = my_stack.pop()
		output_string += curr_char
	return output_string

def depth_first_search_tree(node, search_val):
	stack = Stack()
	stack.push(node)

	while not stack.is_empty():
		curr_node = stack.pop()
		if curr_node.val == search_val:
			return True

		for c in curr_node.children():
			stack.push(c)
	
	return False

def depth_first_traversal_tree(node):
	stack = Stack()
	stack.push(node)
	all_nodes = []
	while not stack.is_empty():
		curr_node = stack.peek()
		all_nodes.append(curr_node.value())
		for c in curr_node.children():
			stack.push(c)
	
	return all_nodes

def depth_first_search(initial_node, search_val):
	stack = Stack()
	stack.push(initial_node)
	visited = set()

	while not stack.is_empty():
		curr_node = stack.pop()
	
		if curr_node not in visited:
			visited.add(curr_node)

			if curr_node.val == search_val:
				return True

	  		# We don't need to check if these nodes have been visited already
	  		# If they have, they will simply be popped from the stack
			for c in curr_node.children():
				stack.push(c)
	
	return False

def main():
	A = Node("A")
	B = Node("B")
	C = Node("C")
	D = Node("D")
	E = Node("E")
	F = Node("F")

	A.add_children([B])
	B.add_children([C, D])
	C.add_children([B, C, E])
	D.add_children([B, E])
	E.add_children([F, C, D])
	F.add_children([E])
	print(depth_first_search(A, "F")) # True
	print(depth_first_search(A, "Z")) # False

if __name__ == '__main__':
	main()