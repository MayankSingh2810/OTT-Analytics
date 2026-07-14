"""
============================================================
OTT STREAM INTELLIGENCE PLATFORM
Database Initialization Script
============================================================
"""

import mysql.connector
from pathlib import Path

from config import *

print("=" * 70)
print(PROJECT_NAME)
print("DATABASE INITIALIZATION")
print("=" * 70)

# ==========================================================
# CONNECT TO MYSQL SERVER
# ==========================================================

connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = connection.cursor()

print("✓ Connected to MySQL Server")

# ==========================================================
# DROP DATABASE
# ==========================================================

print("\nDropping existing database (if it exists)...")

cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")

print("✓ Old database removed")

# ==========================================================
# CREATE DATABASE
# ==========================================================

print("\nCreating database...")

cursor.execute(f"CREATE DATABASE {DB_NAME}")

print("✓ Database created")

cursor.execute(f"USE {DB_NAME}")

print(f"✓ Using database : {DB_NAME}")

# ==========================================================
# EXECUTE SCHEMA.SQL
# ==========================================================

schema_file = BASE_DIR / "database" / "schema.sql"

print("\nExecuting schema.sql...")

with open(schema_file, "r", encoding="utf-8") as file:
    sql_script = file.read()

for statement in sql_script.split(";"):

    statement = statement.strip()

    if statement:

        cursor.execute(statement)

connection.commit()

print("✓ Tables created")

# ==========================================================
# EXECUTE INDEXES.SQL
# ==========================================================

index_file = BASE_DIR / "database" / "indexes.sql"

print("\nExecuting indexes.sql...")

with open(index_file, "r", encoding="utf-8") as file:
    sql_script = file.read()

for statement in sql_script.split(";"):

    statement = statement.strip()

    if statement:

        cursor.execute(statement)

connection.commit()

print("✓ Indexes created")

# ==========================================================
# VERIFY TABLES
# ==========================================================

print("\nVerifying database...\n")

cursor.execute("SHOW TABLES")

tables = cursor.fetchall()

for table in tables:

    print(f"• {table[0]}")

print("\nTotal Tables :", len(tables))

# ==========================================================
# CLEANUP
# ==========================================================

cursor.close()

connection.close()

print("\n" + "=" * 70)
print("DATABASE INITIALIZATION COMPLETED SUCCESSFULLY")
print("=" * 70)