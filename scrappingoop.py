# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:42:19 2019

@author: harid
"""
import requests
import bs4 
import csv
import re
import pandas as pd
import sqlite3 as sql

class scrapper():
    
    def scrap(self, string):
        page = requests.get(string)
        data = bs4.BeautifulSoup(page.content,
                                     "html.parser")
        return data
                
    
    def connect_database(self, filename): 
        #create database connection
        db = sql.connect(filename)
        cursor = db.cursor()
        
        return db, cursor
    

    def drop_table(self, db, cursor, tablename):
        cursor.execute("DROP TABLE IF EXISTS " + tablename)
        db.commit()


    def create_table(self, db, cursor, tablename, *args):
        #create table
        create_table_query = "CREATE TABLE " + tablename + " ("
        
        size = len(args)
        
        for value in range(size):
            create_table_query += args[value]
            if(value == 0):
                create_table_query += " PRIMARY KEY, "
            else:
                if(value != size-1):
                    create_table_query += ", "
        create_table_query += ")"
        
        cursor.execute(create_table_query)
        db.commit()

    def insert_data(self, cursor, tupple):
        cursor.execute('''INSERT INTO imdbdata values(?,?,?,?)'''
                       , tupple)
        
    def show_data(self, cursor, tablename):
        #show data from sqllite file
        cursor.execute("SELECT * FROM " + tablename)
        data = cursor.fetchall()
        print(data)
        
    def close_database(self, cursor, db):
        #close database connection
        cursor.close()
        db.close()

    def to_csv(self, csv_file, *args):
        #save data in csv file, method-1 
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
            
            size = len(args)
            
            header = []
            
            for x in range(int(size/2)):
                header.append(args[x]) 
            
            if(num == 0):
                #add header if first iteration
                writer.writerow(header)
            
            finaldata = list(zip(args[4], args[5], args[6], args[7]))
        
            for row in finaldata:
                row = list(row)
                writer.writerow(row)
                
    def to_csv2(self, csv_file, *args):
        #save data in csv file, method-2
        size = len(args)
        dic = {}
        for value in range(int(size/2)):
            dic[args[value]] = args[value + int(size/2)]
        df = pd.DataFrame(dic)
        
        if(num==0):
            df.to_csv(csv_file,
                      mode="a", index=False)
        
        #if not first iteration then don't add header
        else:
            df.to_csv(csv_file, mode="a",
                      header=False, index=False)
        

if __name__ == "__main__":
    
    obj1 = scrapper()
    
    for num in [0,51,101,151]:
    
        #if first iteration
        if(num == 0):
            string = "https://www.imdb.com/search/title?"\
                         "genres=drama&groups=top_250&"\
                         "sort=user_rating,desc"
    
        #other iterations
        else:
            string = "https://www.imdb.com/search/title?"\
                        "genres=drama&groups=top_250&"\
                        "sort=user_rating,"\
                        "desc&start=" + str(num) + "&ref_=adv_nxt"
        
        #print(string)
        data = obj1.scrap(string)
    
        list1 = data.select("h3.lister-item-header")
    
        list2 = []
    
        #if last iteration
        if(num == 151):
            iterations = 30
        
        else:
            iterations = 50
        
        for x in range(iterations):
            list2.append(list1[x].get_text())
    
        list3 = []
        list4 = []
        list5 = []
    
        for tupple in list2:
            
            #split scrapped data
            part_1,movie_rank,movie_name,movie_year,part_5 = tupple.split('\n')
            
            #if data itself contains "," then replace it with space
            if(re.search(',',movie_name)):
                movie_name = movie_name.replace(", "," ")   
            
            #furthure splitiing for pure data...
            tempe4 = movie_year.split(" ")
            
            if(len(tempe4) > 1):
                movie_year = tempe4[1] 
            
            temp6 = movie_year.split('(')
            temp7 = temp6[1]
            temp8,temp9 = temp7.split(')')
            list3.append(movie_rank)
            list4.append(movie_name)
            list5.append(temp8)
        
        #scraps rating from imdb
        list6 = data.select("div.ratings-bar strong")
        
        list7 = []
        
        for x in list6:
            list7.append(x.get_text())
        
        csv_file = "imdbmovies.csv"
        
        h1 = "Rank"
        h2 = "Name"
        h3 = "Year"
        h4 = "Rating"
        
        obj1.to_csv(csv_file, h1, h2, h3, h4,
                    list3, list4, list5, list7)
        
        #csv_file2 = "imdb2.csv"
        #obj1.to_csv2(csv_file2, h1, h2, h3, h4,
        #             list3, list4, list5, list7)
        
        filename = "imdbsqlfile.db"
        db, cursor = obj1.connect_database(filename)
            
        tablename = "imdbdata"
        obj1.drop_table(db, cursor, tablename)
        
        obj1.create_table(db, cursor, tablename, "rank INTEGER",
                          "name TEXT", "year INTEGER", "rating FLOAT")
        
        if(num == 151):
            ran = 30
        else:
            ran = 50
        
        #insert data into sqlite database
        for x in range(ran):
            tupple = (list3[x], list4[x], list5[x], list7[x])
            obj1.insert_data(cursor, tupple)
        
        obj1.show_data(cursor, tablename)
        
    obj1.close_database(cursor, db)