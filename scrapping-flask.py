# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:47:37 2019

@author: harid
"""
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/movie-data')
def movie_data():
    
   return render_template("movie-data.html", data = movie_data)

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