import os
import psycopg2

print(os.getenv('dbname'))
conn = psycopg2.connect(dbname=os.getenv('dbname'), user=os.getenv('user'), password=os.getenv('password'))
try:
    # Connect to our db
    conn

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

