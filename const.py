class Const :
    @staticmethod
    def invalid_names() :
        return { 'exit' , '' , 'del' , 'add' }
    
    @staticmethod
    def dbname() :
        return "flashcards.db"

    @staticmethod
    def flashcard_choices() :
        return { 'exit' , 'add' , 'leitner' , 'report' , 'del'}
    
    @staticmethod
    def yn() :
        return { 'y' , 'n' , 'Y' , 'N' }