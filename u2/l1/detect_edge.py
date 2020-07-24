class Node:
	def __init__(self, value):
		self.value = value

	def get_value(self):
		return self.value


def has_edge(node_1, node_2, edges):

	for edge in edges:
		first_node, second_node = edge
		if 	(node_1 == first_node and node_2 == second_node) or (node_2 == first_node and node_1 == second_node):
			return True

	return False


def main():

	Node_A = Node("A")
	Node_B = Node("B")
	Node_C = Node("C")
	Node_D = Node("D")
	Node_H = Node("H")
	Node_I = Node("I")

	edges = [(Node_A, Node_B), (Node_A, Node_C), (Node_A, Node_I), (Node_A, Node_D), (Node_B, Node_B), (Node_B, Node_C), (Node_D, Node_H), (Node_I, Node_I)]

	print(has_edge(Node_A, Node_B, edges))
	print(has_edge(Node_I, Node_A, edges))
	print(has_edge(Node_A, Node_H, edges))

if __name__ == '__main__':
	main()
