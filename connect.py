import os
import psycopg2

print(os.getenv('dbname'))
if os.getenv('FLASK_CONFIG') == "development":
    conn = psycopg2.connect(dbname=os.getenv('dbname'), user=os.getenv('user'), password=os.getenv('password'))
elif os.getenv('FLASK_CONFIG') == "testing":
    conn = psycopg2.connect(dbname='testdb', user=os.getenv('user'), password=os.getenv('password'))
else:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
try:
    # Connect to our db
    conn

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

