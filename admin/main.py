from flask import Flask, render_template
from data import db_session
from data.products import Product
import csv

app = Flask(__name__, template_folder=".")
app.config['SECRET_KEY'] = 'baker_admin_secret_key'

with open('csv_files/products.csv', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    products = list(reader)


db_session.global_init("db/assortment.db")

db_sess = db_session.create_session()
product = db_sess.query(Product).all()


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('index.html', product=product)


def main():
    app.run()


if __name__ == '__main__':
    main()