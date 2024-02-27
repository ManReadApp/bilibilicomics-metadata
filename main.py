import json
import sqlite3

import requests


def generate_url(ident: int):
    return "https://www.bilibilicomics.com/detail/mc" + str(ident)


def check(ident: int) -> tuple[int, str, int, str, str, str, str, str, str, int, int, str]:
    url = 'https://www.bilibilicomics.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web&lang=en&sys_lang=en' \
        # url = 'https://www.bilibilicomics.com/twirp/comic.v1.Comic/ComicDetail'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    data = '{"comic_id":' + str(ident) + '}'

    response = requests.post(url, headers=headers, data=data)
    respjson = response.json()
    code = respjson['code']
    title = str(ident)
    lang = ''
    cover = ''
    banner = ''
    authors = []
    styles = []
    tags = []
    is_finish = 0
    status = 0
    evaluate = ""

    if code == 0:
        lang = '-' + respjson['data']['language']
        title = respjson['data']['title']
        cover = respjson['data']['vertical_cover']
        banner = respjson['data']['horizontal_cover']
        authors = respjson['data']['author_name']
        styles = respjson['data']['styles']
        tags = respjson['data']['tags']
        is_finish = respjson['data']['is_finish']
        status = respjson['data']['status']
        evaluate = respjson['data']['evaluate']
    else:
        save_error(ident, code)
        raise Exception
    return ident, title, code, lang, cover, banner, json.dumps(authors), json.dumps(styles), json.dumps(
        tags), is_finish, status, evaluate


def process_range(start, end):
    for ident in range(start, end):
        try:
            data = check(ident)
            save_successful_data(data)
        except:
            pass


def create_tables():
    conn = sqlite3.connect('bilibilicomics.db')
    cursor = conn.cursor()

    # Create table for successful data
    cursor.execute('''CREATE TABLE IF NOT EXISTS successful_data (
                        ident INTEGER PRIMARY KEY,
                        title TEXT,
                        code INTEGER,
                        lang TEXT,
                        cover TEXT,
                        banner TEXT,
                        authors TEXT,
                        styles TEXT,
                        tags TEXT,
                        is_finish INTEGER,
                        status INTEGER,
                        evaluate TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS error_data (
                            ident INTEGER PRIMARY KEY, code INTEGER
                        )''')

    conn.commit()
    conn.close()


def save_successful_data(data):
    conn = sqlite3.connect('bilibilicomics.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO successful_data 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()


def save_error(ident, status):
    conn = sqlite3.connect('bilibilicomics.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO error_data 
                      VALUES (?, ?)''', (ident, status))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
    process_range(1, 4000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
