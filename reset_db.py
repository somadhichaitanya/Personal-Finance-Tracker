import sqlite3

conn = sqlite3.connect('data/finance.db')
conn.execute("DELETE FROM transactions")
conn.commit()
conn.close()
print("✅ Database cleared.")
