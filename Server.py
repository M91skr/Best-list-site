"""---------------------------------------- Virtual_Bookshelf ----------------------------------------
In this code, a site for registering favorite books is written.

The user can register a list of his favorite books that includes the name of the book, the name of the author, and
choose a score for it.

The user can edit the rating of his books or delete a book if needed.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# ---------------------------------------- DB extension Creation ----------------------------------------

db = SQLAlchemy()

# ---------------------------------------- Flask Server Creation ----------------------------------------

app = Flask(__name__)

# ---------------------------------------- SQLite database Creation ----------------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


# ---------------------------------------- Site Pages Definition ----------------------------------------


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = {"name": request.form["book_name"], "author": request.form["book_author"],
                    "rating": request.form["book_rating"]}
        new_book = Book(name=new_book["name"], author=new_book["author"], rating=new_book["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit', methods=["GET", "POST"])
def edit_rate():
    if request.method == "POST":
        book_id = request.form['id']
        book = Book.query.get(book_id)
        book.rating = request.form["rating"]
        db.session.commit()
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template('edit.html', book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
