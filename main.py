from flask import Flask, render_template, request, make_response, redirect
from src import database as db
import datetime as dt
import os
import random


app = Flask(__name__)
app.secret_key = "qhaem"
SITE_TITLE = "شرکت نیرو گستر قائم"

UPLOAD_DIRS = [
    'static/assets/image',
    'static/assets/video'
]

for directory in UPLOAD_DIRS:
    os.makedirs(directory, exist_ok=True)

def check():
    admin_token = request.cookies.get('admin-token')
    if not admin_token or not db.check_admin_token(admin_token):
        return redirect('/login-admin')
    return None

@app.get('/')
def index():
    return render_template('index.html', title=SITE_TITLE)

@app.get('/feature')
def feature():
    title = f'{SITE_TITLE} - ویژگی ها'
    return render_template('feature.html', title=title)

@app.get('/services')
def services():
    title = f'{SITE_TITLE} - خدمات'
    return render_template('service.html', title=title)

@app.get('/portfolio')
def portfolio():
    title = f'{SITE_TITLE} - ویژگی ها'
    return render_template('portfolio.html', title=title)

@app.get('/blog')
def blog():
    title = f'{SITE_TITLE} - بلاگ'
    return render_template('blog.html', title=title)

@app.get('/login-admin')
def get_login_admin():
    title = f'{SITE_TITLE} - ورود ادمین'
    return render_template('login-admin.html')

@app.post('/login-admin')
def post_login_admin():
    data = dict(request.values)
    admin_token = db.get_token_admin(data)
    if not admin_token:
        return get_login_admin()
    response = make_response(render_template('ok.html'))
    response.set_cookie('admin-token', admin_token, expires=dt.datetime.now() + dt.timedelta(days=90))
    return response

@app.get('/panel')
def panel():
    admin_token = request.cookies.get('admin-token')
    if admin_token:
        admin = db.get_admin(admin_token)
        title = f'{SITE_TITLE} - پنل ادمین'
        return render_template('admin-panel.html', admin=admin, title=title)
    user_token = request.cookies.get('user_token')
    if not user_token:
        redirect('/login-users')
    users = db.get_user_information(user_token)
    return render_template('panel.html', users=users)

@app.get('/show-users')
def show_admins_in_admin_panel():
    admins = db.show_admins_in_admin_panel()
    title = f'{SITE_TITLE} - نمایش ادمین های سایت'
    return render_template('/admin/show-admins.html', title=title, admins=admins)

@app.get('/<token>')
def edit_admin(token: str):
    if redirect := check(): return redirect
    title = f'{SITE_TITLE} - ویرایش کاربر'
    data = db.get_admin(token)
    return render_template('update-users.html', title=title, data=data)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)