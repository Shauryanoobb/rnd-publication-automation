# Research Publications Integration


## Overview

This project aims to automate the process of fetching research publications and displaying them on the Research and Development (R&D) website of the institute. Currently, publications need to be added manually to the website, which is a time-consuming process. To streamline this process, the project includes sample frontend pages designed to be integrated with the existing frontend of the current website, a Python script to fill the publications table with the help of the [Scopus API](https://dev.elsevier.com/sc_apis.html) and SQL schemas to organize the data efficiently.


## Features

- Automated fetching of research publications
- Integration with the existing R&D website frontend
- Python script for populating the publications table
- Periodic addition of new publications

<p align='center'><b>Current Research and Development Website</b></p>
<img style='display: none;' src='https://github.com/Shauryanoobb/rnd-publication-automation/blob/main/screenshots/existing_page.jpg'>

<p align = 'center'><b>Sample PHP page displaying the database content after population with Python</b></p>
<img src='https://github.com/Shauryanoobb/rnd-publication-automation/blob/main/screenshots/pagination.png'>
<img src='https://github.com/Shauryanoobb/rnd-publication-automation/blob/main/screenshots/final_page_with_affiliations.jpg'>
<img src='https://github.com/Shauryanoobb/rnd-publication-automation/blob/main/screenshots/batch_processing.jpg'>

### Remarks
The current website consists of $6303$ records that were added manually till date. After fetching all publications of an author (up to $200$ per faculty member), there are now $6814$ records in the new tables, considering those affiliated with IIT Indore only. Otherwise, a total of more than $11000$ publications were fetched as shown.

## Prerequisites

Before running the Python script or integrating the frontend pages, ensure that you have the following:

- [Python](https://python.org/downloads) and [Apache](https://www.apachefriends.org/) (in case running the PHP site locally) installed on your system
- [MySQL](https://dev.mysql.com/downloads/installer/) installed (this is a command line version, to get the GUI version, check out [MySQL Workbench](https://dev.mysql.com/downloads/workbench/))

## Steps to Follow (Local Hosting)

This tutorial will use the **command line version** of MySQL for the database, which is pretty simple and easy to use. <br>
Moreover, a sample page shall be built using PHP and hosted using XAMPP to display the database contents. _This is for preview only._
### 0. Setting up Apache Server and Cloning this Repository
- Install XAMPP server from [here](https://apachefriends.org/).
- Move to the folder within your File Explorer where XAMPP was installed. The installation would default to `C:\xampp` on Windows.
- Open the `htdocs` folder at `C:\xampp\htdocs`. Here we will create a clone folder of this repository.
- Open the terminal in this location by right-clicking on an empty area and selecting "Open in Terminal" (on Windows).
- Run the following commands in order to clone this git repository.
  ```
  git clone https://github.com/Shauryanoobb/rnd-publication-automation.git
  cd rnd-publication-automation
  ```
- Once the cloning completes, the entire code of this repository will be available locally, access it at `C:\xampp\htdocs\rnd-publication-automation`.
  
### 1. Database Setup
- Install **MySQL Command Line Client** from [here](https://dev.mysql.com/downloads/installer).
- After the wizard takes you through the setup, you should be able to start your own local MySQL server.
- Enter your password to access the server. This password is the same as the one provided during the installation of MySQL.
- Run the following command to create a new database called `scopus`. This will be our main database in this project.
  ```
  CREATE DATABASE scopus;
  ```
- Once the database `scopus` is successfully created, run the next command to start using it.
  ```
  USE scopus;
  ```
- Copy and paste **ALL** the SQL commands from the [schema.sql](https://github.com/Shauryanoobb/rnd-publication-automation/blob/main/schema.sql) file to the command line. This will create $4$ tables in the database, which are `publications`, `department`, `authors` and `manages`.

### 2. Python Scripts
To run the given scripts, you'll need to open the terminal (bash on Linux) application in the directory `C:\xampp\htdocs\rnd-publication-automation`. <br>
Open the files `authors.py`, `populate.py`, and `periodic.py` and follow the instructions given in **each** of them. <br>
On Windows, python is invoked using the `python` command, while on Linux/Mac, you'll need to use `python3`. The same applies for `pip`/`pip3`. <br><br>
- Run the following command to install the dependencies used in the project:
  ```
  pip install -r requirements.txt
  ```
- This repository contains sample XLS files for populating the tables `authors` and `department`. To use them, run the following commands:
  ```
  python authors.py
  ```
- Filling the database with **past publications** (one-time population): run the following command. It will take a while to fetch all the past publications as the API response takes considerable amount of time.
  ```
  python populate.py
  ```
- **Periodic update:** the following command fetches only up to $10$ recent publications per author, and hence may be run with a certain frequency throughout the week.
  ```
  python periodic.py
  ```
### 3. Frontend Integration

- Open the `index.php` file and replace the variables with your database connection parameters.
- Open the XAMPP application. On Windows, you may use the Start menu to search for it.
- Start the Apache Server.
- Frontend is good to go! Go to [this link](https://localhost/rnd-publication-automation) to see the results of the database.

## Usage

1. For the first time, you'll need to just run `populate.py`. This will take a while.
2. Run `periodic.py` periodically to update the publications table with new data.
3. You may need to check the weekly quotas of your API keys obtained from [Elsevier Developer Portal.](https://dev.elsevier.com/apikey/manage)
4. Access the [R&D website](https://localhost/rnd-publication-automation) to view the latest research publications.


