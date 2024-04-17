-- This is the SQL file that specifies the schema of the new tables 
-- introduced for the sake of automation. Once successful, the 
-- existing tables regarding publications will be discontinued
-- and these will be used. 

-- Changes after the first iteration: added email and other IDs for 
-- improved search filters by email and possibly use of multiple APIs 

CREATE TABLE publications(
    eid VARCHAR(255) PRIMARY KEY,   -- this is the unique ID in our table
    doi VARCHAR(255),   -- unique ID that is used in scopus database
    title VARCHAR(255),
    date VARCHAR(255),  -- stores the year of publication
    volume VARCHAR(255) DEFAULT '',
    pageRange VARCHAR(255) DEFAULT '',
    publicationType VARCHAR(255) DEFAULT 'Journal',
    co_authors TEXT
);  

CREATE TABLE department(
    department_name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE authors(
    email VARCHAR(255) PRIMARY KEY,
    orcid_id VARCHAR(255),   -- ORCiD ID of the author
    researcher_id VARCHAR(255),   -- researcher ID of the author
    scopus_id VARCHAR(255),   -- scopus ID of the author
    name VARCHAR(255),
    department_name VARCHAR(255) DEFAULT 'Department',  -- department ID
    FOREIGN KEY (department_name) REFERENCES department(department_name) ON DELETE CASCADE
);

-- creating a table to state the relation between a single publication and its related authors
CREATE TABLE manages(
    eid VARCHAR(255),
    email VARCHAR(255),
    PRIMARY KEY (eid, email),
    FOREIGN KEY (eid) REFERENCES publications(eid) ON DELETE CASCADE,
    FOREIGN KEY (email) REFERENCES authors(email) ON DELETE CASCADE
);