from numpy import empty # Creates an empty array
import numpy as np # Used for linear algebra
import math # Used for square roots


def clean_paragraph(paragraph):
	stop_words = [" ", "a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", "its", "itself", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should", "should've", "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", "weren't", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would"]
	punctuation = [".", "-", "_", ",", "<", ">", "?", "/", "'", "\"", "“", "”", ";", ":", "[", "{", "}", "]", "\\", "|", "`", "~", "!", "@", "#", "$", "^", "&", "*", "(", ")"]
	# Create an array to contain the words in the paragraph
	cleaned_paragraph = list()

	# Split the paragraphs into words by splitting on spaces
	words = paragraph.strip().split(" ")
	# Iterate over each word
	for word in words:
		# Make all words lowercase
		word = word.lower()
		# Iterate over each punctuation mark and remove it
		# We can remove it by simply replacing it with an empty string
		for char in punctuation:
			word = word.replace(char, '')	
		# If the word is not a stop word and the word is not an empty string
		# then add it to the cleaned_paragraph array
		if word not in stop_words and len(word) > 0:
			cleaned_paragraph.append(word)

	# Return the cleaned paragraph
	return cleaned_paragraph


def clean_book(file_location):
	book = list()
	book_map = list()

	# Open the book file and iterate over each line
	# Note that lines are separated by the newline character '\n'
	with open(file_location) as file_input:
		for line in file_input:
			# If the file is only a newline character, we can skip this line
			if line == "\n":
				continue

			# Otherwise, replace any newline characters
			line = line.replace("\n", "")
			# Clean the paragraphs
			cleaned_paragraph = clean_paragraph(line)
			# Add the original paragraph and the cleaned paragraph to our map
			if (line, cleaned_paragraph) not in book_map:
				book_map.append((line, cleaned_paragraph))

	# Return the fully formed map
	return book_map


def cosine_similarity(paragraph1, paragraph2):
	# Create a set and add all the words in paragraph1 and paragraph2
	# to this set. There's no need to keep track of duplicates
	all_words = set()
	all_words.update(paragraph1)
	all_words.update(paragraph2)

	# For each word in the set of all_words:
	#	add a 1 if this word is in paragraph1 otherwise add 0
	# Do this for both paragraph1 and paragraph2
	paragraph1vector = list()
	paragraph2vector = list()
	for word in all_words:
		paragraph1vector.append(1) if word in paragraph1 else paragraph1vector.append(0)
		paragraph2vector.append(1) if word in paragraph2 else paragraph2vector.append(0)
	
	# Convert these lists to NumPy arrays so we can use built-in linear algebra functions
	pg1vect = np.asarray(paragraph1vector, dtype=np.float32)
	pg2vect = np.asarray(paragraph2vector, dtype=np.float32)

	# Cosine similarity is defined as the dot product of two vectors over
	# the product of their magnitudes
	# Calculate these values using numpy functions
	sum_val = np.dot(pg1vect, pg2vect)
	magnitudeA = np.linalg.norm(pg1vect)
	magnitudeB = np.linalg.norm(pg2vect)

	# This prevents errors that arise due to division by 0
	if magnitudeA == 0 or magnitudeB == 0:
		return 0.0

	# Calculate the cosine similarity
	cosine_sim_val = float(sum_val) / float(magnitudeA*magnitudeB)

	# Return this value
	return cosine_sim_val


def build_matrix(paragraph_list):
	n = len(paragraph_list)
	# Create an empty NxN matrix which will be our adjacency matrix
	adjacency_matrix = empty([n,n])
	
	# The cosine similarity for vectors A and B is the same as the cosine similarity
	# for vectors B and A, so we only need to calculate these values once.
	# Then we can updated adjacency_matrix[x][y] and adjacency_matrix[y][x] accordingly.
	for x in range(n):
		for y in range(x, n):
			cos_sim = cosine_similarity(paragraph_list[x][1], paragraph_list[y][1])
			adjacency_matrix[x][y] = cos_sim
			adjacency_matrix[y][x] = cos_sim

	# Return the adjacency matrix
	return adjacency_matrix


def calculate_stationary_probabilities(adjacency_matrix):
	# Code pulled from Duke University, Stats 663 from Dr. Cliburn Chan
	# http://people.duke.edu/~ccc14/sta-663-2016/homework/Homework02_Solutions.html#Part-3:-Option-2:-Using-numpy.linalg-with-transpose-to-get-the-left-eigenvectors

	a = adjacency_matrix
	b = np.sum(adjacency_matrix, 1)[:, np.newaxis]
	
	normalized_matrix = c = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
	
	matrix_mult_result = np.linalg.matrix_power(normalized_matrix, 5000)
	matrix_mult_result_check = np.dot(matrix_mult_result, normalized_matrix)
	np.testing.assert_allclose(matrix_mult_result, matrix_mult_result_check)
	return matrix_mult_result_check


def output_summarization_paragraphs(distribution, book_map, num_paragraphs):
	# This is some fancy NumPy code that sorts of distribution
	# It returns a set of indices from highest value to lowest value
	# We can then iterate over these indices and pull the associated paragraphs
	indices = distribution.argsort()[-(num_paragraphs):][::-1]
	for index in indices:
		print("Paragraph:	" + str(book_map[index][0]))
		print("Probability: " + str(distribution[index]))
		print("---------------")


def main():
	# Clean the test
	book_map = clean_book("1984.txt")
	# Build an adjancey matrix
	adjacency_matrix = build_matrix(book_map)
	# Calculate the steady state probabilities
	probability_distribution = calculate_stationary_probabilities(adjacency_matrix)
	# Output the best sentences
	output_summarization_paragraphs(probability_distribution[0], book_map, 10)

if __name__ == '__main__':
	main()

