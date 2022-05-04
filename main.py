from flask import Flask, render_template, url_for
from admin.data import db_session
from admin.data.products import Product
import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from admin.data import db_session
from flask import session
from admin.data.products import Product
from admin.data.users import User
from werkzeug.utils import secure_filename
from admin.edit_form import EditForm
from admin.add_form import AddForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # pip install -U flask-cors
from datetime import timedelta
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy.exc import IntegrityError



app = Flask(__name__, template_folder=".")
app.config['SECRET_KEY'] = 'baker_admin_secret_key'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
CORS(app)

app.config['MYSQL_HOST'] = '31.31.198.124'
app.config['MYSQL_USER'] = 'u1635912_default'
app.config['MYSQL_PASSWORD'] = 'Vv8B2y7UkpIOeJa0'
app.config['MYSQL_DB'] = 'u1635912_default'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
is_authorized = False
username = ""

db_session.global_init("admin/db/assortment.db")

db_sess = db_session.create_session()
products = db_sess.query(Product).all()


@app.route('/', methods=['GET', 'POST'])
def baker():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    # print(products[0].title)
    return render_template('main.html', products=products)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    print("huiwihwhifhiwfw")
    print(is_authorized)
    name = db_sess.query(User).get(1).name
    return render_template('admin/index.html', product=products, is_authorized=is_authorized, username=username)


@app.route('/edit/<index>', methods=['GET', 'POST'])
def edit(index):
    form = EditForm()
    db_sess = db_session.create_session()
    item = db_sess.query(Product).get(int(index))
    if request.method == 'GET':
        # print(request.form['status_select'])
        # print(form.content.default)
        form.content.default = item.about
        # print(form.content.default)
        db_sess = db_session.create_session()
        products = db_sess.query(Product).all()
        return render_template('admin/edit.html', product=products, form=form, item=item)
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


@app.route('/delete/<index>', methods=['GET', 'POST'])
def delete(index):
    db_sess = db_session.create_session()
    item = db_sess.query(Product).get(int(index))
    db_sess.delete(item)
    db_sess.commit()
    return redirect("/admin")


@app.route('/add', methods=['GET', 'POST'])
def add():
    global products
    form = AddForm()
    if request.method == 'GET':
        return render_template('admin/add.html', product=products, form=form)
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
            db_sess = db_session.create_session()
            products = db_sess.query(Product).all()
            return redirect("/admin")
        return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('admin/login.html', error=False)
    if request.method == 'POST':
        _login = request.form['login']
        _password = request.form['password']
        user = db_sess.query(User).filter_by(login=_login).first()
        if user:
            if check_password_hash(user.password_hash, _password):
                print("YES")
                global is_authorized
                is_authorized = True
                global username
                username = user.name
                return redirect("/admin")
            else:
                print("NO")
                return redirect("/login")
        return render_template('admin/login.html', error=True)
    # _password = "123"
    # _username = "aaa"
    # a = generate_password_hash(_password)
    # print(a)
    # return render_template("404.html")

    #     # check user exists
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #
    #     sql = "SELECT * FROM user WHERE username=%s"
    #     sql_where = (_username,)
    #
    #     cursor.execute(sql, sql_where)
    #     row = cursor.fetchone()
    #     username = row['username']
    #     password = row['password']
    #     if row:
    #         if check_password_hash(password, _password):
    #             session['username'] = username
    #             cursor.close()
    #             return jsonify({'message': 'You are logged in successfully'})
    #         else:
    #             resp = jsonify({'message': 'Bad Request - invalid password'})
    #             resp.status_code = 400
    #             return resp
    # else:
    #     resp = jsonify({'message': 'Bad Request - invalid credendtials'})
    #     resp.status_code = 400
    #     return resp


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('admin/register.html', password_error=False, login_error=False)
    if request.method == 'POST':
        _login = request.form['login']
        _password = request.form['password']
        _repeat_password = request.form['repeat_password']
        _name = request.form['name']
        print(_password)
        print(_repeat_password)
        if _repeat_password != _password:
            return render_template('admin/register.html', password_error=True, login_error=False)
        else:
            try:
                new_user = User()
                new_user.login = _login
                new_user.name = _name
                new_user.password_hash = generate_password_hash(_password)
                db_sess.add(new_user)
                db_sess.commit()
            except IntegrityError:
                return render_template('admin/register.html', password_error=False, login_error=True)
            return redirect("/admin")
    #     if request.form['status_select'] == "Хит":
    #         item.status = 2
    #     elif request.form['status_select'] == "Новинка":
    #         item.status = 1
    #     db_sess.add(item)
    #     db_sess.commit()
    #     if user:
    #         if check_password_hash(user.password_hash, _password):
    #             print("YES")
    #             return redirect("/")
    #         else:
    #             print("NO")
    #             return redirect("/login")
    #     return render_template('admin/login.html', error=True)
    # # _password = "123"


@app.route('/exit', methods=['GET', 'POST'])
def exit():
    global is_authorized
    is_authorized = False
    return redirect("/admin")


def main():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
