# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:47:37 2019
@author: haridutt
"""
from scrapping import Scrapper
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/movie-data/<int:start>/<tag>/<html_class>/<int:iterations>')
def movie_data_base(start, tag, html_class, iterations):
    if(start == 1):
        web_url = "https://www.imdb.com/search/title?"\
                    "genres=drama&groups=top_250&sort=user_rating,desc"
    else:
        web_url = "https://www.imdb.com/search/title?"\
                    "genres=drama&groups=top_250&sort=user_rating,desc"\
                    "&start=" + str(start) + "&ref_=adv_nxt"
                    
    imdb_scrapper = Scrapper()
    
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
   app.run(host='0.0.0.0')