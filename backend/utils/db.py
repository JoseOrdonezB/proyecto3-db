import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='proyecto4',
        user='js103',
        password='_ElBichoSql7_'
    )
    return conn