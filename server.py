"""---------------------------------------- Best list Site ----------------------------------------
In this site, the best books that I have read and the best movies, based on the site..., have been collected.

In the books section:
The user can register a list of his favorite books that includes the name of the book, the name of the author, and
choose a score for it.

The user can edit the rating of his books or delete a book if needed.

In the films section:
The user can add a list of his favorite movies.

This work is facilitated by the apis of themoviedb.org site.

The user enters the name of the movie, through the search api, all movies with similar names are identified and shown to the user. The user selects the desired movie, and through the movie information api, the movie's specifications (including the original title, year of production, poster image and description of the desired movie) are received and added to the site.



The user can rate his videos. In this case, the movies will be sorted by rank.

The user can edit the rating and description of the movie.

Also, the user can completely delete a video.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import requests

# ---------------------------------------- Add Parameters ----------------------------------------

movie_db_url = "MOVIE_DB_URL"
movie_db_key = "MOVIE_DB_API_KEY"
movie_search_url = "MOVIE_SEARCH_URL"
movie_image_url = "MOVIE_IMAGE_URL"


# ---------------------------------------- DB extension Creation ----------------------------------------

db = SQLAlchemy()

# ---------------------------------------- Flask Server Creation ----------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

""" ---------------------------------------- SQLite database Creation ----------------------------------------
------------ For books"""

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

# ------------ For films


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()

# ---------------------------------------- Site Pages Definition ----------------------------------------


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/books')
def book():
    all_books = db.session.query(Book).all()
    return render_template('books.html', books=all_books)


@app.route("/books/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = {"name": request.form["book_name"], "author": request.form["book_author"],
                    "rating": request.form["book_rating"]}
        new_book = Book(name=new_book["name"], author=new_book["author"], rating=new_book["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('book'))
    return render_template('books_add.html')


@app.route('/books/edit', methods=["GET", "POST"])
def edit_rate():
    if request.method == "POST":
        book_id = request.form['bk_id']
        book = Book.query.get(book_id)
        book.rating = request.form["rating"]
        db.session.commit()
    book_id = request.args.get('bk_id')
    book_selected = Book.query.get(book_id)
    return render_template('books_edit.html', book=book_selected)


@app.route("/books/delete")
def delete():
    book_id = request.args.get('bk_id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('book'))


@app.route('/films')
def film():
    all_films = Film.query.order_by(Film.rating).all()
    for i in range(len(all_films)):
        all_films[i].ranking = len(all_films) - i
    db.session.commit()
    return render_template('films.html', films=all_films)


@app.route('/films/edit', methods=["GET", "POST"])
def film_edit():
    if request.method == "POST":
        film_id = request.form['fm_id']
        film = Film.query.get(film_id)
        film.rating = request.form["rating"]
        film.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('film'))
    film_id = request.args.get('fm_id')
    film_selected = Film.query.get(film_id)
    return render_template('films_edit.html', film=film_selected)


@app.route("/films/delete")
def film_delete():
    film_id = request.args.get('fm_id')
    film_to_delete = Film.query.get(film_id)
    db.session.delete(film_to_delete)
    db.session.commit()
    return redirect(url_for('film'))


@app.route("/films/add", methods=["GET", "POST"])
def film_add():
    if request.method == "POST":
        new_film = {"title": request.form["title"]}
        response = requests.get(os.getenv(movie_db_url), params={"api_key": os.getenv(movie_db_key), "query": new_film["title"]})
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template('films_add.html')


@app.route("/films/find", methods=["GET", "POST"])
def find_movie():
    if request.method == "GET":
        movie_api_id = request.args.get("id")
        if movie_api_id:
            movie_api_url = f"{os.getenv(movie_search_url)}/{movie_api_id}"
            response = requests.get(movie_api_url, params={"api_key": os.getenv(movie_db_key), "language": "en-US"})
            response.raise_for_status()
            data = response.json()
            new_movie = Film(
                title=data["title"],
                year=data["release_date"].split("-")[0],
                img_url=f"{os.getenv(movie_image_url)}{data['poster_path']}",
                description=data["overview"]
            )
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for("film"))


if __name__ == "__main__":
    app.run(debug=True)
