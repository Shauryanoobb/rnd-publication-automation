"""
    This file is to populate a local database initially with
    publications that already exist. The periodic insertion of 
    new publications will be done separately using Celery and Flask.

    This database is local and is used for testing purposes only.
    The population works fine locally. This completes step 1 of the project.

    The main database exists on the Institute server and the changes done 
    will soon be reflected there after meeting with the developers this week.
"""

# First, establish database connection
import mysql.connector

try:
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',    # replace with your username
        password='password',    # replace with your password
        database='scopus'   # replace with your database name
    )

    # Create a cursor to interact with the database
    cursor = connection.cursor()

    # Helper function to make changes for new publications
    def update_database(new_data, scopus_id):
        try:
            for entry in new_data:
                # Check if the publication already exists based on eid
                cursor.execute("SELECT * FROM publications WHERE eid = %s", (entry['eid'], ))
                existing_entry = cursor.fetchone()

                if existing_entry is None:
                    # Insert new data entry into the publications table
                    # Define the SQL query template with placeholders
                    add_pub = '''INSERT INTO publications (eid, doi, title, date, volume, pageRange, publicationType) VALUES (%s, %s, %s, %s, %s, %s, %s)'''

                    # Extract values
                    # Replace '"' with '\"' in each of them
                    eid = str(entry['eid'])
                    doi = str(entry.get('prism:doi', '#')).replace('"', '\"')
                    title = str(entry['dc:title']).replace('"', '\"')[0:255]
                    date = str(entry.get('prism:coverDate', 'NA'))[0:4]
                    volume = str(entry.get('prism:volume', '0'))
                    pageRange = str(entry.get('prism:pageRange', ''))
                    publicationType = str(entry.get('subtypeDescription', ''))
                    if publicationType == "Article":
                        publicationType = "Journal"

                    # Execute the query with the values
                    cursor.execute(add_pub, (eid, doi, title, date, volume, pageRange, publicationType))

                    # Now execute the establishment of relationship 
                    # between the new publications and the given authors
                    add_manages = '''INSERT INTO manages VALUES (%s, %s)'''
                    cursor.execute(add_manages, (eid, scopus_id))
                    print(f"New entry added: {eid}")

        except Exception as e:
            print(f"Oops! {str(e)}")

    # ******************************************************************************************************

    import requests

    # API endpoint
    url = 'https://api.elsevier.com/content/search/scopus'
    apiKey = 'YOUR_API_KEY' # insert your own API key

    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()

    for auth in authors:
        # auth is a tuple [scopus_id, name, did]
        print("Current author: ", auth[1])
        data = {
            'start': '0',
            'count': '200',
            'query': f'au-id({auth[0]})',
            'apiKey': apiKey
        }

        # Get all publications related to the current author
        response = requests.get(url, params=data)
        if response.status_code == 200:
            response = response.json()
            pub_array = response['search-results']['entry']
            update_database(new_data=pub_array, scopus_id=auth[0])
            # print(response)
        else:
            print("API response error: ", response.status_code)

    # Commit changes and close the connection
    connection.commit()
    connection.close()

except mysql.connector.Error as db_error:
    print(f"Error while connecting to MySQL: {db_error}")