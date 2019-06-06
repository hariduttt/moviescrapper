# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:47:37 2019
@author: haridutt
"""
from scrapping import Scrapper
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/movie-data/<int:start>/<tag>/<html_class>/<int:iterations>/'\
           '<int:sorter>')
def movie_data_base(start, tag, html_class, iterations, sorter):    
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
    movie_links = imdb_scrapper.get_link(web_url, tag,
                                         html_class, iterations)
    sized = len(movie_rank)
    for x in range(sized):
        movie_rank[x] = int(movie_rank[x].split('.')[0])
    l = list(zip(movie_rank, movie_name, movie_year,
                 movie_rating, movie_links))
    if(sorter == 0):
        l.sort(key = lambda t:t[0])
    elif(sorter == 1):
        l.sort(key = lambda t:t[1])
    elif(sorter == 2):
        l.sort(key = lambda t:t[2])
    elif(sorter == 3):
        l.sort(key = lambda t:t[3])
        
    return render_template("movie-data.html", data = l, size = sized)

    
if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)