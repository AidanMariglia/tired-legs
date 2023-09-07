import sqlite3
import os
import click
import typing

from pathlib import Path
from flask import current_app, g
from .utils import get_data


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# open doesn't return the right type
def init_db(db: sqlite3.Connection, schema: str):
    db.executescript(schema)

    populate_data(db)


@click.command('init-db')
def init_db_command():
    """clear existing data and create new tables"""
    with current_app.open_resource('schema.sql') as f:
        s = f.read().decode('utf-8')
        init_db(get_db(), s)
    click.echo("initiliazed the db")


def clean_street(street: str) -> str:
    street = street.lower()
    street = street.replace(" ", "")
    street = street.replace(".", "")
    street = street.replace(",", "")

    return street


def populate_data(db: sqlite3.Connection):
    INSERT_STRING = 'INSERT INTO bench (address_number, address_street, side, search_street) VALUES(?, ?, ?, ?)'
    benches = get_data.get_benches()
    cursor = db.cursor()

    data = [(bench[3], bench[4], bench[6], clean_street(bench[4])) for bench in benches]
    for entry in data:
        print(entry)
    cursor.executemany(INSERT_STRING, data)
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_bench_data(db: sqlite3.Connection, id: int) -> typing.Tuple[int, str, str, str, str]:
    res = db.execute("SELECT * FROM bench WHERE id=?;", (str(id),))
    res_row = res.fetchone()
    return res_row[:]


def get_bench_data_by_street(db: sqlite3.Connection, street: str) -> typing.List[typing.Tuple[int, str, str, str, str]]:
    res = db.execute("SELECT address_number, address_street from bench WHERE search_street LIKE (? || '%');", (street,))
    return res


def main():
    db = sqlite3.connect(
        os.path.join(os.getcwd(), 'tired_legs.sqlite'),
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row

    p = Path(__file__).with_name('schema.sql')
    with p.open('r') as f:
        s = f.read()
        init_db(db, s)

    print(get_bench_data(db, 2))


# init db for testing
if __name__=="__main__":
    main()