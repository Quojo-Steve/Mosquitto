from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask('__name__')


def connect_to_db() -> sqlite3.Connection:
    con = sqlite3.connect("database.db")
    return con


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/login')
def login():
    try:
        conn = connect_to_db()
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE firstname = ? AND password = ?"
        result = conn.execute(query, (username,password,))
        user_data = result.fetchone()
        if user_data:
            return redirect('/message')
        else:
            return {"message": "User not found!"}
    except Exception as e:
        return {"error": str(e)}


@app.post('/signup')
def signup():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    try:
        con = connect_to_db()
        con.execute('''
                    CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        firstname TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL
                    );
                ''')
        con.execute('''
                INSERT INTO users(
                        firstname,password,email
                    ) VALUES (?,?,?)
                ''', (username, password, email))
        con.commit()
        con.close()
        message = "Successfully created account"
        return render_template('index.html',message=message)
    except sqlite3.Error as e:
        return str(e)

@app.route('/message')
def message():
    return render_template('text.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
