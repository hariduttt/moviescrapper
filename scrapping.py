# -*- coding: utf-8 -*-
# -*- PEP-8 Python Standard -*- 
"""
Created on Fri May 31 10:42:19 2019

@author: haridutt
"""
import requests
import bs4 
import csv
import re
import pandas as pd
import sqlite3 as sql

class Scrapper():
    
    #Function to initialize instance variables    
    def __init__(self, table_name, database_file, csv_file):
        self.table_name = table_name
        self.database_file = database_file
        self.csv_file = csv_file
    
    
    #Function to scrape webpage content and convert it into readable text
    def scrap(self, webpage_url, tag, html_class, iterations):
        scrapped_datalist = []
        page = requests.get(webpage_url)
        data = bs4.BeautifulSoup(page.content,
                                     "html.parser")
    
        scrapped_datalist = data.select(tag + "." + html_class)
        
        scrapped_datalist_text = []
        for x in range(iterations):
            scrapped_datalist_text.append(scrapped_datalist[x].get_text())

        return scrapped_datalist_text
                
    
    #Function for database connection and defining a cursor for querying
    def connect_database(self): 
        #create database connection
        database_name = sql.connect(self.database_file)
        cursor = database_name.cursor()
        
        return database_name, cursor
    
    
    #Function to drop a table
    def drop_table(self, database_name, cursor):
        cursor.execute("DROP TABLE IF EXISTS " + self.table_name)
        database_name.commit()

    
    #Function to create a table according to collumns specified in parameters
    def create_table(self, database_name, cursor, *args):
        #create table
        create_table_query = "CREATE TABLE " + self.table_name + " ("
        
        size = len(args)
        
        for value in range(size):
            create_table_query += args[value]
            #First collumn will be considered  as a primary key
            if(value == 0):
                create_table_query += " PRIMARY KEY, "
            else:
                if(value != size-1):
                    create_table_query += ", "
        create_table_query += ")"
        cursor.execute(create_table_query)
        database_name.commit()

    #Function to insert data into table
    def insert_data(self, cursor, iterations, *args):
        collumn_1 = args[0]
        collumn_2 = args[1]
        collumn_3 = args[2]
        collumn_4 = args[3]
        
        for x in range(iterations):       
            row = (collumn_1[x], collumn_2[x], collumn_3[x], collumn_4[x])
            cursor.execute('''INSERT INTO imdbdata values(?,?,?,?)''', row)
        
    
    #Function to show content of a table
    def show_data(self, cursor):
        #show data from sqllite file
        cursor.execute("SELECT * FROM " + self.table_name)
        fetched_data = cursor.fetchall()
        print(fetched_data)
        

    #Function to close database connection    
    def close_database(self, cursor, database_name):
        cursor.close()
        database_name.close()


    #Function to convert scrapped data into a csv file
    def to_csv(self, mode, header_string, *args):
        #save data in csv file, method-1 
        with open(self.csv_file, mode, newline='') as file:
            writer = csv.writer(file, delimiter=',',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
            
            size = len(args)
            if(header_string == "True"):
                header = True
            else:
                header = False
                
            if(header == True):
                header = []
            
                for x in range(int(size/2)):
                    header.append(args[x]) 
            
                #add header if first iteration
                writer.writerow(header)
            
            data_tupple = list(zip(args[4], args[5], args[6], args[7]))
        
            for row in data_tupple:
                row = list(row)
                writer.writerow(row)
    

    #Function to convert scrapped data into a csv file (another function)            
    def to_csv2(self, csv_file, mode, index, *args):
        #save data in csv file, method-2
        size = len(args)
        dic = {}
        for value in range(int(size/2)):
            dic[args[value]] = args[value + int(size/2)]
        df = pd.DataFrame(dic)
        
        df.to_csv(csv_file,
                  mode=mode, index=index)
        
        
    #Function to get readable text data from scrapped (html formatted) data
    def get_text_from_scrapped_data(self, scrapped_data):
        
        list_of_movie_ranks = []
        list_of_movie_names = []
        list_of_movie_years = []
    
        for tupple in scrapped_data:
            
            part_1, movie_rank, movie_name,\
            movie_year, part_5 = tupple.split('\n')
            
            #if data itself contains "," then replace it with space
            if(re.search(',',movie_name)):
                movie_name = movie_name.replace(", "," ")
            
            #furthure splitiing for pure data...
            movie_year_splitted = movie_year.split(" ")
            
            if(len(movie_year_splitted) > 1):
                movie_year = movie_year_splitted[1] 
            
            movie_year_splitted = movie_year.split('(')
            movie_year_part1 = movie_year_splitted[1]
            movie_year_final, movie_year_part2 = movie_year_part1.split(')')
            
            list_of_movie_ranks.append(movie_rank)
            list_of_movie_names.append(movie_name)
            list_of_movie_years.append(movie_year_final)
            
        return list_of_movie_ranks, list_of_movie_names, list_of_movie_years
    
    
    #Function that takes input from user
    def take_input(self):
        webpage_link = input("Enter the URL to scrap : ")
        tag = input("HTML tag of the page to retrieve the data : ")
        html_class = input("Class of the HTML tag : ")
        iterations = int(input("How many datapoints are to"\
                                       "be scrapped? : "))
        mode = input("The mode of operation in file "\
                     "(w:write, a:append) : ")
        header = input ("Add header or not? (True/False) : ")            
        if(header == 'True'):
            column_1, column_2,\
            column_3, column_4 = input("Enter four headers : ").split()
        else:
            column_1 = column_2 = column_3 = column_4 = "default"    
    
        return webpage_link, tag, html_class, iterations, mode, header,\
                column_1, column_2, column_3, column_4


    def default_column(self):
        column_1 = "Rank"
        column_2 = "Name"
        column_3 = "Year"
        column_4 = "Rating" 
        return column_1, column_2, column_3, column_4
        
'''h3.lister-item-header'''

if __name__ == "__main__":
    
    #Create an object of Scrapper class
    database_file = "imdbsqlfile.db"
    table_name = "imdbdata"
    csv_file_name = "imdbmovies.csv"
    imdb_scrapper = Scrapper(table_name, database_file, csv_file_name)
    
    website_link, tag, html_class, iterations,mode, header,\
    column_1, column_2, column_3, column_4 = imdb_scrapper.take_input()

    scrapped_data = imdb_scrapper.scrap(website_link, tag,
                                        html_class, iterations)
    
    movie_rank, movie_name,\
    movie_year = imdb_scrapper.get_text_from_scrapped_data(scrapped_data)
    
    movie_rating = imdb_scrapper.scrap(website_link, "div",
                                 "ratings-bar strong", iterations)
    imdb_scrapper.to_csv(mode, header, column_1, column_2, column_3,
                         column_4, movie_rank, movie_name,
                         movie_year, movie_rating)
    database_object, cursor = imdb_scrapper.connect_database()
    
    imdb_scrapper.drop_table(database_object, cursor)
    imdb_scrapper.create_table(database_object, cursor, "rank INTEGER",
                               "name TEXT", "year INTEGER", "rating FLOAT")
    imdb_scrapper.insert_data(cursor, iterations, movie_rank, 
                        movie_name, movie_year, movie_rating)
    imdb_scrapper.show_data(cursor)
    imdb_scrapper.close_database(cursor, database_object)