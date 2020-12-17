####################################################################################################
## The following program is a movie recommendation tool. Based on several filters the user can choose from, it suggests 1-25 movies to watch and gives information on genre, release year, rotten tomatoes score, number of reviews, and a description. The filter process is looped to allow restarts in case of wrong entries or empty searches.
####################################################################################################

#First pandas is imported to allow reading and filtering csv files 
#Pandas is imported as pd to simplify referencing it
#Difflib is imported to enable a title search based on an estimation of the title (therefore the input 'toy stori'can return the toy story movie information)

import pandas as pd
from difflib import get_close_matches


#read csv allows access to the data of the referenced csv file
movies = pd.read_csv ('movie_list.csv')

#This first function allows the search for movie information based on an estimation of the movie title
#While loops are used throughout all filters to let the user retry in case of errors

def title():
  KeepGoing = True 
  while KeepGoing:
    KeepGoing = False
    title = input("\nEnter a Title: ")

#The cutoff determines how accurately the user must enter the movie title in percentage terms. It is based on the congruence of characters between input and database. It does take the order of characters into account. While n = 1 filters out all the duplicates, making only the first match appear. Furthermore, astype(str) makes the get_close_matches read movies dataframe as a string

    movies_temp1 = get_close_matches(title, movies['Title'].astype(str), n = 1, cutoff = 0.6)
    best_match = "-"
#since movies_temp1 is a list, join() is used to convert the movies_temp1 to the string format
    best_match = best_match.join(movies_temp1)

  #Try allows to test a code for errors, except then specifies actions if errors are found this structure is repeated for all filters
    try:
      if title == best_match:
  #.loc is a command that enables the search through a a column with a defined title (in this case 'Genres') in the defined csv file, duplicates are then eliminated from the list 
        df = movies.loc[(movies.Title == title)]
        df = df.drop_duplicates(subset = ['Title'], keep = 'first')
  # in order to print the full tables the dataframe is printed as a string.
        print(df.to_string())
      else:
  #df introduces a new dataframe, isempty then defines that the user should be asked to input something else if no close matches can be found and the dataframe is empty. 
        df = movies.loc[(movies.Title == best_match)]
        df = df.drop_duplicates(subset = ['Title'], keep = 'first')
        df_1 = pd.DataFrame(df)
        isempty = df_1.empty
        #Another if statement is introduced in case get_close_matches returns an output same as one of the titles
        if isempty == False:
          print("\n\tDid you mean",best_match,"?")
          print(line)
          print("\n", df.to_string())
        elif isempty == True:
          print("\tPlease try again.")
          KeepGoing = True
    except ValueError:
      print("Please try again")
      KeepGoing = True

#This function prints out just the genre list from the movies database by filtering out the duplicates
def genre_list():
  genre_list = movies['Genres']
  genre_list = genre_list.drop_duplicates(keep = 'first')
#A dashed line is added to separate the menu
  print(line)
# in order to print the full tables the dataframe is printed as a string.
  print(genre_list.to_string())
  print(line)

#This function filters for genre and for minimum number of reviews
#user enters their preferences, numerical inputs are required to be integers in order to work as a filter. The input for genre is capitalized to enable lowercase inputs
def genre_reviews():
  KeepGoing = True
  while KeepGoing:
    KeepGoing = False
    try:
      #a list of all genres is printed
      genre_list()
      genre = input("\nEnter a genre from the list: ")
      genre1 = genre.title()
  #.loc is a command that enables the search through a a column with a defined title (in this case 'Genres') in the defined csv file
      result = movies.loc[(movies['Genres'] == genre1)]
      df = pd.DataFrame(result)
      isempty = df.empty
      if isempty == True:
        print("\nPlease enter a genre from the list")
        KeepGoing = True
      num_reviews = int(input("\nEnter a minimum number of reviews: "))
    except ValueError:
      print("\tBad command, please try again")
      KeepGoing = True
    
    try:
  #based on the preferences the data is located in the csv and a new dataframe is denoted
      movies_temp4 = movies.loc[(movies['Genres'] == genre1) & (movies['Reviews'] > num_reviews)]
  # in order to print the full tables the dataframe is printed as a string and the loop is repeated if no movies match the selected criteria (meaning if the dataframe is empty).
  
      df = pd.DataFrame(movies_temp4)
      isempty = df.empty
      if isempty == False:
         print(movies_temp4.to_string())
      elif isempty == True:
        print("""

      No movies available. 
      Please enter a different minimum number or genre.

      """)
        KeepGoing = True
    except:
      KeepGoing = True

#This function defines what movies to search for in the csv based on the user input. The input is capitalized to enable lowercase inputs.
def genre():
  KeepGoing = True
  while KeepGoing:
    KeepGoing = False
    genre_list()
    genre = input("\nEnter a genre from the list: ")
    genre1 = genre.title()
    result = movies.loc[(movies['Genres'] == genre1)]
    df = pd.DataFrame(result)
    isempty = df.empty
    if isempty == False:
      print(result.to_string())
    elif isempty == True:
      print("Please enter a genre from the list")
      KeepGoing = True
  
