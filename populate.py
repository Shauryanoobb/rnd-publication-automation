import mysql.connector
import requests

# Function to update the database with new publications


def update_database(new_data, scopus_id, cursor):
    try:
        for entry in new_data:
            # Check if the publication already exists based on eid
            cursor.execute(
                "SELECT * FROM publications WHERE eid = %s", (entry['eid'], ))
            existing_entry = cursor.fetchone()

            if existing_entry is None:
                # Insert new data entry into the publications table
                add_pub = '''INSERT INTO publications (eid, doi, title, date, volume, pageRange, publicationType) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                # Extract values
                eid = str(entry['eid'])
                doi = str(entry.get('prism:doi', '#')).replace('"', '\"')
                title = str(entry['dc:title']).replace('"', '\"')[:255]
                date = str(entry.get('prism:coverDate', 'NA'))[:4]
                volume = str(entry.get('prism:volume', '0'))
                pageRange = str(entry.get('prism:pageRange', ''))
                publicationType = str(entry.get('subtypeDescription', ''))
                if publicationType == "Article":
                    publicationType = "Journal"

                # Execute the query with the values
                cursor.execute(add_pub, (eid, doi, title, date,
                               volume, pageRange, publicationType))

            # Establish relationship between the new publications and the given authors
            add_manages = '''INSERT INTO manages VALUES (%s, %s)'''
            eid = str(entry['eid'])
            cursor.execute(add_manages, (eid, scopus_id))
            print(f"New entry added: {eid} for author: {scopus_id}")

    except Exception as e:
        print(f"Oops! {str(e)}")


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

    # API endpoint and key
    url = 'https://api.elsevier.com/content/search/scopus'
    apiKey = 'd2593387abb4a1af3002b66979fb5e5d'  # insert your own API key

    # Retrieve authors from the database
    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()

    for auth in authors:
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
            update_database(new_data=pub_array,
                            scopus_id=auth[0], cursor=cursor)
        else:
            print("API response error: ", response.status_code)

    # Commit changes and close the connection
    connection.commit()
    connection.close()

except mysql.connector.Error as db_error:
    print(f"Error while connecting to MySQL: {db_error}")
