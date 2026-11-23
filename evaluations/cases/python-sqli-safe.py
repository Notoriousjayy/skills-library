def find_user(conn, username):
    return conn.execute("SELECT * FROM users WHERE name = ?", (username,)).fetchall()
