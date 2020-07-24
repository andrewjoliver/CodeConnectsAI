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
		return self.q[0]

	def size(self):
		return len(self.q)

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

def breadth_first_search(node, value_to_find):
    queue = Queue()
    queue.enqueue(node)
    while queue.size() != 0:
        dequeued = queue.dequeue()
        if dequeued.value() == value_to_find:
            return True
        for c in dequeued.children():
            queue.enqueue(c)
    
    return False

def breadth_first_search_graph(node, value_to_find):
    queue = Queue()
    queue.enqueue(node)
    visited = set()

    while queue.size() != 0:
        dequeued = queue.dequeue()
        visited.add(dequeued)
        if dequeued.value() == value_to_find:
            return True
        for c in dequeued.children():
            if c not in visited:
                queue.enqueue(c)

    return False

def bacon_number_search(Kevin_Bacon):
	actor_number_dict = dict()
	actor_number_dict[Kevin_Bacon.value()] = 0
	
	queue = Queue()
	# Our Queue will be tuples of (Node, Bacon-Num) 
	# so we can continually update our Bacon Number.
	queue.enqueue((Kevin_Bacon, 0))
	visited = set()

	while queue.size() != 0:
		dequeued_node, curr_bacon_num = queue.dequeue()
		actor_number_dict[dequeued_node.value()]=curr_bacon_num
		visited.add(dequeued_node)
		for c in dequeued_node.children():
			if c not in visited:
				queue.enqueue((c, curr_bacon_num+1))

	return actor_number_dict


def main():
	Kevin_Bacon = Node("Bacon")
	# BN = 1 -- Apollo 13 w./ Bacon
	Tom_Hanks = Node("Hanks")
	# BN = 1 -- Crazy Stupid Love w./ Bacon	
	Emma_Stone = Node("Stone")
	# BN = 2 -- Philadelphia w./ Hanks
	Denzel_Washington = Node("Washington")
	# BN = 2 -- The Post w./ Hanks
	Meryl_Streep = Node("Streep")
	# BN = 2 -- La La Land w./ Stone
	Ryan_Gosling = Node("Gosling")
	# BN = 2 -- The Great Debaters w./ Washington
	Jurnee_Smollett_Bell = Node("Smollett-Bell")
	# BN = 3 -- Little Women w./ Streep
	Timothee_Chalamet = Node("Chalamet")
	# BN = 4 -- Interstellar w./ Chalamet
	Anne_Hathaway = Node("Hathaway")
	# BN = 5 -- The Intern w./ Hathaway
	Robert_DeNiro = Node("DeNiro")

	Kevin_Bacon.add_children([Tom_Hanks, Emma_Stone])
	Tom_Hanks.add_children([Denzel_Washington, Meryl_Streep])
	Emma_Stone.add_children([Ryan_Gosling])
	Denzel_Washington.add_children([Jurnee_Smollett_Bell])
	Meryl_Streep.add_children([Timothee_Chalamet])
	Timothee_Chalamet.add_children([Anne_Hathaway])
	Anne_Hathaway.add_children([Robert_DeNiro])

	actor_number_dict = bacon_number_search(Kevin_Bacon)
	print(actor_number_dict)

if __name__ == '__main__':
  main()

