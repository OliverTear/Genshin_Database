import sqlite3

def main():
    print("Hello from genshin-database!")
    dbname = "genshin.db"
    conn = sqlite3.connect(dbname)
    conn.close()

if __name__ == "__main__":
    main()
