import json
import sqlite3

# データベース初期化
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# テーブルを初期化
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# JSONファイル読み込み
fname = '/Users/wanakahideyuki/Library/Mobile Documents/com~apple~CloudDocs/仕事/ml-study-roadmap/roster/roster_data.json'  # 自分のファイル名に合わせてください
with open(fname) as f:
    data = json.load(f)

# データは三重構造のリスト: [ [ユーザ名, コース名, 役割], ... ]
for entry in data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    # UserとCourseを登録（なければ挿入）
    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name,))
    cur.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (title,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (title,))
    course_id = cur.fetchone()[0]

    # Memberに登録（役割も含めて）
    cur.execute('''
        INSERT OR REPLACE INTO Member (user_id, course_id, role)
        VALUES (?, ?, ?)''', (user_id, course_id, role))

# データ保存
conn.commit()