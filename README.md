# fast_api_demo
1) git clone https://github.com/krishakalariya/fast_api_demo.git
2) cd your-repository
3) pip install -r requirements.txt
4) # Create the PostgreSQL database
    createdb your_database_name
    # Create a new user
    createuser --interactive --pwprompt
    # Enter a username and password for the new user
    # Grant necessary permissions to the user
    psql your_database_name
    GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
5) create .env file and add DATABASE_URL=postgresql://username:password@localhost:5432/databasename
6) uvicorn main:app --reload
7) hit http://127.0.0.1:8000/docs.
