import configparser
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, json
from werkzeug.exceptions import abort
import utils
from Stocks import stocks

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Leshkovo136'

ini = configparser.ConfigParser()
ini.read('config.ini')

debug = utils.DEBUG()
stocks = stocks.STOCKS()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def root():
    return "hey hey"

@app.route('/about')
def about():
    return render_template('about.html', name='Denis')

@app.route('/index')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', name='Denis', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/req')
def req():
    if request.method == 'POST':
        print('post req here')
    if request.method == 'GET':
        args = request.args
        for k,v in args.items():
            print(k,v)
    return redirect(url_for('index'))

@app.route('/stocks', methods=['GET', 'POST'])
def tables():
    if request.method == 'POST':
        print('[#112] POST comes ')
    if request.method == 'GET':
        print('GET calls')
    return stocks.tables()

@app.route('/stocks_table_td_sel')
def td_sel():
    return stocks.td_sel(request)

@app.route('/stocks/req', methods=['GET', 'POST'])
def stocks_all_calls():
    if request.method == 'POST':
        s = request.data.decode('utf-8')
        args = json.loads(s)
        return stocks.stock_all_calls(args)
    if request.method == 'GET':
        print('GET calls')
        return jsonify({'action':'GET calls'})

def main():
    debug('here')

if __name__ == '__main__':
#    stocks.delete_all_from_table('stock_list')
    stocks.update_stock_list()
#    slist = stocks.get_stock_list()
#    print(slist)
    app.run(debug=True)
