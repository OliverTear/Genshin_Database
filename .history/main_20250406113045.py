import sqlite3

def main():
    print("Hello from genshin-database!")
    # genshin.dbを作成する
    # すでに存在していれば、それにアスセスする。
    dbname = "genshin.db"
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # personsというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute('CREATE TABLE persons(id INTEGER PRIMARY KEY AUTOINCREMENT,name STRING)')

    conn.close()

if __name__ == "__main__":
    main()
