from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine, text
import pandas as pd
app = Flask(__name__)
db_name = 'database'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'db'
db_port = '5432'

app.debug = True
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)


def get_values():
    global db_string
    db = create_engine(db_string)
    conn = db.connect()
    res = conn.execute(text("SELECT * FROM numbers"))
    kek = pd.read_sql("SELECT * FROM numbers", conn)
    return kek


@app.route('/')
def show_page():
    data = get_values()
    return data.to_html()


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
