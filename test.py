# this is a testing file to measure the accuracy of the solution

import requests
import mysql.connector
import pandas as pd

def insertTestResults(connection):
    cursor = connection.cursor()
    # API endpoint
    url = 'https://api.elsevier.com/content/search/scopus'
    apiKey = 'd2593387abb4a1af3002b66979fb5e5d' # insert your own API key

    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()

    # Create an empty list to store data
    data = []

    for auth in authors:
        scopus_id_list = str(auth[3]).split(";")
        count = 0

        print("Current author:", auth[4], end=' ')
        for scopus_id in scopus_id_list:
            params = {
                'start': 0,
                'count': 1,
                'query': f'au-id({scopus_id})',
                'apiKey': apiKey
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                response = response.json()
                count += int(response['search-results']['opensearch:totalResults'])
            else:
                print("API error:", response.json()['service-error']['status']['statusCode'])

        print(count)
        
        # Append data to the list
        data.append({
            "name": auth[4],
            "email": auth[0],
            "total_publications_found": count
        })

    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Write DataFrame to Excel file
    df.to_excel("test.xlsx", index=False)

    # Commit changes
    connection.commit()

def main():
    try:
        # Connect to local MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',    # replace with your username
            password='password',    # replace with your password
            database='scopus'   # replace with your database name
        )

        insertTestResults(connection=connection)
        connection.close()
    
    except Exception as e:
        print("MySQL DB error:", str(e))
    
if __name__ == '__main__':
    main()
