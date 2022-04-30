from flask import Flask, render_template, url_for
from admin.data import db_session
from admin.data.products import Product
import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from admin.data import db_session
from admin.data.products import Product
from werkzeug.utils import secure_filename
from admin.edit_form import EditForm
from admin.add_form import AddForm




application = Flask(__name__, template_folder=".")
application.config['SECRET_KEY'] = 'baker_admin_secret_key'

db_session.global_init("admin/db/assortment.db")





@application.route('/', methods=['GET', 'POST'])
def baker():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    # print(products[0].title)
    return render_template('main.html', products=products)


db_session.global_init("admin/db/assortment.db")

db_sess = db_session.create_session()
product = db_sess.query(Product).all()


@application.route('/admin', methods=['GET', 'POST'])
def admin():
    db_sess = db_session.create_session()
    product = db_sess.query(Product).all()
    return render_template('admin/index.html', product=product)


@application.route('/edit/<index>', methods=['GET', 'POST'])
def edit(index):
    form = EditForm()
    db_sess = db_session.create_session()
    item = db_sess.query(Product).get(int(index))
    if request.method == 'GET':
        # print(request.form['status_select'])
        # print(form.content.default)
        form.content.default = item.about
        # print(form.content.default)
        return render_template('admin/edit.html', product=product, form=form, item=item)
    elif request.method == 'POST':
        # if form.title.validate(form):
        #     print(1)
        # if form.content.validate(form):
        #     print(2)
        # if form.submit.validate(form):
        #     print(3)
        # a = request.form['about_value']
        f = request.files['file']
        filename = secure_filename(f.filename)
        if filename:
            f.save(f'static/img/product/{filename}')
            item.image_file_path = filename
        # if item.title != form.title.data:
        item.title = form.title.data
        # print(form.content.data, item.about)
        item.about = request.form['about_value']
        # if item.image_file_path == 'static/img/product/':
        if request.form['status_select']:
            print(request.form['status_select'])
            if request.form['status_select'] == "Хит":
                item.status = 2
            elif request.form['status_select'] == "Новинка":
                item.status = 1
            else:
                item.status = None
        db_sess.add(item)
        db_sess.commit()
        return redirect("/admin")
    return render_template("404.html")


@application.route('/delete/<index>', methods=['GET', 'POST'])
def delete(index):
    db_sess = db_session.create_session()
    item = db_sess.query(Product).get(int(index))
    db_sess.delete(item)
    db_sess.commit()
    return redirect("/admin")


@application.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if request.method == 'GET':
        return render_template('admin/add.html', product=product, form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            # print(request.form['status_select'])
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(f'static/img/product/{filename}')
            db_sess = db_session.create_session()
            item = Product()
            item.title = form.title.data
            item.about = form.content.data
            item.image_file_path = filename
            if request.form['status_select'] == "Хит":
                item.status = 2
            elif request.form['status_select'] == "Новинка":
                item.status = 1
            db_sess.add(item)
            db_sess.commit()
            return redirect("/admin")
        return redirect("/")


def main():
    application.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
