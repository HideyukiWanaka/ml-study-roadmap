import sqlite3
import csv

# SQLiteデータベースに接続
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# テーブル初期化
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# ファイル名の入力（デフォルト）
fname = '/Users/wanakahideyuki/Library/Mobile Documents/com~apple~CloudDocs/仕事/ml-study-roadmap/tracks/tracks.csv'
if len(fname) < 1:
    fname = 'tracks.csv'

with open(fname, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        if len(row) < 7:
            continue

        # 列の対応（0ベース）
        title = row[0]
        artist = row[1]
        album = row[2]
        count = row[3]
        rating = row[4]
        length = row[5]
        genre = row[6]

        if title == '' or artist == '' or album == '' or genre == '':
            continue

        # Artist登録とID取得
        cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
        cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
        artist_id = cur.fetchone()[0]

        # Genre登録とID取得
        cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
        cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
        genre_id = cur.fetchone()[0]

        # Album登録とID取得
        cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
        cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
        album_id = cur.fetchone()[0]

        # Track登録
        cur.execute('''
            INSERT OR REPLACE INTO Track 
            (title, album_id, genre_id, len, rating, count) 
            VALUES (?, ?, ?, ?, ?, ?)''',
            (title, album_id, genre_id, length, rating, count))

# データ保存
conn.commit()
print("Database 'trackdb.sqlite' created successfully.")