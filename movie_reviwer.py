# FUnctions to be performed
# 1. Add Movie
# 2. Add Series/Episode
# 3. View All
# 4. Edit an Entry
# 5. Filter by Genre
# q. Quit
# Select:

# seperate class for each
# MediaEntry class is the base/parent class , holds title , genre , review and rating used by both movie and series class
# movieENtry class is for movies , Seriesentry class for series -- both use parent , are subclasses of MediaEntry
# entryMangaer class is the manager , its for storing , finding , editing , and filtering .we'll also creates the movie and series objects here
# -- so basically media entry , movientry , seriesentry - ask and store the movies and series info and does some minor correctionds like rating should be below 5 and also give out their own prints using str 
#    and entrymanageer does all the work on the data

#-------------------------------------------------------------------------------------------------------

#lets create a decorator function - it shows the time when the function was used(added or edited or stored or found) , and then calls the function and makes it work , then say ah yes the function was performed
#and ha yes , we are calling our function inside the decorator -- good technique
import datetime

def log_activity(func) :
     def wrapper(*args, **kwargs):
          timestamp = datetime.datetime.now().strftime("%H:%M:%S")  #collects the time at which the function was executed
          print(f"\n[LOG {timestamp}] Running action: {func.__name__}...") 

          result = func(*args , **kwargs)  #calling the function
          print("[LOG] Action complete.")

          return result #at the end obvously wrapper function returns (the calling of the orginal function) by design
     
     return wrapper #means its returning the output of the wrapper function

#filtering the genre - function to check if the movie genre is equal to genre ur searching
# normally u can see if movie.genre = genre u want to search ( target genre ) , and whatever come true , i store those moviee
#but faster method is to create a function thats job is to 
#here fucntion's job is to -  
#now for a fucntion we can also use a nomrla function but we'll use closure function because it has memory
# inner function remembers the value that was entered in the outer fucntion thats what a closure is.. cause the outer function once it runs it dies and forgets the value enterd
#closure basically grabs that value and keeps it alive , like abackpack
#normal way - is iron man comedy , is thor comeddy ..
# closure way - yo function lock in for comedy as ur target -- outer fucntion, store it , now.. iron man check it , thor check it (checking it if its comedy) - inner fucntion does this

def make_genre_filter(target_genre):  #remebers the genre u want to search , target genre 
    def filter_func(entry): #movie object
        # This inner function already remembers target_genre from the outer function , it says i dont need u to tell me the genre agai , outer funtion has already told me which genre to look for , u uss give me the movie
        return entry.genre.lower() == target_genre.lower() #so filter function either returns true or false
    return filter_func
# to use this , say some filter_func = make_genre_filter(genre u want to search) -- since thats what the make genre filter returns so its equal
               # and then filter-func(movie)u can pass for the movie u want 
