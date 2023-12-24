# Flask Application with PostgreSQL Database

This repository contains a Flask application that uses a PostgreSQL database. Follow the steps below to set up and run the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Creating the PostgreSQL Database and User](#creating-the-postgresql-database-and-user)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)

## Prerequisites

Before you begin, ensure you have the following requirements installed on your machine:

- Python (version 3.10.1)
- PostgreSQL (version 15.5)

## Creating the PostgreSQL Database and User

Log in to an interactive Postgres session using the following command:

```bash
cd "C:\Program Files\PostgreSQL\15\bin"
psql -U postgres
```

You will be given a PostgreSQL prompt where you can set up your requirements.
First, create a database for your project:
```bash
CREATE DATABASE flask_db;
```

Next, create a database user for our project. Make sure to select a secure password:
```bash
CREATE USER postgres WITH PASSWORD root;
```

Then give this new user access to administer your new database:
```bash
GRANT ALL PRIVILEGES ON DATABASE flask_db TO postgres;
```

## Installation

- You will install Flask and the psycopg2 library so that you can interact with your database using Python.

- With your virtual environment activated, use pip to install Flask and the psycopg2 library:

```bash
pip install Flask psycopg2-binary
```

- Clone the repository to your local machine:

```bash
git clone https://github.com/VismayaM-2003/Flask-Application-with-PostgreSQL-Database.git
```


1. Navigate to the project directory:

```bash
cd flask_app
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS and Linux:

```bash
source venv/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Configuration


Set up a PostgreSQL database and note down the connection details (host, port, username, password, database name).

- This file will open a connection to the flask_db database, create a table called books, and populate the table using sample data. 
[init_db.py]()

Copy the .env.example file to .env and update the environment variables with your PostgreSQL connection details.

[.env: I have already set the password and username in .env file, so no need to set it.]()

-For the database connection to be established, set the DB_USERNAME and DB_PASSWORD environment variables by running the following commands. Remember to use your own username and password:

- On Windows:

```bash
set DB_USERNAME=postgres
set DB_PASSWORD=root
```

- Log in to an interactive Postgres session to check out the new books table.
```bash
sudo -iu postgres psql
```

- Connect to the flask_db database using the \c command:

```bash
postgres# \c flask_db
```

- You can navigate to the codes then run the Applicatin.

## Usage

Run the Flask application:

```bash
python app.py 
```
or

```bash
flask run
```
- Open your web browser and navigate to http://localhost:5000 to access the application.


## Contributing

If you'd like to contribute to this project, please follow these guidelines:

Fork the repository.

Create a new branch:

```bash
git checkout -b feature/new-feature
```

Make your changes and commit them:

```bash
git commit -m "Add new feature"
```

Push to the branch:

```bash
git push origin feature/new-feature
```

Create a pull request.






