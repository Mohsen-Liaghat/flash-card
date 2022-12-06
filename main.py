import sqlite3 as sql 
from datetime import date 
from queue import Queue
import sys 
from random import shuffle


from matplotlib import pyplot as plt
import pandas as pd 


from const import Const as C
from flashcard import Card 

#############################################################################

def printsets( cur ) :
    sets = cur.execute("SELECT * FROM SQLITE_MASTER ").fetchall()
    if sets == None :
        print("you don't have any set.")
    else : 
        print("enter the name of the set that you want to work with that : ")
        print("list of the sets : ")
        for table in sets :
            if table[0] == "table" :
                print('\t' , table[1] ) 

def preparing() :
    print("loading ... ")
    db = sql.connect(C.dbname())
    cur = db.cursor()
    return db , cur

def addset(cur) :
    name = input("enter a name for the set or an empty line for back : ").strip()
    if name != "" :
        while "'" in name :
            print( "name of a set can't contain ' symbol try an other one : " , end = "" )
            name = input().strip()
            if name == "" : 
                return
        sets = cur.execute("SELECT NAME FROM SQLITE_MASTER").fetchall()
        sets = [ i[0] for i in sets ]
        while name in C.invalid_names() or ( sets != None and name in sets ) :
            name = input("sorry, the name was reserved. try another one : ")
            if name == "" :
                return 
        cur.execute("CREATE TABLE " + name + "( \
            WORD TEXT PRIMERY KEY UNIQUE , \
            PRONUNCIATION TEXT , \
            TYPE TEXT, \
            NEXT_REVIEW DATE NOT NULL , \
            LEVEL INT DEFAULT 0 , \
            MEANING TEXT NOT NULL \
        )") 
        print( name , "was sucessfully added to sets.")

def exit_program( db , cur ) :
    cur.close()
    db.close()

def exist_table( cur , table ) :
    return cur.execute("SELECT NAME FROM SQLITE_MASTER WHERE NAME = '" + table + "'" ).fetchone() != None

def addcard( db , cur , table ) :
    card = Card()
    while card.word != "" and card.meaning != "" :
        existed = cur.execute("SELECT * FROM " + table + " WHERE WORD = '" + card.word + "'" ).fetchone()
        if existed == None :
            cur.execute("INSERT INTO " + table + " VALUES " + card.list_str() )
            db.commit() 
            print("The card was added.")
        else :
            print ( existed )
            choice = input("the card has existed. do you want to update that(N/Y)").strip().lower()
            while choice not in C.yn() :
                choice = input("invalid input try another one : ").strip().lower()
            choice = choice.upper()
            if choice == 'Y' : 
                dbupdate(db, cur, table, card)
        card = Card()
                


def today_review( cur , table , today ) :
    today_list = cur.execute("SELECT * FROM " + table + " WHERE NEXT_REVIEW <= '" + str( today ) + "'" ).fetchall()
    shuffle(today_list)
    today_queue = Queue()
    for i in today_list : 
        today_queue.put( Card( i ) )
    return today_queue , len(today_list)

def dbupdate( db , cur , table , card ) :
    cur.execute("UPDATE " + table + " SET " + str(card) + " WHERE WORD = '" + card.word + "'" ) 
    db.commit()
    print("the card has updated.")

def card_review( card , today ) :
    print("###################################")
    print(card.word , '\t type = ' , card.type )
    input("press enter to show the answer. ")
    print("###################################")
    print("###################################")
    print(card.word , '\t category :' , card.type , '\t pronunciation :' , card.pronunciation )
    print()
    print(card.meaning)
    print("###################################")
    
    print("enter B to exit leitner mood.")
    print("enter T for correct answer.")
    print("enter F for wrong answer.")    
    choice = input().strip().lower()

    while choice not in "tfbTFB" or choice == "" :
        choice = input("invalid input try another one : ").strip().lower()

    if choice == "B" or choice == "b" :
        return card , True
    if choice == "T" or choice == "t" :
        card.nextlevel()
        return card , False
    if choice == "F" or choice == "f" :
        card.level = 0 
        card.next_review = str(today)
        return card , False


def leitner_mood( db , cur , table ) :
    today = date.today()
    review_queue , review_number = today_review( cur , table , today )
    
    print("today we can review" , review_number , "cards." )
    
    while not review_queue.empty() :
        print( review_number , " cards are remain.")
        card , no_intrest = card_review( review_queue.get() , today ) 
        if no_intrest :
            break
        elif card.level == 0 :
            review_queue.put(card) 
            dbupdate( db , cur , table , card ) 
        else :
            dbupdate( db , cur , table , card ) 
            review_number -= 1

def openset( db , cur , table ) :
    if exist_table( cur , table ) :
        while True :
            print("###################################")
            print("###################################")
            print("enter leitner to enter to the leitner mood.")
            print("enter add to add a flashcard.")
            print("enter report to report.")
            print("enter del to delete.")
            print("enter exit to exit.")
            choice = input().strip().lower()
            while choice not in C.flashcard_choices() :
                print("invalid input.")
                choice = input().strip().lower()
            if choice == "exit" :
                return
            elif choice == "add" :
                addcard( db , cur , table )
            elif choice == "leitner" :
                leitner_mood( db , cur , table )
            elif choice == "report" :
                report( db , cur , table )
            elif choice == "del" :
                card_del( db , cur , table )

def card_del( db , cur , table ) :
    word = input("enter the name of card that you want to delete or empty line to back : ")
    if word != "" :
        detaile = cur.execute("SELECT * FROM " + table + " WHERE WORD = '" + word + "'" ).fetchone()
        while detaile == None :
            word = input("Invalid input. try another one : ")
            if word == "" : 
                break
            detaile = cur.execute("SELECT * FROM " + table + " WHERE WORD = '" + word + "'" ).fetchone()
        else :
            print( "are you sure to delete this card (Y/N) : ")
            print( Card(detaile) )
            if input().strip().capitalize() == "Y" :
                cur.execute( "DELETE FROM " + table + " WHERE WORD = '" + word + "'" )
                db.commit()
                print("The card has deleted. ")

def report ( db , cur , table ) :
    lr_report = pd.DataFrame(cur.execute("SELECT NEXT_REVIEW, COUNT( WORD ) FROM " + table + " GROUP BY NEXT_REVIEW").fetchall() , columns= [ "date" , "count"] )
    lr_report.plot.bar( x= "date" , y= "count")
    # plt.bar( [ i[0] for i in lr_report ] , [ i[1] for i in lr_report ])
    # plt.figure("Level")
    # lr_report = cur.execute("SELECT NEXT_REVIEW, AVG( LEVEL ) FROM " + table + " GROUP BY NEXT_REVIEW").fetchall()
    # plt.bar( [ i[0] for i in lr_report ] , [ i[1] for i in lr_report ])
    plt.show()

def main() :
    db , cur = preparing() 
    while True :
        print("###################################")
        print("###################################")
        printsets( cur )
        print("enter add to add an empty set.")
        print("enter exit to exit.")
        choice = input().strip()
        if "'" in choice :
            continue
        if choice.lower() == "exit" :
            exit_program( db , cur )
            break
        elif choice == "" :
            pass 
        elif choice.lower == "add" :
            addset(cur)
        # elif choice == "del" :
            # delset()
        else :
            openset( db , cur , choice)
        


if __name__ == "__main__" :
    main()