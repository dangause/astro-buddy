import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
dotenv_path = os.path.abspath('../src/.env')
_ = load_dotenv(dotenv_path)
OPENAI_API_KEY  = os.environ['OPENAI_API_KEY']

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host='localhost',
    port=5433,
    user='postgres',
    database='tasks'
)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id SERIAL PRIMARY KEY,
             task TEXT NOT NULL,
             completed INTEGER,
             due_date DATE,
             completion_date DATE,
             priority INTEGER)''')

# Insert sample tasks into the tasks table
cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
               ('Finish homework', 1, '2023-05-01', None, 1))
cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
               ('Buy groceries', 0, '2023-05-03', None, 2))
cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
               ('Pay bills', 0, '2023-05-05', None, 3))
cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
               ('Clean house', 0, '2023-05-08', None, 4))
cursor.execute("INSERT INTO tasks (task, completed, due_date, completion_date, priority) VALUES (%s, %s, %s, %s, %s)",
               ('Exercise', 1, '2023-05-10', None, 5))

# Commit the changes and close the connection
conn.commit()
conn.close()
