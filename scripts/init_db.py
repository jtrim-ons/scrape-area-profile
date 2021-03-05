import sqlite3

if __name__ == "__main__":
    con = sqlite3.connect('cache/cache.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE cache
               (url text, html text)''')
    con.commit()
    con.close()
