from datetime import date
from datetime import timedelta

class Card :
    def __init__(self , args = [] ) :
        if args == [] : 
            self.word = input("enter the word or empty line to back : ")
            if self.word == "" :
                return 
            self.pronunciation = input("enter the pronunciation : ")
            self.type = input("enter the categories : ")
            self.next_review = date.today() + timedelta( days= 1 )
            self.level = 0
            print("enter the meaning end by \"$\" ")
            self.meaning = ""
            while True :
                nextline = input()
                if "$" in nextline :
                    nextline , chert = nextline.split("$")
                    self.meaning += "\n" + nextline
                    break
                else :
                    self.meaning += "\n" + nextline
        else :
            self.word = args[0] 
            self.pronunciation = args[1]
            self.type = args[2]
            tmp = tuple ( args[3].split("-") )
            self.next_review = date( int( tmp[0] ) , int ( tmp[1] ) , int (tmp[2] ) )
            self.level = args[4]
            self.meaning = args[5]
        self.word = self.word.strip().replace("'", "`")
        self.type = self.type.strip().replace("'", "`")
        self.meaning = self.meaning.strip().replace("'", "`")
        self.pronunciation = self.pronunciation.strip().replace("'", "`")

    def __str__(self) :
        return "WORD = \"" + str(self.word) + "\" , PRONUNCIATION = \"" + self.pronunciation + "\" , TYPE = \"" + self.type + "\" , NEXT_REVIEW = DATE(\"" + str ( self.next_review ) + "\" ) , LEVEL = " + str(self.level) + " , MEANING = \"" + self.meaning + "\""

    def list_str(self) :
        return "( \"" + str(self.word) + "\" , \"" + self.pronunciation + "\" , \"" + self.type + "\" , DATE(\"" + str ( self.next_review ) + "\" ) , " + str(self.level) + " , \"" + self.meaning + "\" ) "

    def nextlevel(self) :
        if self.level >= len( self.next_moove() ) - 2 :
            print("the card level is max")
            self.level = len( self.next_moove() ) - 2
        self.level += 1

        self.next_review = date.today() + timedelta( days= self.next_moove()[self.level] )
        
    @staticmethod
    def next_moove () :
        return ( 0 , 1 , 2 , 4 , 7 , 14 , 21 , 28 , 30 , 40 , 60 , 90 , 180 , 270 , 360 , 365 )