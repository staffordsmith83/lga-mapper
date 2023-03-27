import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS poi;')
cur.execute('CREATE TABLE poi (id serial PRIMARY KEY,'
            'name varchar (30) NOT NULL,'
            'description varchar (150),'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )


# Insert data into the table

cur.execute('INSERT INTO poi (name, description)'
            'VALUES (%s, %s)',
            ('Camping spot 1',
             'This place looks sweet down by the river')
            )

cur.execute('INSERT INTO poi (name, description)'
            'VALUES (%s, %s)',
            ('Camping spot 2',
             'This place looks terrible too many flies')
            )

conn.commit()

cur.close()
conn.close()
