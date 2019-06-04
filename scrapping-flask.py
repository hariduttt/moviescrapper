# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:47:37 2019

@author: harid
"""
from scrapping import Scrapper
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/movie-data/<tag>/<html_class>/<int:iterations>')
def movie_data(tag, html_class, iterations):
    database_file = "imdbsqlfile.db"
    table_name = "imdbdata"
    csv_file_name = "imdbmovies.csv"
    web_url = "https://www.imdb.com/search/title?"\
                "genres=drama&groups=top_250&sort=user_rating,desc"
    
    imdb_scrapper = Scrapper(table_name, database_file, csv_file_name)
    
    col_1, col_2, col_3, col_4 = imdb_scrapper.default_column()

    scrapped_data = imdb_scrapper.scrap(web_url, tag,
                                        html_class, iterations)
    
    movie_rank, movie_name,\
    movie_year = imdb_scrapper.get_text_from_scrapped_data(scrapped_data)
    
    movie_rating = imdb_scrapper.scrap(web_url, "div",
                                 "ratings-bar strong", iterations)
    sized = len(movie_rank)
    
    return render_template("movie-data.html", data1 = movie_rank,
                           data2 = movie_name, data3 = movie_year,
                           data4 = movie_rating, size = sized)

if __name__ == '__main__':
   app.run()