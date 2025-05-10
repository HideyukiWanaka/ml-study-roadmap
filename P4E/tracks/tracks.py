import sqlite3
import csv

# Connect to (or create) the database
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Drop old tables and create new ones
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

# Open and read CSV file
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = '/Users/wanakahideyuki/Library/Mobile Documents/com~apple~CloudDocs/仕事/ml-study-roadmap/tracks/tracks.csv'

with open(fname, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Skip header

    for row in reader:
        if len(row) < 10:
            continue

        name = row[1]
        artist = row[2]
        album = row[3]
        genre = row[4]
        count = row[5]
        rating = row[6]
        length = row[7]

        # Skip rows with missing critical data
        if name == '' or artist == '' or album == '' or genre == '':
            continue

        # Insert or ignore artist, genre, and album
        cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
        cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
        artist_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
        cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
        genre_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
        cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
        album_id = cur.fetchone()[0]

        # Insert track
        cur.execute('''
            INSERT OR REPLACE INTO Track 
            (title, album_id, genre_id, len, rating, count) 
            VALUES (?, ?, ?, ?, ?, ?)''',
            (name, album_id, genre_id, length, rating, count))

# Commit changes
conn.commit()
print('Database built successfully!')
