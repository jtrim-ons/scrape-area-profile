import requests
import sqlite3

from bs4 import BeautifulSoup

def get_page_from_cache(url):
    con = sqlite3.connect('cache/cache.db')
    cur = con.cursor()
    cur.execute('SELECT html FROM cache WHERE url=?', (url,))
    result = cur.fetchone()
    con.close()
    return None if result is None else result[0]

def get_page(url):
    cached_page = get_page_from_cache(url)
    if cached_page is not None:
        return cached_page
    html = requests.get(url).text
    con = sqlite3.connect('cache/cache.db')
    cur = con.cursor()
    cur.execute('INSERT INTO cache values (?,?)', (url, html))
    con.commit()
    con.close()
    return html

def parse_html(html):
    result = []
    soup = BeautifulSoup(html, "html.parser")
    trs = soup.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds) == 3:
            strings = [td.string for td in tds]
            result.append(strings)
    return result

if __name__ == "__main__":
    with open("input/start-url.txt", "r") as f:
        for line in f.readlines():
            url = line.strip()
            page_html = get_page(url)
            print(url.split("/"))
            with open("pages/{}.html".format(url.split("/")[-2]), "w") as f:
                f.write(page_html)
            data = parse_html(page_html)
            print(data)
