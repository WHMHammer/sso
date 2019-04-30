import flask
from simplejson import dumps

import auth


@auth.cors("/get_challenge")
def get_challenge():
    form = flask.request.get_json()
    try:
        username = str(form["username"])
    except (KeyError, TypeError):
        return "{}", 400, {"Content-Type": "application/json"}

    if not(
        auth.check_username(username)
    ):
        return "{}", 400, {"Content-Type": "application/json"}

    conn = auth.connectDB()
    cur = conn.cursor()

    cur.execute(
        "select salt from users where username=%s and status=%s limit 1;",
        (username, "verified")
    )
    try:
        salt = cur.fetchone()[0]
    except TypeError:
        conn.close()
        return "{}", 404, {"Content-Type": "application/json"}

    challenge = auth.generate_salt()

    cur.execute(
        "update users set challenge=%s where username=%s;",
        (challenge, username)
    )

    conn.commit()
    conn.close()

    return dumps({
        "salt": salt,
        "challenge": challenge
    })
