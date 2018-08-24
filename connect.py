import os
import psycopg2

conn = psycopg2.connect(dbname=os.getenv('dbname'), user=os.getenv('user'), password=os.getenv('password'))


try:
    conn

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

