from MySQLdb.connections import Connection
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path="")

# fungsi koneksi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_apotek'
mysql = MySQL(app)

# fungsi view index() untuk menampilkan data dari database


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM obat")
    rv = cur.fetchall()
    cur.close()
    return render_template('index.html', obat=rv)

# fungsi view tambah() untuk membuat form tambah


@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama_obat']
        harga = request.form['harga']
        stok = request.form['stok']
        val = (nama, harga, stok)
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO obat(nama_obat, harga,stok) VALUES (%s, %s, %s)", val)
        mysql.connection.commit()
        return redirect(url_for('index'))
    else:
        return render_template('tambah.html')
# fungsi view edit() untuk form edit


@app.route('/edit/<kd_obat>', methods=['GET', 'POST'])
def edit(kd_obat):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM obat WHERE kd_obat =%s', (kd_obat,))
    data = cur.fetchone()
    if request.method == 'POST':
        id_barang = request.form['kd_obat']
        nama = request.form['nama_obat']
        harga = request.form['harga']
        stok = request.form['stok']
        val = (nama, harga, stok, id_barang)
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE obat SET nama_obat=%s, harga=%s, stok=%s WHERE kd_obat=%s", val)
        mysql.connection.commit()
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', data=data)
# fungsi untuk menghapus data


@app.route('/hapus/<kd_obat>', methods=['GET', 'POST'])
def hapus(kd_obat):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM obat WHERE kd_obat=%s', (kd_obat,))
    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
