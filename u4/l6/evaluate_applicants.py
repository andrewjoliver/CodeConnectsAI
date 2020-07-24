import collections
import numpy as np

def calculate_heuristic_val(applicant_data):
	university, major, GPA, SAT = 0,0,0,0

	# Set university = 4 to the hueristic value if they went to a top 20 university
	if applicant_data[0] == '0':
		university = 4.0

	# Set major 4 to the hueristic value if their major is in CS, Math/Stat, or Engineer
	if applicant_data[1] in ['CS', 'Math/Stat', 'Engineering']:
		major = 4.0

	# Convert the GPA to a float from a strong, save it as the GPA variable
	GPA = float(applicant_data[2])

	# Divide SAT score by 400 (so it is between 0 and 4)
	# Save this variable as a float in the SAT variable
	SAT = float(applicant_data[3])/400

	# Add the four variables above and return this value
	applicant_heurisitc = university + major + GPA + SAT

	return applicant_heurisitc

def sort_applicants(input_file, output_file):
	# Open the input file
	input_file = open(input_file, "r")
	# Initialize a list
	applicant_list = list()

	# Iterate over the input file
	for line in input_file:
		# Split the applicant data by commas
		applicant_data_arr = line.split(",")
		# Calculate heuristic
		hueristic_val = calculate_heuristic_val(applicant_data_arr)
		# Add a tuple to the main lsit with hueristic_val as the first element
		# And the full applicant data as the second element
		applicant_list.append((hueristic_val, applicant_data_arr))

	# Close the input file (this is good practice but not totally necessary)
	input_file.close()

	# Sort the list in descending order using the reverse parameter
	applicant_list.sort(reverse=True)

	# Open the output file
	with open(output_file, 'a') as output_file:
		# Add the first 250 elements to the output file
		# Note that it needs to be in CSV format so each entry must be separated by a comma
		for x in range(250):
			output_line = str(applicant_list[x][0]) + ","
			output_line += ",".join(applicant_list[x][1])
			output_file.write(output_line)

def analyze_output(data_file):
	num_top_20_unveristy = 0
	
	num_majors_selected = [0,0,0,0]
	major_map = {"CS":0, "Math/Stat":1, "Engineering":2, "Other":3}
	
	gpa_scores = list()
	sat_scores = list()
	
	num_racial_cateogries_selected = [0,0,0,0,0]
	race_num_map = {"White":0, "Black":1, "Hispanic/Latinx":2, "Asian/Pacific Islander":3, "American Indian":4}
	num_male = 0

	data_file = open(data_file, "r")
	applicant_list = list()

	for line in data_file:
		app_data_arr = line.split(",")
		num_top_20_unveristy += 1 if app_data_arr[1] == '0' else 0
		num_majors_selected[major_map[app_data_arr[2]]] += 1
		gpa_scores.append(float(app_data_arr[3]))
		sat_scores.append(float(app_data_arr[4]))

		num_racial_cateogries_selected[race_num_map[app_data_arr[5]]] += 1
		num_male += 1 if app_data_arr[6] == "Male\n" else 0

	percent_top_20 = (float(num_top_20_unveristy)/250)*100
	percent_top_20 = round(percent_top_20, 1)
	print("Applicants from Top 20 University: " + str(percent_top_20) + "%\n")

	for x in range(len(num_majors_selected)):
		percent_major = (float(num_majors_selected[x])/250)*100
		percent_major = round(percent_major, 1)
		print(list(major_map.keys())[x] + ": " + str(percent_major) + "%")

	print("\nAverage GPA: " + str(round(np.mean(gpa_scores), 2)) + "\n")
	print("Average SAT: " + str(round(np.mean(sat_scores), 0)) + "\n")

	for x in range(len(num_racial_cateogries_selected)):
		percent_racial_cateogry = float((num_racial_cateogries_selected[x])/250)*100
		percent_racial_cateogry = round(percent_racial_cateogry, 1)
		print(list(race_num_map.keys())[x] + ": " + str(percent_racial_cateogry) + "%")

	percent_male = float(num_male)/250*100
	percent_male = round(percent_male, 1)

	percent_female = float(250-num_male)/250*100
	percent_female = round(percent_female, 1)

	print("\nMale Applicants Selected: " + str(percent_male) + "%")
	print("Female Applicants Selected: " + str(percent_female) + "%")



def main():
	sort_applicants("applicant-data.csv", "top-applicants.csv")
	analyze_output("top-applicants.csv")


if __name__ == '__main__':
	main()
	