#now classes
class MediaEntry : #is the parent class, holds data shared by both movie and series class
     total_entries = 0
     def __init__(self, title , review_text , genre , rating):

        self.title = title
        self.review_text = review_text
        self.genre = genre
        self._rating = None
        self.rating = rating
        #the vraible assignment is disguised as an function call , cause RATING IS actually a function thtat we are using as an variable by @property method
        
        MediaEntry.total_entries +=1 #everytime a new object is created the number of entry is counted

    #i have to condition for the rating variaable , it has to be between 0 to 10
    #If i enter enter raitng value directly inside the program(while coding) it'll be bad data since it won't go through condition unless the data is inputed from outside.. 
    # but with property,the rating value entered will go into the rating function whenever the rating variable is brought up inisde the code, and check the conditon
    # means u dont have to write the conditon code again and again , everyimme u call a variable it goes through this property function
    #used in edit_entry below check

     @property #to use the variable as a function , made the variable to a function
     def rating (self): #creted a function called rating
        return self._rating     #returns _rating not rating ,else "rating" will activate function call(setter) then itll get stuck in a loop ( recursion )
                                #and this variable like any other variable must be defined inide init
                                #initiallly  _rating is empty( under init) , but when property function call of the rating is brought , rating function returns _rating , so it stores the value of rating in _rating ..it acts like a storer to avoid recursion(function stuck calling itself infinetley)
    
     @rating.setter #to apply conditions and functionality and make changes to the property vaariable
     def rating(self , value ): #value is the vlaue of the rating variable
        if not ( 0 <= value <= 10): #like using and condition
                raise ValueError ("Invalid rating , rating must be from 0 to 10") #exception handling - print statement must be in the same line
        self._rating = value  
       
        #or can also use try and except
        #basically we try a code , if that fails we do a exception statement

        # try :
        #  if not ( 0 <= value <= 10):
        #     raise ValueError     -> value error is raised , we know it will raise value error and we're raising it

        # except ValueError :      -> exception statement for value error
        #     print("Invalid rating , rating must be from 0 to 10")

        # except typeError :       -> this exception statemenet wont be used since try raised valueerror and not type error
        #     print("this is for type error")

          #or u can directly say -----use this normally
          #      try:
          #        r = int(input("Enter rating: "))
          #      except ValueError as e:
          #        print(e) --> writes a value error message

        
        #if we dont know or we dont care about what error it is , do this
        #it catches any error that happens then prints , we dont care what particular error it is
        # try:
        #      if not (0 <= value <= 10):
        #           raise Exception ("invalid error")  
        # except Exception as e :
        #      print(e)          -->prints "invalid error"

     

     def __str__(self) :       #using str dunder method .. when u print object it gives the loction , when u use str and when object is printed ,it prints whatever is returned here in str dunder function
         return f"Title :{self.title} | Genre : {self.genre} | Rating : {self.rating}" 
    #review text not included here cause we dont want to explode our console when we print our movie object list
    #when we print movie of list , we'll just print the movie name , genre and rating ..its like a headline , later if we want we can do movie1.review_text to get the reviwe of it , this is more clean
        #instead of dot format , use f before the print variables and write the variables directly
        #"Title : {} | Genre : {} | Rating : {}/5 ".format(self.title , self.genre , self.rating )

     def __repr__(self): #str was string representaion of object for user(outside output viewer) , repr is string representation for the programmer juss in case if u need , other programmers can repr print and check what object is u creating antha
                        #when u print object str one prints , to print the repr one u have say print repr(object)
         return f"MovieEntry({self.title} , {self.genre} , {self.rating})"
    

    
    #getting input
    #instead of making a list like below , we'll make it in a seperate class called logbook
    #we'll make seperate classes for each type of functonality
    #one class for movie entry , one for series entry , and one to store it 
    #making classes helps to keep it organizized

    
    #list_of_movies = []
    #list_of_shows = []
    #k=int(input('Enter 1 to review a movie | Enter 2 to review a show'))
    #if k==1 :
        # n = int (input ('number of movies u wish to log : '))
        # for i in range (n) :
             # title = input("Enter the title of the movie: ")  
            #   genre = input("Enter the genre of the movie : ")
            #   review_text = input("Write the review :\n ")
            #   rating = int(input("Enter the rating of the movie from 1 to 5 : "))
            #   new_movie = MovieEntry(title , genre , review_text , rating)
            #   list_of_movies.append(new_movie) #ovie 1 appended in list's first(o) position

#subclass for movies
class MovieEntry(MediaEntry) : #inherited from mediaentry class
     def __init__(self, title,review_text , genre, rating):#order should be same as parent class-- self, title , review_text , genre , rating
        super().__init__(title,review_text , genre, rating) #inorder too use the init from the mediaentry class do- super().init

     def __str__(self):
          return  f"MOVIE:  {super().__str__()}" #inorder to use str from the mediaentry class do super().str
     
#subclass for series
#so its job is to take review for each episode , or the whole season or the whole show depending upon the user's choice
class ShowEntry(MediaEntry) : #order should be same as parent class-- self, title , review_text , genre , rating
     def __init__(self, title, genre, rating , show_review = None , episode_number = None , season_number = None , season_review = None , episode_review= None): #intitlizing the series object
          # equals to none meaning, itll assume none when any of these are not used while creating an object ..go down in main program
          #lets say u juss want  t ,g, r , season_no , season_review
          #so now we can say so = ShowEntry( t ,g, r , season_number = s_no , season_review= s_review) rest all will be assumed as none since they were not entred
         
          # super().__init__(title,review_text = None, genre, rating ) || u cant like this cause its a rule not to mix up keyword arguments in between positional arguments.,so none must be the last argument but itll go out of order ..so we'll assign for all instead
          #so juss say ,-- as we dont need review text
          super().__init__(title, None, genre, rating ) 
          self.show_review = show_review
          self.episode_number = episode_number
          self.season_number = season_number
          self.episode_review = episode_review
          self.season_review = season_review


     def __str__(self) :
     #i wanat it print show name , season number , episode number ..if juss the whole show review , no need of season number and the episode number
       base_str = super().__str__() #title, genre and rating are in base str so use it
     #sceniores - whole show review , no season or episode number mentioned
     #          - a particular season reviwew , season number mentioned
     #          - episode reviw - season number and episode number mentioned
       if self.episode :   #exists  
          return f"SERIES : {base_str} | SEASON NUMBER : {self.season_number} | EPISODE NUMBER : {self.episode_number}"
       elif self.season :
          return f"SERIES : {base_str} | SEASON NUMBER : {self.season_number}"
       return f"SERIES : {base_str}"

