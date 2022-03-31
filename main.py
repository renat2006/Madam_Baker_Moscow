from flask import Flask, render_template, url_for
from admin.data import db_session
from admin.data.products import Product
import csv

app = Flask(__name__, template_folder=".")
app.config['SECRET_KEY'] = 'baker_admin_secret_key'


db_session.global_init("admin/db/assortment.db")


@app.route('/madam_baker', methods=['GET', 'POST'])
def baker():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    print(products[0].title)
    return render_template('index.html', products=products)


def main():
    app.run()


if __name__ == '__main__':
    main()