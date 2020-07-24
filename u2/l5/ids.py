class Stack:
	def __init__(self):
		self.stack = []
	
	def push(self, e):
		self.stack.append(e)
	
	def pop(self):
		return self.stack.pop()
	
	def peek(self):
		return self.stack[-1]

	def is_empty(self):
		return len(self.stack) == 0

class Node:
	def __init__(self, value):
		self.value = value
		self.children = []
		self.depth = 1

	def add_children(self, children):
		self.children.extend(children)
		for child in children:
		  child.depth = self.depth+1

	def get_value(self):
		return self.value

	def get_children(self):
		return self.children

	def get_depth(self):
		return self.depth

def iddfs(root, search_val, max_depth):
	curr_depth = 1
	
	while curr_depth <= max_depth:
		stack = Stack()
		stack.push(root)
		
		while not stack.is_empty():
			curr_node = stack.pop()
			if curr_node.get_value() == search_val:
				return True
			
			for child in curr_node.get_children():
				if child.get_depth() <= curr_depth:
					stack.push(child)

		curr_depth += 1

	return False

def main():
	root = Node(1)
	left_child = Node(2)
	right_child = Node(5)
	root.add_children([left_child, right_child])
	left_child.add_children([Node(3), Node(4)])
	right_child.add_children([Node(6), Node(7)])

	print(iddfs(root, 6, 1)) # False
	print(iddfs(root, 6, 2)) # False
	print(iddfs(root, 6, 3)) # True

if __name__ == '__main__':
	main()