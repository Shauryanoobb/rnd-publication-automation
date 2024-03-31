# First, establish database connection
import mysql.connector
import pandas as pd
import numpy as np


        
# # Create a cursor to interact with the database	

def department_exists(cursor, department_name):
	cursor.execute("SELECT COUNT(*) FROM department WHERE department_name = %s", (department_name,))
	count = cursor.fetchone()[0]
	return count > 0

def update_database_department(file_path):
	try:
		# Connect to MySQL database
		connection = mysql.connector.connect(
			host='localhost',
			user='root',    # replace with your username
			password='tesla@2005',    # replace with your password
			database='scopus'   # replace with your database name
		)

		# Create a cursor to interact with the database
		cursor = connection.cursor()

		# Read data from Excel sheet
		data = pd.read_excel(file_path)

		# Iterate over rows and insert data into the database
		for index, row in data.iterrows():
			department_name = row['Department']

			# Check if department already exists
			if not department_exists(cursor, department_name):
				# Insert data into the database
				cursor.execute("INSERT INTO department (department_name) VALUES (%s)",
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
				host='localhost',
				user='root',    # replace with your username
				password='tesla@2005',    # replace with your password
				database='scopus'   # replace with your database name
			)

			# Create a cursor to interact with the database
			cursor = connection.cursor()

			# Read data from Excel sheet
			data = pd.read_excel(file_path)

			# Iterate over rows and insert data into the database
			for index, row in data.iterrows():
				# Extract values from the DataFrame
				scopus_id = row['Scopus_ID']
				if scopus_id is None or pd.isnull(scopus_id): continue
				name = row['First_Name'] + " " + row['Last_Name']
				department_name = row['Department']

				# Insert data into the database
				cursor.execute("INSERT INTO authors (scopus_id, name, department_name) VALUES (%s, %s, %s)",
							(scopus_id, name, department_name))

			# Commit changes to the database
			connection.commit()

			# Close cursor and connection
			cursor.close()
			connection.close()

			print("Data successfully updated in the authors database.")

		except mysql.connector.Error as db_error:
			print(f"Error while connecting to MySQL: {db_error}")


update_database_department("authors.xlsx")
update_database("authors.xlsx")
