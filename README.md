# Research Publications Integration


## Overview

This project aims to automate the process of fetching research publications and displaying them on the Research and Development (R&D) website of the institute. Currently, publications need to be added manually to the website, which is a time-consuming process. To streamline this process, the project includes sample frontend pages designed to be integrated with the existing frontend of the current website, a Python script to fill the publications table with the help of the [Scopus API](https://dev.elsevier.com/sc_apis.html) and SQL schemas to organize the data efficiently.


## Features

- Automated fetching of research publications
- Integration with the existing R&D website frontend
- Python script for populating the publications table
- Periodic addition of new publications

## Prerequisites

Before running the Python script or integrating the frontend pages, ensure that you have the following:

- Python installed on your system
- MySQL or another compatible database management system installed
- Access to the existing R&D website frontend files and backend server

## Getting Started

### 1. Database Setup

- Use the provided SQL schemas to create the necessary tables in your database.
- Make sure your database server is running and accessible.

### 2. Python Script

- Run the provided Python script to populate the publications table with sample data.
- Customize the script to fetch publications from your preferred source or API.

### 3. Frontend Integration

- Merge the sample frontend pages with the existing frontend of the R&D website.
- Update the PHP code to fetch publications from the database and display them on the website.

## Usage

1. Run the Python script periodically to update the publications table with new data.
2. Access the R&D website to view the latest research publications.


