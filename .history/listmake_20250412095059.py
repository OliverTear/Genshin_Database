import sqlite3

dbname = 'genshin.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()


cur.execute('INSERT INTO ArtifactList(name) values("Taro")')


conn.commit()

cur.close()
conn.close()