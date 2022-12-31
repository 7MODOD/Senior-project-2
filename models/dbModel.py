import sqlite3


def execute(query,array, fetchone: bool | None = False):
    conn = sqlite3.connect('IMAGES.db')
    conn.text_factory = bytes
    cursor = conn.cursor()

    cursor.execute(query,array)
    if fetchone is True:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return result
