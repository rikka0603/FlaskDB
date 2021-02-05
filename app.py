from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/movie')
def movie():
    datalist = []
    con = sqlite3.connect("movie.db")
    cur = con.cursor()
    sql1 = "select * from movie250"
    ver = cur.execute(sql1)
    for item in ver:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template("movie.html", movies=datalist)

    # return render_template("movie.html")


@app.route('/rate')
def rate():
    return render_template('echarts.html')


@app.route('/word')
def word():
    return render_template('word.html')


@app.route('/data')
def data():
    return render_template('data.html')


if __name__ == '__main__':
    app.run()









