#now we'll create a class called manager , which does all the fucntions and also creates objects
class Manager :
     def __init__(self) :
         # create an empty list for movies and shows
         self.entries = [] 
         # list of movies and shows like =[ movie1 , series1 , movie2 ]
         # this is like a box of folders-  box being the list , folder being the movie1 , and "batman ,rating , revie , genre" - all these being the files
         # initializing a list , like object..,evertime i use Manager class, a new empty list is created , so i can use this application when necesary 
         # the application being we might need multiple lists here for watchlist or watchedlsit , and instead of creating neew lists evertime ,,well use this list itself , cause we can reset them evertime we call them in a fucntion and they get initialized #all matter of efficiency
         #here when we use movieshowadder function we initialize only once and add it to the same old list,we dont intialise again ,if we initalize again itll become empty ,,if wecalll soem other function which invloves list we'll initialoz it again

         #object is actually fully created in the main program -> movie1(entry) = MovieEntry(batman , thriller ,4/5 , supercoolmovie)
         
#this funcytion's job is to basically take in the movies and shows(OBJECTS) and append it to the list(another object list)
     @log_activity #this decorator gives time of entry and also calls the entry fucntion to get it started
     def addentry (self , entry ) :
        self.entries.append(entry)
        print(f"Succesfully added {entry.title}")

#we'll make a fucntion to find index , we can use it later on for many reasons
#ways of using function over an object,either do object.function or funcyion(object)- this takes arguemnt
#so we do findindex(batman)..so itll check where batman is inside the entry list and tell the positon
#uk entries[0] is movie 1 object and name get by entries[0].title
     def find_index(self , title_to_find):
      for i in range(len(self.entries)):
            if self.entries[i].title.lower() == title_to_find.lower():
                return i
            return -1

#entering the title and editing what we want
# to use this do , edit_entry(batman)
     @log_activity
     def edit_entry(self , title):
     #first check if the title is in the list
     #this mechanism already works in finding index function ,so we'll use ot , before givning index we check there if the title is in the list
      index = self.find_index(title)
      print(f" title found :  {self.entries[index]}")
     #instead lets make a varaible for the object
      entry = self.entries[index]
     #if u juss say self.entries[index] , thats the object , when u print it , __str__ will printed
      if index == -1 :
          print("entered title is invalid")
          k = input(int("ENTER 1 to edit the title \n ENTER 2 to the rating \n ENTER 3 to edit the genre \n ENTER 4 to edit the review text  "))
     
      if k == 1 :
          newtitle = input(print("Enter the edit for the title"))
          entry.title = newtitle
          print(f"Title updated as {newtitle}")

      elif k == 2 :
          try :
               newrating = int(input(print("Enter the new rating : ")))
               entry.rating = newrating #rating varaible when brought up here uses @property setter behavaing like a function call , so it checks if rating is from 0 to 10
          except ValueError as e :
               print(f"Error : {e}")

      elif k == 3 :
          newgenre = input(print('Enter the new genre'))
          entry.genre = newgenre
          print(f"genre updated to {newgenre}")

      elif k == 4 :
          print(f"entered review : {entry.review_text}")
          newreview = input(print("Enter the new review"))
          entry.review_text = newreview
          print(f"new entered review : {newreview} ")
     
     def showall(self) : #fucntion show all the stuffs entered in the list
      print("------------------------------------")
      print(f"Total {MediaEntry.total_entries} entries")
      #learn to use if not ,
      if not self.entries: #is like asking "if list doest exist(not list)"
                           #if self.entries - asking "if list exists"
          print("list is empty")
      else :
          for entry in self.entries :
               print(entry) #as we know when we print entry(object) it prints str

          print("--------------------------------------goodboy")

     def filter_by_genre(self, genre): #we enter the genre and the function return all the movies belonging to the genre 
        #we have a function "make_genre_filter and filter_func" which checks if the movie genere is equal to the genre to be searched
         filter_func = make_genre_filter(genre)
     
     #new techniqye type shi , call some k = False , so make it true when u sucesfully run what u want , so if u dont run what u want itll remain fakse itself ..so u can say if not k ,shi didnt run-- which means , if the statement is true(not k , is not false , which is true )so the satement below if will run
         found = False

         for entry in self.entries :
             if filter_func(entry) :
                 print(f"{entry}\n")
                 found = True

             if not found : #basically wanting to print a "if it is false then print"
               print("movie with entered genre not found")

#yoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
#-----------MAIN PROGRAM---------------------------
#till now what we did were creating functions inside the classes to use them here , 

if __name__ == "__main__" :        # python assigns __ name__( nametag ) to any given file
                                   # the program file that u run in the terminal is assigned to be the main
                                   # It's usually main = name when u run the same file  
                                   # but Let's say a new file test.py 
                                   # U import some movieapp( another file )
                                   # -- import movieapp
                                   # And u run test.py - python test py
                                   # Now main is test.py is seen as the main ,and any other file imported is seen as name(they all have tehir own name tag ofcourse , if their not main , their juss name) - so movieapp isn't main ,and name = Main is false 
                                   # here itll come into movieapp and check if name = main , checking if moveapp is the main ..if not then main program inst allowed , only stuffs outisde can be seen , that is to acces all the classes and the functions
                                   # Why use this though? - lets say I make a new file (pgb), I import program(pgA) which has many classes and funcions , if pga  has "if name == main" , then i can juss access classes and functions without having to run the etnire program , else itll run the entire program(itll ask like enter the movie in the terminal) , but we dont want that , we juss need the classes and funcitions used in the program

     
     logbook = Manager() # so an empty "object" list is created and stored in logbook variable
                         #logbook is basically an empty object list -- self.entries[]
                         # Managaer() - runs the class , in that class we have init fucntion which runs, which creates the empty self.entries object list ...this is stored in logbook - an empty objectlist
                         # other functions(methods) inside manager dont run yet , they are manual and have to be called by doing(object.method as u know) - logbook.addentry etc .. .. only init method runs automatically when come accros(class is called) cause its a dunder method which is built to run that way 
      #so bascially what is going on is , we created function and method to work on the self.entries list , now that self.entries list is logbook ,a nd we'll be applying all the functions and methods to loggbook
     while True:
        print("\n=== ----MY WATCH LOG---- ===")
        print("1. Add Movie")
        print("2. Add TV show")
        print("3. View All")
        print("4. Edit an Entry")
        print("5. Filter by Genre")
        print("q. Quit")
        
        choice = input("Select: ")

        if choice == "1" :
            try :
              #first we gotta create an object , and then pass it to the movieshowadder function that we had created
             print('---MOVIE ENTRY---')
             t = input("Title : \n")
             g = input("Genre : \n")
             r = float(input("Rating (0-10): \n"))
             txt = input("Review text : \n")

             #creating the object with MovieEntry clas
             #order should be same as parent class-- self, title , review_text , genre , rating
             mo = MovieEntry( t, txt , g, r)

             #now to use a function(method) over an object as u know , we juss do object.method
             #we are adding mo object into the logbook objectlist through add entry method( adding object inside a object(list)) ..so add entry method is being applied on the logbook object
             logbook.addentry(mo)

            except ValueError as e :
                 print(f"Failed to add : {e}")

        elif choice == "2" :
              try :
                print('---SHOW ENTRY---')
                #object is __init__ self, title, genre, rating , show_review = None , episode_number = None , season_number = None , season_review = None , episode_review= None)
                t = input("Title : ")
                g = input("Genre: ")
                r = float(input("Rating (0-10): "))
                s_no = input("Season number (press ENTER if you want to review the whole show instead) : ")
                if s_no.strip() == "": #.strip is juss a cleanup tool , it removes the empty spaces incase entered
                   s_r = input("SHOW REVIEW : ")
                   so = ShowEntry( t ,g, r , show_review=s_r)
                else :
                     e_no = input("EPISODE NUMBER ( press ENTER if u want to review just the season instead ) : ")
                     if e_no.strip() == "" :
                          s_review = input("SEASON REVIEW : ")
                          so = ShowEntry( t ,g, r , season_number = s_no , season_review = s_review)
                     else :
                          e_review = input("EPISODE REVIEW : ") 
                          so = ShowEntry( t ,g, r, episode_number = e_no , season_number = s_no , episode_review = e_review) 

                logbook.addentry(so)


              except ValueError as e :
                   print(f"Failed to add : {e}")
                   
          
        elif choice == "3" :
             logbook.showall()

        elif choice == "4" :
             title = input("Enter title of the movie/show you wish to edit : ")
             logbook.edit_entry(title)

        elif choice == "5":
             gen = input("Enter the Genre u wish to search : ")
             logbook.filter_by_genre(gen)

        elif choice == "q" :
             print("Thank u")
             break #the program stops , back to terminal command
             
             

          


