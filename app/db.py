import time
import requests
from datetime import datetime
from googlesheet import GoogleSheet
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
time.sleep(0.5)
db_name = 'database'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'db'
db_port = '5432'
meta_data = MetaData()
numbers = Table('numbers', meta_data,
                Column('Id', Integer, nullable=True),
                Column('order_id', Integer, nullable=True),
                Column('dollar_price', Integer, nullable=True),
                Column('date', DateTime, nullable=True),
                Column('ruble_price', Integer, nullable=True))
# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
conn = db.connect()
meta_data.create_all(db)


# parse price
def check_course():
    usd_to_ruble = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    value = usd_to_ruble['Valute']['USD']['Value']
    return value


def check_equal(value1, value2):
    if value1 == value2:
        return True
    else:
        return False


def correct_data_format(values):
    values = values
    usd_price = check_course()
    for sp in values:
        for i in range(len(sp) - 1):
            sp[i] = int(sp[i])
        print(sp[3])
        sp[3] = datetime.strptime(sp[3], '%d.%m.%Y')
        sp.append(int(sp[2] * usd_price))
    return values


def insert_values(values):
    global numbers
    for el in values:
        ins = numbers.insert().values(Id=el[0], order_id=el[1], dollar_price=el[2], date=el[3], ruble_price=el[4])
        ins.compile().params
        res = conn.execute(ins)


if __name__ == '__main__':
    print('Application started')

    data = GoogleSheet()
    test_range = 'List1!A:D'
    values = data.show_range_value(test_range)
    values.pop(0)
    correct_values = correct_data_format(values)
    insert_values(correct_values)

    while True:
        data2 = GoogleSheet()
        test_range = 'List1!A:D'
        values2 = data.show_range_value(test_range)
        values2.pop(0)
        if values2 != values:
            db.execute(text("DELETE FROM numbers"))
            correct_values2 = correct_data_format(values2)
            insert_values(correct_values2)
