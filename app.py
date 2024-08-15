import os
import psycopg2
from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

uri = "mongodb+srv://bilelelleuch96:<password>@cluster0.qdq3p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

pg_conn = psycopg2.connect(
    host=os.environ.get('POSTGRES_HOST'),
    database=os.environ.get('POSTGRES_DB'),
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASS')
)

mongo_client = MongoClient(os.environ.get('MONGO_URI'))
mongo_db = mongo_client['your_mongo_database']

@app.route('/')
def home():
  return 'Hello from Flask python!'

@app.route('/test-postgres')
def test_postgres():
    try:
        cur = pg_conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        return f"Connected to PostgreSQL: {db_version[0]}"
    except Exception as e:
        return f"Failed to connect to PostgreSQL: {str(e)}"
    finally:
        cur.close()

@app.route('/test-mongo')
def test_mongo():
    try:
        db_list = mongo_client.list_database_names()
        return f"Connected to MongoDB: Databases - {db_list}"
    except Exception as e:
        return f"Failed to connect to MongoDB: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
