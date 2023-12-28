import os
import psycopg2

from flask import Flask, render_template, request, url_for, redirect, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    print("Books before deletion:", books)
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/update/<int:book_id>/', methods=['GET', 'PUT', 'POST'])
def update(book_id):
    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books WHERE id=%s;', (book_id,))
        book = cur.fetchone()
        cur.close()
        conn.close()

        if book:
            return render_template('update.html', book=book, book_id=book_id)
        else:
            return jsonify({"error": "Book not found"}), 404

    elif request.method in ['PUT', 'POST']:
        if request.form.get('_method') == 'PUT':
            # Handle the update logic
            conn = get_db_connection()
            cur = conn.cursor()

            title = request.form['title']
            author = request.form['author']
            pages_num = int(request.form['pages_num'])
            review = request.form['review']

            cur.execute('UPDATE books SET title=%s, author=%s, pages_num=%s, review=%s WHERE id=%s',
                        (title, author, pages_num, review, book_id))

            conn.commit()
            cur.close()
            conn.close()

            return redirect(url_for('index'))

    # If the request is not GET, PUT, or POST, or if the form didn't contain '_method' as 'PUT'
    return jsonify({"error": "Invalid request"}), 400


@app.route('/patch/<int:book_id>/', methods=['GET', 'PATCH'])
def patch_example(book_id):
    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books WHERE id=%s;', (book_id,))
        book = cur.fetchone()
        cur.close()
        conn.close()

        if book:
            return render_template('update.html', book=book, book_id=book_id)
        else:
            return jsonify({"error": "Book not found"}), 404

    elif request.method == 'PATCH':
        conn = get_db_connection()
        cur = conn.cursor()

        # Assume that the request data contains the fields to be updated
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid request data"}), 400

        # Construct the dynamic update query based on the provided fields
        update_query = 'UPDATE books SET '
        update_values = []

        for key, value in data.items():
            update_query += f'{key}=%s, '
            update_values.append(value)

        update_query = update_query.rstrip(', ')
        update_query += ' WHERE id=%s'
        update_values.append(book_id)

        cur.execute(update_query, tuple(update_values))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))

@app.route('/delete/<int:book_id>/', methods=['GET', 'POST', 'DELETE'])
def delete(book_id):
    if request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books WHERE id=%s;', (book_id,))
        book = cur.fetchone()
        cur.close()
        conn.close()

        if book:
            return render_template('delete.html', book=book, book_id=book_id)
        else:
            return jsonify({"error": "Book not found"}), 404

    elif request.method == 'POST' and request.form.get('_method') == 'DELETE':
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('DELETE FROM books WHERE id=%s;', (book_id,))
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))

    # If the request is not GET or DELETE
    return jsonify({"error": "Invalid request"}), 400

@app.route('/head/', methods=['GET', 'HEAD'])
def head_example():
    # Assume the resource always exists for demonstration purposes
    resource_exists = True

    if resource_exists:
        # Return only the headers without a response body
        response_headers = {'Custom-Header': 'SomeValue'}
        return '', 200, response_headers
    else:
        # If the resource does not exist, return a 404 status code
        return '', 404
    
if __name__ == '__main__':
    app.run(debug=True)