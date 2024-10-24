import sqlite3

conn = sqlite3.connect('store.db')
c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS productos(
id TEXT PRIMARY KEY,
nombre TEXT NOT NULL,
descricion TEXT,
marca TEXT,
tamaño TEXT
) """)
