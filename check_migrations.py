import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check migrations table
cursor.execute('SELECT id, app, name FROM django_migrations WHERE app=? ORDER BY id DESC', ('admin_panel',))
rows = cursor.fetchall()

print("Admin Panel Migrations in Database:")
print("-" * 50)
for row in rows:
    print(f"ID: {row[0]}, Name: {row[2]}")

conn.close()
