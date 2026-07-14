from database.connection import get_connection

print("=" * 60)

conn = get_connection()

print("Connection Successful!")

cursor = conn.cursor()

cursor.execute("SELECT VERSION();")

print(cursor.fetchone())

cursor.close()
conn.close()

print("=" * 60)