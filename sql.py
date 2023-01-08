import sqlite3


def result(num):
    con = sqlite3.connect("result")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM result1""").fetchall()

    c = []
    if result[0][0] < num:
        cur.execute(f"""UPDATE result1
                    SET result = {num}
                    WHERE id = 1""").fetchall()
    con.commit()
    con.close()
    return result[0][0]

