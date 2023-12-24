import os
import psycopg2
from flask import Flask, abort, render_template
from flask import Flask, render_template, request, url_for, redirect
from flask import request, jsonify
# from curses import flash

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

if __name__ == '__main__':
    app.run(debug=True)


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

@app.route('/update/<int:book_id>', methods=['GET', 'POST'])#read the explanation for this line.
def update(book_id):
    if request.method == 'POST':
        # Handling POST requests
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE books SET title=%s, author=%s, pages_num=%s, review=%s WHERE id=%s',
                    (title, author, pages_num, review, book_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'GET':
        # Handling GET requests
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        book = cur.fetchone()
        cur.close()
        conn.close()

        if not book:
            abort(404)  # Book not found

        return render_template('update.html', book=book)
    
@app.route('/delete/<int:book_id>', methods=['GET', 'DELETE'])
def delete(book_id):
    if request.method == 'DELETE':
        # Handling DELETE requests
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the book with the given ID exists
        cur.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        book = cur.fetchone()

        if not book:
            cur.close()
            conn.close()
            return jsonify({'error': 'Book not found'}), 404

        # Delete the book with the given ID
        cur.execute('DELETE FROM books WHERE id = %s', (book_id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({'message': 'Book deleted successfully'})

    if request.method == 'GET':
        # Handling GET requests
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        book = cur.fetchone()
        cur.close()
        conn.close()

        if not book:
            abort(404)  # Book not found

        return render_template('delete.html', book=book)
    
    if request.method == 'POST':
        
        # Example: Additional confirmation step
        confirmation = request.form.get('confirmation')
        if confirmation != 'yes':
            print('Please confirm deletion by entering "yes".', 'error')
            return redirect(url_for('delete', book_id=book_id))


        print('Book deleted successfully!', 'success')
        return redirect(url_for('index'))