import random
import numpy as np
import csv
# WM, WF, BM, BF, HM, HF, AsM, AsF, AIM, AIF

def generate_university_acceptance(race_num):
	race_averages = [42.5, 8.9, 13.8, 26.1, 1.5]
	rand_number = random.uniform(0, 100)
	if rand_number < race_averages[race_num]:
		return 0
	else:
		return 1


def generate_rand_array_mean(desired_mean, desired_arr_length, min_val, max_val, val_type):
	generated_rand_arr = []

	while len(generated_rand_arr) < desired_arr_length:
		first_value = random.uniform(min_val, max_val)
		second_value = (desired_mean*2)-first_value

		if max_val < first_value or first_value < min_val or max_val < second_value or second_value < min_val:
			continue

		if val_type == 'int':
			first_value = int(first_value)
			second_value = int(second_value)

		generated_rand_arr.append(first_value)
		generated_rand_arr.append(second_value)

	return generated_rand_arr


def main():
	num_total_applicants = 8000
	num_applicants_in_csv = 0

	num_cs_applicants = [694, 152, 113, 25, 133, 29, 209, 46, 4, 1]
	num_math_stat_applicants = [573, 380, 46, 30, 108, 71, 137, 91, 3, 2]
	num_engineering_applicants = [773, 212, 52, 14, 137, 37, 150, 41, 4, 1]

	all_applicants = [num_cs_applicants, num_math_stat_applicants, num_engineering_applicants]
	race_categories = ["White", "Black", "Hispanic/Latinx", "Asian/Pacific Islander", "American Indian"]
	curr_race = 0
	sex_gaterories = ["Male", "Female"]
	curr_sex = 0
	major_categories = ["CS", "Math/Stat", "Engineering"]

	# Tuple for Am. Ind. as no data exists so we use M/F averages
	gpa_race = [2.88, 2.47, 2.6, 3.09, 3.0]
	sat_race = [1114, 978, 933, 1223, 912]


	with open('applicant-data.csv', 'a') as output_file:
		writer = csv.writer(output_file)
		# University, Major, GPA, SAT, Race, Gender

		for x in range(len(all_applicants)):
			for y in range(len(all_applicants[x])):
				num_desired_applicants = all_applicants[x][y]
				
				gpa_distribution = generate_rand_array_mean(gpa_race[curr_race % 5], num_desired_applicants, 2, 4, 'float')

				sat_distribution = generate_rand_array_mean(sat_race[curr_race % 5], num_desired_applicants, 200, 1600, 'int')
				major = major_categories[x]
				race = race_categories[curr_race % 5]
				sex = sex_gaterories[curr_sex % 2]

				for z in range(num_desired_applicants):
					university_acceptance = generate_university_acceptance(curr_race % 5)
					applicant_row_data = [university_acceptance, major, gpa_distribution[z], sat_distribution[z], race, sex] 
					writer.writerow(applicant_row_data)

				curr_sex += 1
				if curr_sex % 2 == 0:
					curr_race += 1

if __name__ == '__main__':
	main()

