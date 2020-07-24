def evaluate_heuristic(curr_values):
	location_map = {0: (0,0),  1: (0,1),  2: (0,2),  3: (0,3),
				  	4: (1,0),  5: (1,1),  6: (1,2),  7: (1,3),
				  	8: (2,0),  9: (2,1),  10: (2,2), 11: (2,3),
				  	12: (3,0), 13: (3,1), 14: (3,2)}
	manhattan_dist = 0
	for x in range(len(curr_values)):
		correct_row = int(x/4)
		correct_col = x%4		

		curr_val = curr_values[x]
		curr_row, curr_col = location_map[curr_val]

		curr_dist = abs(curr_row - correct_row) + abs(curr_col - correct_col)
		manhattan_dist += curr_dist

	return manhattan_dist

def main():
	curr_values = [x+1 for x in range(15)]
	curr_values[14] = 0
	manhattan_dist = evaluate_heuristic(curr_values)
	print(manhattan_dist)

if __name__ == '__main__':
	main()

