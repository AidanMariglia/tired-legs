import logging

from flask import Blueprint, render_template, request
from .db import get_db, get_bench_data, clean_street, get_bench_data_by_street

logging.basicConfig(level=logging.INFO)

bp = Blueprint('main', __name__)

# logger = app.logger

# provide two modes, one where all the data is preloaded
# in a db, another where we make a live request
@bp.route("/", methods=('GET', 'POST'))
def get_address():
    if request.method == 'POST':
        street_name = request.form["street"]
        # logger.info(f"Recieved a request for %s", street_name)
        print(f"Recieved a request for %s", street_name)

        db = get_db()

        street_cleaned = clean_street(street_name)
        
        res = get_bench_data_by_street(db, street_cleaned)

        # for row in res:
        #     print(f"{row[0]}, {row[1]}")
        
        # use the street name to make an api request,
        # then return the properly formated data

        return render_template('showAddress.html', res=[f"{b[0]}, {b[1]}" for b in res])

    return render_template('getAddress.html')


# use this to find bench record
@bp.route('/bench/<int:id>', methods=("GET",))
def get_bench(id: int):
    print(f"Selecting bench with id={id}")
    db = get_db()

    row = get_bench_data(db, id)


    return f"{row}"
