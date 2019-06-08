# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:47:37 2019
@author: haridutt
"""
from scrapping import Scrapper
from flask import Flask, render_template, request, json, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('movie_data_base', start = 1, tag = 'h3',
                            html_class = "lister-item-header",
                            iterations = 50, sorter = 0))

@app.route('/movie-data/<int:start>/<tag>/<html_class>/<int:iterations>/'\
           '<int:sorter>/', methods =['GET','POST'])
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
        
    movie_data_dictionary = {"rank":movie_rank, "name":movie_name,
                             "year":movie_year,
                             "rating":movie_rating, "link":movie_links}    
    imdb_scrapper.to_json("movie_data.json", "rank", "name", "year", "rating",
                          "link", movie_rank, movie_name, movie_year,
                          movie_rating, movie_links)
    collumn_list = list(zip(movie_rank, movie_name, movie_year,
                 movie_rating, movie_links))
    collumn_list.sort(key = lambda t:t[sorter])
    
    if(request.method == 'POST'):
        response = app.response_class(
                response = json.dumps(movie_data_dictionary),
                status = 200,
                mimetype = "application/json"
                )
        return response
                
    return render_template("movie-data.html", data = collumn_list,
                           size = sized)


if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)