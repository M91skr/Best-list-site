## Virtual Bookshelf

## Description
In this site, the best books that I have read and the best movies, based on the site..., have been collected.

### In the books section:
The user can register a list of his favorite books that includes the name of the book, the name of the author, and 
choose a score for it.

The user can edit the rating of his books or delete a book if needed.

### In the films section:
The user can add a list of his favorite movies.

This work is facilitated by the apis of themoviedb.org site.

The user enters the name of the movie, through the search api, all movies with similar names are identified and shown to the user. The user selects the desired movie, and through the movie information api, the movie's specifications (including the original title, year of production, poster image and description of the desired movie) are received and added to the site.



The user can rate his videos. In this case, the movies will be sorted by rank.

The user can edit the rating and description of the movie.

Also, the user can completely delete a video.

.........



## How to run
run following:
```bash
python -m venv env
. env/bin/activate
pip install -r requirements.txt
python server.py
```
