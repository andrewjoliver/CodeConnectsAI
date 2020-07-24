class Node:
	def __init__(self, value, adj_list):
		self.value = value
		if adj_list is None:
			self.adj_list = {}
		else:
			self.adj_list = adj_list

def dijkstra(node_list, beg_node):
	mst_edges = list()
	visited_nodes = set()
	inf = float('inf')
	
	# Set the distances of all nodes to infinity
	dist = dict()
	for node in node_list:
		dist[node] = inf
	dist[beg_node] = 0

	visited_nodes.add(beg_node)

	while len(visited_nodes) < len(node_list):

		beg_node, end_node = None, None
		min_val = inf

		# Find minimal edge extending from any node in our visited set

		for node in visited_nodes:
			for adj_node in node.adj_list:
				if node.adj_list[adj_node] < min_val and adj_node not in visited_nodes:
					min_val = node.adj_list[adj_node]
					beg_node, end_node = node, adj_node

		mst_edges.append("(" + str(beg_node.value) + ", " + str(end_node.value) + ")")
		visited_nodes.add(end_node)

		# Update values based on this end node

		for adj_node in end_node.adj_list:
			old_val = dist[adj_node]
			new_val = dist[end_node] + end_node.adj_list[adj_node]
			if new_val < old_val:
				dist[adj_node] = new_val
	print(mst_edges)


def main():
	node_0 = Node(0, None)
	node_1 = Node(1, None)
	node_2 = Node(2, None)
	node_3 = Node(3, None)
	
	node_0.adj_list = {node_1:1, node_2:10}
	node_1.adj_list = {node_0:1, node_2:2}
	node_2.adj_list = {node_0:10, node_1:2, node_3:5}
	node_3.adj_list = {node_2:5}

	node_list = [node_0, node_1, node_2, node_3]

	dijkstra(node_list, node_0)
	dijkstra_decomposed(node_list, node_0)



if __name__ == '__main__':
	main()