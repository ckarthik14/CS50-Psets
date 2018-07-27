import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    return render_template("index.html")


@app.route("/articles", methods=["GET"])
def articles():
    """Look up articles for geo"""

    geo = request.args.get("geo")

    # check for empty input
    if geo != "":
        feeds = lookup(geo)
        return jsonify(feeds)

    else:
        raise RuntimeError("No Argument Given")


@app.route("/search", methods=["GET"])
def search():
    """Search for places that match query"""

    args1 = []
    args2 = []
    q = request.args.get("q")
    res1 = []
    rows = []
    res2 = []

    if q != "":

        # check if query is postal code
        if q.isdigit():
            q += "%"
            rows = db.execute("SELECT * FROM places WHERE postal_code LIKE :q", q=q)

        else:

            if len(q.split(' ')) == 2 and ',' not in q:
                rows = db.execute("SELECT * FROM places WHERE place_name LIKE :q", q=q)

            if ' ' in q:
                args1 = re.split(', | |,', q)
                args2 = args1[:]
                res1 = args1
                res2 = args2

                print(res1)

                if len(res2) > 2:
                    res2[0] = res2[0] + ' ' + res2[1]
                    del res2[1]
                    res2 = [item.strip(",") for item in args2]

                else:
                    del res2[:]

            else:
                res1.append(q)

            for i in range(len(res1)):
                res1[i] = '%' + res1[i] + '%'

            for i in range(len(res2)):
                res2[i] = '%' + res2[i] + '%'

            if len(res1) == 1:
                rows += db.execute("SELECT * FROM places WHERE place_name LIKE :r0 \
                OR admin_name1 LIKE :r0", r0=res1[0])

            elif len(res1) == 2:
                rows += db.execute("SELECT * FROM places WHERE place_name LIKE :r0 AND \
                (admin_name1 LIKE :r1 OR admin_code1 LIKE :r1)", r0=res1[0], r1=res1[1])

            elif len(res1) == 3:
                rows += db.execute("SELECT * FROM places WHERE place_name LIKE :r0 AND (admin_name1 \
                LIKE :r1) AND (admin_code1 LIKE :r2 \
                OR country_code LIKE :r2)", r0=res1[0], r1=res1[1], r2=res1[2])

            if len(res2) == 2:
                rows += db.execute("SELECT * FROM places WHERE place_name LIKE :r0 AND \
                (admin_name1 LIKE :r1 OR admin_code1 LIKE :r1)", r0=res2[0], r1=res2[1])

            elif len(res2) == 3:
                rows += db.execute("SELECT * FROM places WHERE place_name LIKE :r0 AND (admin_name1 \
                LIKE :r1) AND ((admin_code1 LIKE :r2) \
                OR country_code LIKE :r2)", r0=res2[0], r1=res2[1], r2=res2[2])

        if len(rows) == 0:
            raise RuntimeError("No city found")
            return jsonify([])

        return jsonify(rows)

    else:
        raise RuntimeError("No Argument Given")
        return jsonify([])


@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