#This function defines a search of movies by year 
def year():
  KeepGoing = True
  while KeepGoing:
    KeepGoing = False
    try:
      year = int(input("\nEnter a year: "))
  #This ensures that an integer is entered
    except ValueError:
      print("\nBad command, please try again")
      KeepGoing = True
    
    try:
  #based on the preferences the data is located in the csv and a new dataframe is denoted
      movies_temp3 = movies.loc[(movies['Year'] == year)]
      movies_temp3 = movies_temp3.drop_duplicates(subset = ['Title'], keep = 'first')
  
  # in order to print the full tables the dataframe is printed as a string. When no movies can be found based on user input the steps are repeated.
      df = pd.DataFrame(movies_temp3)
      isempty = df.empty
      if isempty == False:
        print(movies_temp3.to_string())
      elif isempty == True:
        print("Please enter a different year")
        KeepGoing = True
    except:
      print("Try'1999' or '2019'")
      KeepGoing = True

#This function defines a search of movies by filtering by genre and year of the movies. User enters their preferences, numerical inputs are required to be integers in order to work as a filter.
def genre_year():
  KeepGoing = True
  while KeepGoing:
    KeepGoing = False
    try:
      genre_list()
      genre = input("\nEnter a genre from the list: ")
      genre1 = genre.title()
      result = movies.loc[(movies['Genres'] == genre1)]
      df = pd.DataFrame(result)
  #the loop is repeated if no movies match the selected criteria meaning if the dataframe is empty.
      isempty = df.empty
      if isempty == True:
        print("\n\tPlease enter a genre from the list")
        KeepGoing = True
      year = int(input("Enter a Year: "))

  #This ensures that the user enters an integer
    except ValueError:
      print("\nBad command, please try again")
      KeepGoing = True
    
    try:
  #based on the preferences the data is located in the csv and a new dataframe is denoted
      movies_temp5 = movies.loc[(movies['Genres'] == genre1) & (movies['Year'] == year)]
  
  # in order to print the full tables the dataframe is printed as a string and the loop is repeated if no movies match the selected criteria meaning if the dataframe is empty
  
      df = pd.DataFrame(movies_temp5)
      isempty = df.empty
      if isempty == False:
        print(movies_temp5.to_string())
      elif isempty == True:

      #The triple quotes allow to set this specific error message apart from the general instructions
        print("""

      No movies available. 
      Please enter a different year or genre 
      and restart the search.

      """)
        KeepGoing = True
    except:
      KeepGoing = True

#Returns the best movies of all times from the csv indicated by the genre title "All-Time"
def best():
  
  movies_temp6 = movies.loc[(movies['Genres'] == 'All-Time')]
  print(movies_temp6.to_string())


#The function returns five randomly selected movies  from the whole database cleared from duplicates
def luck():
  
  movies_temp7 = movies
  movies_temp7 = movies_temp7.drop_duplicates(subset = ['Title'], keep = 'first')
  lucky = movies_temp7.sample(n = 5)
  print(lucky.to_string())


#To simplify the initial userinterface, a line is defined and later printed twice to seperate the entries from one another
line = "-----------------------"

#Below are the different filter options 
#This function defines the main user interface menu from where the user can navigate to different functions built into this code. There are 8 possible options the user can choose, if the user types in a wrong number or a string of letter, he/she is returned to the menu and asked to try again
def hub():
  
  end = "\nEnjoy your movie(s)!"
  options = range (1,8)
  options = True
  while options:
    options = False
    print(line)
    print("1. Search for movies")
    print("2. Filter by genre")
    print("3. Filter by year")
    print("4. Filter by genre and number of reviews")
    print("5. Filter by genre and year")
    print("6. View the best movies of all times")
    print("7. I am feeling lucky")
    print("8. Quit")
    print(line)
    user_input = input("\nEnter a number from the menu: ")
#If functions are used to distinguish between the user choices and options are established to allow only 8 actions in the menu

#Enables user to search information for a specific movie based on an approximation of its title
    if user_input == "1":
      title()
      print(end)

#Allows to select a specific genre
    elif user_input == "2":
      genre()
      print(end)

#Allows to select a specific year
    elif user_input == "3":
      year()
      print(end)
  
#Allows to filter for a minimum of reviews and a genre
    elif user_input == "4":
      genre_reviews()
      print(end)

#Allows to filter for both a genre and a year
    elif user_input == "5":
      genre_year()
      print(end)   

#Displays best movies of all time   
    elif user_input == "6":
      best()
      print(end)

#Displays five random movie suggestions
    elif user_input == "7":
      luck()
      print(end)

#Allows the user to quit the menu
    elif user_input == "8":
      print("Hope you enjoyed the Movie Connoisseurs!") 

#Error message in case the user does not choose a menu item    
    else:
      print("\nPlease enter a valid number from the menu")
      options = True
#hub() initates the whole code, since all other functions are launched from the hub() function
hub()
