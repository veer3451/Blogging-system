import sqlite3

conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    likes INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blog_id INTEGER,
    text TEXT,
    FOREIGN KEY (blog_id) REFERENCES blogs(id)
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully")
