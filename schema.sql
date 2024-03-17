-- This is the SQL file that specifies the schema of the new tables 
-- introduced for the sake of automation. Once successful, the 
-- existing tables regarding publications will be discontinued
-- and these will be used. 

CREATE TABLE publications(
    eid VARCHAR(255) PRIMARY KEY,   -- this is the unique ID in our table
    doi VARCHAR(255),   -- unique ID that is used in scopus database
    title VARCHAR(255),
    date VARCHAR(255),  -- stores the year of publication
    volume VARCHAR(255) DEFAULT '',
    pageRange VARCHAR(255) DEFAULT '',
    publicationType VARCHAR(255) DEFAULT 'Journal'
);  

CREATE TABLE department(
    department_name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE authors(
    scopus_id VARCHAR(255) PRIMARY KEY,   -- scopus ID of the author
    name VARCHAR(255),
    department_name VARCHAR(255) DEFAULT 'Department',  -- department name
    FOREIGN KEY (department_name) REFERENCES department(department_name) ON DELETE CASCADE
);

-- creating a table to state the relation between a single publication and its related authors
CREATE TABLE manages(
    eid VARCHAR(255),
    scopus_id VARCHAR(255),
    PRIMARY KEY (eid, scopus_id),
    FOREIGN KEY (eid) REFERENCES publications(eid) ON DELETE CASCADE,
    FOREIGN KEY (scopus_id) REFERENCES authors(scopus_id) ON DELETE CASCADE
);