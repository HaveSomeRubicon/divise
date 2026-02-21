import sqlite3

DB_FILE = "divise.db"


def get_conn():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS apps (
        id INTEGER PRIMARY KEY,
        name TEXT,
        path TEXT UNIQUE
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        app_id INTEGER,
        start_time INTEGER,
        end_time INTEGER,
        FOREIGN KEY(app_id) REFERENCES apps(id)
    )
    """)

    conn.commit()
    conn.close()


def get_app_id(name, path) -> int:
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """SELECT id FROM apps WHERE path=?""",
        (path,),
    )
    row = c.fetchone()
    if row:
        app_id = row[0]
    else:
        c.execute(
            """INSERT OR IGNORE INTO apps (name, path) VALUES (?, ?)""",
            (name, path),
        )
        app_id = c.lastrowid
        conn.commit()

    conn.close()
    return app_id


def save_session(app_id: int, start_time: float, end_time: float):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """INSERT INTO sessions (app_id, start_time, end_time) VALUES (?, ?, ?)""",
        (app_id, int(start_time), int(end_time)),
    )
    conn.commit()

    conn.close()
