API_KEY='APikey'
from datetime import datetime
import random
from telegram.ext import *
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def sample_res2(text):
    try:
        print(text)


        def get_title_from_index(index):
        	return df[df.index  == index]["title"].values[0]

        def get_index_from_title(title):
        	return df[df.title == title]['index'].values[0]
#read csv
        df= pd.read_csv(r'v1.csv')
        df["title"]= df["title"].str.upper().str.title()
        features=['book_desc','book_authors','genres']
#create a df with all combned featues selected
        for features in features:
            df[features]=df[features].fillna('')
        def combine_features(row):
            return row['book_desc']+" "+row['book_authors']+" "+row['genres']
        df['combine_features']=df.apply(combine_features,axis=1)
#creating count matrix
        cv=CountVectorizer()
        count_matrix=cv.fit_transform(df['combine_features'])
#cosine similarity
        cosine_sim=cosine_similarity(count_matrix)
#print(cosine_sim)
        book_user_likes=str(text)
        book_index=get_index_from_title(book_user_likes)
#print(movie_index)
        simalar_books=list(enumerate(cosine_sim[book_index]))
#desending order
        sorteds_similar_books=sorted(simalar_books,key=lambda x:x[1],reverse=True)
#print
        i=1
        result=[]
        up=[]
        for book in sorteds_similar_books:
                r=get_title_from_index(book[0])
                result.append(r)
                i=i+1
                if i>10:
                    break
        result.pop(0)
        u = random.sample(result,k=5)
        up.append(u)
        res = str(up)[2:-2]
        k='The books similar to '+text+' are:\n'
        res=k+res
        k=res.replace(",","\n")
        print(k)
        return str(k)
    except:
        return "Enter Correct book Name (or) in a correct format way you can get instructions by using '/help' "

def sample_res1(text):  
    try:
        print(text)
        
        def get_title_from_index(index):
                return df[df.index == index]["title"].values[0]

        def get_index_from_title(title):
            return df[df.title == title]["index"].values[0]

        df= pd.read_csv(r'movie_dataset.csv')
        df["title"]= df["title"].str.upper().str.title()
        features=['keywords','cast','genres','director']

        for features in features:
            df[features]=df[features].fillna('')
        def combine_features(row):
            return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
        df['combine_features']=df.apply(combine_features,axis=1)

        cv=CountVectorizer()
        count_matrix=cv.fit_transform(df['combine_features'])

        cosine_sim=cosine_similarity(count_matrix)

        movie_user_likes=str(text)

        movie_index=get_index_from_title(movie_user_likes)
        simalar_movies=list(enumerate(cosine_sim[movie_index]))

        sorteds_similar_movies=sorted(simalar_movies,key=lambda x:x[1],reverse=True)
        i=1
        result=[]
        up=[]
        for movie in sorteds_similar_movies:
            r=get_title_from_index(movie[0])
            result.append(r)
            i=i+1
            if i>10:
                 break
        result.pop(0)
        u = random.sample(result,k=5)
        up.append(u)
        res = str(up)[2:-2]
        k='The Movies similar to '+text+' are:\n'
        #emo='\U0001f600'
        res=k+res
        k=res.replace(",","\n")
        print(k)
        return str(k)
    except:
        return "Enter Correct Movie Name (or) in a correct format way you can get instructions by using  '/help' "
       

def sample_res(text):
    u=str(text)
    if u in('Hi','Hello','Hlo'):
        return 'Hello  ---use "/help" or "/start" to know about Bot ---'
    elif u in ('Who Are You?','What Do You Do?'):
        return "I am a bot which can recommend you a bunch of movies and books you can get instructions by using '/help' "
    elif(u[0:6]=='Movie-'):
        k=str(u[6:])
        print(k)
        return sample_res1(k)
    elif(u[0:5]=='Book-'):
        print(u)
        k=str(u[5:])
        print(k)
        return sample_res2(k)
    else:
        return 'use--"/help" or "/start" '
print("started")

def start_command(update,context):
    update.message.reply_text('Hi I am a bot which can recommend you a bunch of movies and books\nyou can get recommendation by sending messages to this bot in the format of\nFor movies:\nMovie-<movie name>\nFor Book:\nBooks-<book name>\nFor best recomendation use movie name or book name you liked before\nEx:Movie-gravity\n  Book-twilight')

def help_command(update,context):
    update.message.reply_text(' Instructions:-\nyou can get recomendations by sending messages to this bot in the format of\nFor movies:\nMovie-<movie name>\nFor Books:\nBook-<book name>\nFor best recomendation use movie name or book name you liked before\nEx:Movie-gravity\n  Book-twilight')

def error(update,context):
    print(f"update {update} caused error {content.error }")

def handel_message(update,context):
    text=str(update.message.text).title()
    #text=str(update.message.text)

    response= sample_res(text)

    update.message.reply_text(response)

def main():
    updater=Updater(API_KEY,use_context=True)
    dp=updater.dispatcher
 
    dp.add_handler(CommandHandler('start',start_command))
    dp.add_handler(CommandHandler('help',help_command))
    dp.add_handler(MessageHandler(Filters.text,handel_message))
    updater.start_polling()
    #updater.idel()
main()
