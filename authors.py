"""
	Welcome to authors.py!
	This file will fill the `authors` AND the `department` table with data 
	from `auth.xlsx` and `dept.xlsx` respectively. 
	Make sure to change each of them as needed.
"""

DATABASE_HOST = 'localhost'  # set to localhost if you are using an SQL database on your local machine
DATABASE_USERNAME = 'root'  # leave it as `root` if it's localhost, else mention the username
DATABASE_PASSWORD = '********'  # you know what's coming here
DATABASE_NAME = ''  # insert the name of your database

"""
	You're good to go!
"""

import mysql.connector
import pandas as pd
import numpy as np

def update_database_department(file_path):
	try:
		# Connect to MySQL database
		connection = mysql.connector.connect(
			host=DATABASE_HOST,
			user=DATABASE_USERNAME,    # replace with your username at the top of the file
			password=DATABASE_PASSWORD,    # replace with your password at the top of the file
			database=DATABASE_NAME   # replace with your database name at the top of the file
		)

		# Create a cursor to interact with the database
		cursor = connection.cursor()

		# Read data from Excel sheet
		data = pd.read_excel(file_path)

		# Iterate over rows and insert data into the database
		for index, row in data.iterrows():
			department_name = row['Department']

			# Check if department already exists
			cursor.execute("INSERT IGNORE INTO department (department_name) VALUES (%s)",
								(department_name,))

		# Commit changes to the database
		connection.commit()

		# Close cursor and connection
		cursor.close()
		connection.close()

		print("Data successfully updated in the department database.")

	except mysql.connector.Error as db_error:
		print(f"Error while connecting to MySQL: {db_error}")

def update_database(file_path):
		try:
			# Connect to MySQL database
			connection = mysql.connector.connect(
				host=DATABASE_HOST,
				user=DATABASE_USERNAME,    # replace with your username
				password=DATABASE_PASSWORD,    # replace with your password
				database=DATABASE_NAME   # replace with your database name
			)

			# Create a cursor to interact with the database
			cursor = connection.cursor()

			# Read data from Excel sheet
			data = pd.read_excel(file_path)

			# Iterate over rows and insert data into the database
			for index, row in data.iterrows():
				if pd.isnull(row['Email']):
					print("Skipping row with missing email:", row)
					continue

				email = row['Email']
				orcid_id = str(row.get('ORCID_ID', '$'))
				researcher_id = str(row.get('Researcher_ID', '$'))
				scopus_id = str(row.get('Scopus_ID', '$'))
				
				name = f'{row["First_Name"]} {row["Last_Name"]}'
				department_name = str(row.get('Department', 'Department'))
				print(email, orcid_id, researcher_id, scopus_id, name, department_name)
				# break

				# Insert data into MySQL table
				cursor.execute("INSERT INTO authors (email, orcid_id, researcher_id, scopus_id, name, department_name) VALUES (%s, %s, %s, %s, %s, %s)",
								(email, orcid_id, researcher_id, scopus_id, name, department_name))
        # break

			# Commit changes to the database
			connection.commit()

			# Close cursor and connection
			cursor.close()
			connection.close()

			print("Data successfully updated in the authors database.")

		except mysql.connector.Error as db_error:
			print(f"Error while connecting to MySQL: {db_error}")


update_database_department("auth.xlsx")
update_database("dept.xlsx")
