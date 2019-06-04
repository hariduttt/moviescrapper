# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:47:37 2019

@author: harid
"""
from scrapping import Scrapper
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/movie-data/<web_link>/<tag>/<html_class>/<iterations>')
def movie_data(web_link, tag, html_class, iterations):
    database_file = "imdbsqlfile.db"
    table_name = "imdbdata"
    csv_file_name = "imdbmovies.csv"
    imdb_scrapper = Scrapper(table_name, database_file, csv_file_name)
    
    col_1, col_2, col_3, col_4 = imdb_scrapper.default_column()

    scrapped_data = imdb_scrapper.scrap(website_link, tag,
                                        html_class, iterations)
    
    movie_rank, movie_name,\
    movie_year = imdb_scrapper.get_text_from_scrapped_data(scrapped_data)
    
    movie_rating = imdb_scrapper.scrap(website_link, "div",
                                 "ratings-bar strong", iterations)
    
    movie_collumns_dictionary = {col_1:movie_rank, col_2:movie_name,
                                 col_3:movie_year, col_4:movie_rating}
    
   return render_template("movie-data.html",
                          data = movie_collumns_dictionary)

'''@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))'''

if __name__ == '__main__':
   app.run()