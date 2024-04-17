"""
    Welcome to periodic.py!
    This file will fill your database with publications, those which belong to the 
    all the authors mentioned in the file `auth.xlsx`.

    This file is intended to be executed once in every week (or as needed.)

    Necessary settings are mentioned below. Set them up in order to get the application running.
"""

YOUR_API_KEY = '7f59af901d2d86f78a1fd60c1bf9426a'   # insert your own API key. created on https://dev.elsevier.com/apikey/manage
DATABASE_HOST = 'localhost'  # set to localhost if you are using an SQL database on your local machine
DATABASE_USERNAME = 'root'  # leave it as `root` if it's localhost, else mention the username
DATABASE_PASSWORD = '********'  # you know what's coming here
DATABASE_NAME = ''  # insert the name of your database

"""
    You're good to go!
"""

import requests, mysql.connector

# Helper function to get all the co-authors of a particular publication, 
# given the Scopus eid. This function also returns whether IIT Indore is within the list of 
# affiliation or not.
def getScopusCoAuthors(eid, iiti_author_exists):
    api_url = f"https://api.elsevier.com/content/abstract/eid/{eid}?apiKey={YOUR_API_KEY}&httpAccept=application/json"

    try:
        # Make the HTTP GET request for co-authors
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()
        # print(data)

        # Extract co-authors from the response
        co_authors = []
        authors_data = data.get('abstracts-retrieval-response', {}).get('authors', {}).get('author', [])
        for author in authors_data:
            co_authors.append(author.get('ce:indexed-name', ''))
        
        # Extract the affiliations of all the authors
        affilnames = []
        affiliation_data = data.get("abstracts-retrieval-response", {}).get("affiliation")

        # Check if affiliation_data is a list or a single dictionary
        if isinstance(affiliation_data, list):
            # If it's a list, iterate over each affiliation dictionary
            for affiliation in affiliation_data:
                if isinstance(affiliation, dict) and "affilname" in affiliation:
                    affilnames.append(affiliation["affilname"])
                elif isinstance(affiliation, str):
                    affilnames.append(affiliation)
        elif isinstance(affiliation_data, dict):
            # If it's a single dictionary, directly extract the affiliation name
            if "affilname" in affiliation_data:
                affilnames.append(affiliation_data["affilname"])

        # Check if IIT Indore is in the list of affilations, if not then we ignore it
        iiti_author_exists[0] = "Indian Institute of Technology Indore" in affilnames
        
        return ', '.join(co_authors)

    except requests.exceptions.RequestException as e:
        print(f"Error accessing Scopus API: {e}")
        return ""  # Return empty string in case of an error

# Function to insert a new record into the tables `publications` and `manages`
def insertScopusData(connection, new_data, email):
    cursor = connection.cursor()
    for entry in new_data:
        try:
            # Define the SQL query template with placeholders
            add_pub = '''INSERT IGNORE INTO publications (
                            eid, 
                            doi, 
                            title, 
                            date, 
                            volume, 
                            pageRange, 
                            publicationType, 
                            co_authors
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s
                    )'''

            # Extract values
            # Replace '"' with '\"' in each of them
            eid = str(entry['eid'])
            doi = str(entry.get('prism:doi', '#')).replace('"', '\"')
            title = str(entry['dc:title']).replace('"', '\"')[0:255]
            date = str(entry.get('prism:coverDate', 'NA'))[0:4]
            volume = str(entry.get('prism:volume', '0'))
            pageRange = str(entry.get('prism:pageRange', ''))
            publicationType = str(entry.get('subtypeDescription', ''))
            iiti_author_exists = [False]    # set this array = [True] if you don't want an Institute check
            co_authors = getScopusCoAuthors(eid=eid, iiti_author_exists=iiti_author_exists)
            if publicationType == "Article" or publicationType == "Erratum":
                publicationType = "Journal"

            # Execute the query for the publications table
            if iiti_author_exists[0] == True and int(date) >= 2008:
                cursor.execute(add_pub, (eid, doi, title, date, volume, pageRange, publicationType, co_authors))

                # Now execute the establishment of relationship 
                # between the new publications and the given authors, using the manages table
                add_manages = '''INSERT IGNORE INTO manages VALUES (%s, %s)'''
                cursor.execute(add_manages, (eid, email))
                print(f"Entry processed: {eid}")
        
        except Exception as e:
            print(f"SQL INSERT error: {str(e)}")

def updateViaScopusAPI(connection):
    cursor = connection.cursor()
    # API endpoint
    url = 'https://api.elsevier.com/content/search/scopus'
    apiKey = YOUR_API_KEY # insert your own API key at the top of the file

    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()

    for auth in authors:
        # auth is a tuple [email, orcid_id, researcher_id, scopus_id, name, department_name]
        scopus_id_list = str(auth[3]).strip().split(";")    # some faculty members may have multiple Scopus IDs

        if scopus_id_list.__len__() == 0:
            print("Author has no Scopus ID(s)")
            continue

        for scopus_id in scopus_id_list:
            print("Current author:", auth[4])

            # Get all publications related to the current author in batches of 200
            data = {
                'start': 0,
                'count': 10,    # retrieve up to 10 records per week, per Scopus ID
                'query': f'au-id({scopus_id})',
                'apiKey': apiKey
            }

            response = requests.get(url, params=data)
            if response.status_code == 200:
                response = response.json()
                pub_array = response['search-results'].get('entry', [])
                if len(pub_array) == 0:
                    print("Exit due to 0 length")
                    break
                insertScopusData(connection=connection, new_data=pub_array, email=auth[0])
            else:
                print("API error:", response.json()['service-error']['status']['statusCode'])
                break
        # break
        # Enable the above break statement to process only the first author

    # Commit changes (all changes are committed at once, so if there is any failure, all of the changes are lost)
    connection.commit()

def main():
    try:
        # Connect to local MySQL database
        connection = mysql.connector.connect(
            host=DATABASE_HOST, # replace your database host at the top of the file
            user=DATABASE_USERNAME,    # replace your username at the top of the file
            password=DATABASE_PASSWORD,    # replace your password at the top of the file
            database=DATABASE_NAME   # replace your database nameat the top of the file
        )

        updateViaScopusAPI(connection=connection)
        print("Connection status:", connection.is_connected())
        connection.close()
    
    except Exception as e:
        print("MySQL DB error:", str(e))
    
if __name__ == '__main__':
    main()