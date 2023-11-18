from flask import Flask, jsonify, request, redirect
import pymysql
from flask_cors import CORS

# Set the database credentials
host = 'database-1.cwruyiuygx34.us-east-2.rds.amazonaws.com'
port = 3306
user = 'admin'
password = 'password'
database = 'library_system'

# Connect to the database
connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
app = Flask(__name__)
CORS(app)


# The response model is a list of strings since you're only returning titles
@app.route("/books/titles")
def get_book_titles():
    # Using a with statement ensures the cursor is closed automatically
    cur = connection.cursor()
    cur.execute("SELECT Title FROM books")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

# get all books with page number + limits. If page == 0, return all
@app.route("/books")
def get_book_info():
    page_num_str = request.args.get("page")
    limit_str = request.args.get("limit")
    cur = connection.cursor()

    if not page_num_str: 
        cur.execute("SELECT * FROM books")
        result = cur.fetchall()
        cur.close()
        return jsonify(result)

    page_num = int(page_num_str)
    limit = int(limit_str)
    
    # if not specify page, or set it to 0
    # we return all books
    if page_num == 0:
        cur.execute("SELECT * FROM books")
    else:
        offset = (page_num - 1) * limit
        cur.execute(f"SELECT * FROM books LIMIT {limit} OFFSET {offset}")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

# get books with same author
@app.route("/books/authors")
def get_book_info_for_an_author():
    author = request.args.get("author")
    cur = connection.cursor()

    author = author.replace('+', ' ')
    cur.execute(f"SELECT * FROM books WHERE Author = '{author}'")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

# get books with same genre
@app.route("/books/genres")
def get_book_for_a_genre():
    genre = request.args.get("genre")
    cur = connection.cursor()

    genre = genre.replace('+', ' ')
    cur.execute(f"SELECT * FROM books WHERE Genre = '{genre}'")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

# get books with same category
@app.route("/books/categories")
def get_book_for_a_category():
    category = request.args.get("category")
    cur = connection.cursor()

    category = category.replace('+', ' ')
    cur.execute(f"SELECT * FROM books WHERE Category = '{category}'")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

# get a specific book info
@app.route('/books/info')
def get_book_with_isbn():
    isbn = request.args.get("isbn")
    cur = connection.cursor()
    cur.execute(f"SELECT * FROM books WHERE ISBN = '{isbn}'")
    result = cur.fetchall()
    cur.close()
    if not result:
        return "NULL"
    return jsonify(result)


# add a book
@app.route('/books', methods=['POST'])
def add_book():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    genre = request.form['genre']
    category = request.form['category']
    edition = request.form['edition']
    status = "Available"

    cur = connection.cursor()
    cur.execute(f"INSERT INTO books(ISBN, Title, Author, Genre, Category, Edition, Status) VALUES('{isbn}', '{title}', '{author}', '{genre}', '{category}', '{edition}', '{status}')")
    cur.close()

    return redirect('/books')

# update a book status
@app.route('/books', methods=['PUT'])
def update_book_status():
    isbn = request.form['isbn']
    status = request.form['status']

    cur = connection.cursor()
    cur.execute(f"UPDATE books SET Status = '{status}' WHERE ISBN = {isbn}")
    cur.close()

    return redirect('/books')

# remove a book
@app.route('/books', methods=['DELETE'])
def delete_book():
    isbn = request.form['isbn']

    cur = connection.cursor()
    cur.execute(f"DELETE FROM books WHERE ISBN = {isbn}")
    cur.close()

    return redirect('/books')

@app.get("/")
def root():
    return {"message": "This microservice is for our library catalog."}

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(app, host="0.0.0.0", port=8000)
