from flask import current_app
import matplotlib.pyplot as plt
from matplotlib import animation
import networkx as nx
from csv import reader
import pandas as pd
import random
from random import sample
import numpy as np


## paths to the files we will use to build our graph
keywords_path = "Downloads/keywords.csv/keywords.csv"
movies_metadata_path = "Downloads/movies_metadata.csv/movies_metadata.csv"
credits_path = "Downloads/credits.csv/credits.csv"
saved_movie_path = "movieGraph.graphml"

colors = {}

## dictionary to store movie metadeta info -- key: movieID, value: movieTitle
movie_list = {}


## a function to read genre information into a dictionary and a list
## input: path to movies_metadata file
## the list keeps tracks of all genres in the file (including duplicates)
## the dictionary stores movie genre info -- key: movieID, value: genre_list
## returns: a genre dict and genre list 
def readGenres(movies_metadata_path):
    metadata = pd.read_csv(movies_metadata_path, low_memory=False)
    genres = {}
    all_genres = []
    for idx in range(len(metadata)):
        g = []
        for i in metadata.iloc[idx]["genres"].split("'name': '")[1:]:
            g.append(i.split("'")[0])
            all_genres.append(i.split("'")[0])
        genres[metadata.iloc[idx]["id"]] = g
        
    return genres, all_genres


## a function to read the movie metadata dataset into a networtx graph
## input: path to movies_metadata file, num_movies (how many movies to read from the dataset)
## each movie_title in the dataset is added as a node in our graph 
## movie_id is added to each node as an attribute 
## node type (movie) is added to each node as an attribute
## returns: movieGraph 
def readMovies(movies_metadata_path, num_movies): 

    count = 0

    movieGraph = nx.Graph()

    nodeDict = {}

    firstRow = True


    with open(movies_metadata_path, 'r', encoding="utf8") as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if firstRow != True:
                nodeInfo = {}
                movie_title, movie_id, genre = row[20], str(row[5]), row[3] 
                movieGraph.add_node(movie_title)
                movie_list[movie_id] = movie_title
                nodeInfo["node_type"] = "movie"
                nodeInfo["movie_id"] = str(movie_id)
                nodeDict[movie_title] = nodeInfo
                nx.set_node_attributes(movieGraph, nodeDict) 

                count += 1
                if count == num_movies:
                    break 

            else:
                firstRow = False 
                

    return movieGraph
            
## a function to add genre edges to the movieGraph 
## input: movieGraph, list of all_genres, genre dict, num_genres(the number of genre lists to read)
## each genre from the genre list (all_genres) is added to the movieGraph as a node 
## an edge is added between each movie and each genre in its associated list of genres  (using the genre dict)

def addGenreEdges(movieGraph, genres, all_genres, num_genres): 

    global movie_list
    
    nodeDict = {}
    for genre in all_genres:
        movieGraph.add_node(genre)
        nodeInfo = {}
        nodeInfo["node_type"] = "genre"
        nodeDict[genre] = nodeInfo
    count = 0

    for key in genres.keys():
        key = str(key)
        if key in movie_list:
            movieID = key
            movieNode = movie_list[movieID]
            nodeInfo = {}
            nodeInfo["node_type"] = "movie"
            nodeDict[movieNode] = nodeInfo
            
            count +=1
            
            genres_list = genres[key] 
            for genre in genres_list:
                movieGraph.add_edge(movieNode, genre)

        if count == num_genres:
            break
            

    nx.set_node_attributes(movieGraph, nodeDict)

## a function to read keyword information into a dictionary and a list
## input: path to keywords file
## the list keeps tracks of all keywords in the file (including duplicates)
## the dictionary stores movie keyword info -- key: movieID, value: keywords_list
## returns: a  keyword dict and keywords list 
def readKeywords(keywords_path):

    keywords_dict = {}
    all_keywords = []
    keywords = pd.read_csv(keywords_path, low_memory=False)

    for idx in range(len(keywords)):
        k = []
        for i in keywords.iloc[idx]["keywords"].split("'name': '")[1:]:
            k.append(i.split("'")[0])
            all_keywords.append(i.split("'")[0])
        keywords_dict[keywords.iloc[idx]["id"]] = k
        
    return keywords_dict, all_keywords 

## a function to add keywords edges to the movieGraph 
## input: movieGraph, list of all genres, keywords dict, num_keywords(the number of keywords lists to read)
## each keyword from the keyword list (all_keywords) is added to the movieGraph as a node 
## an edge is added between each movie and each keyword in its associated list of keywords  (using the keywords_dict)
def addKeywordsEdges(movieGraph, keywords_dict, all_keywords, num_keywords):

    global movie_list
    
    
    nodeDict = {}

    for keyword in all_keywords:
        movieGraph.add_node(keyword)
        nodeInfo = {}
        nodeInfo["node_type"] = "keyword"
        nodeDict[keyword] = nodeInfo
        

    count = 0

    for key in keywords_dict.keys():
        key = str(key)
        count +=1
        if key in movie_list:
            movieID = key
            movieNode = movie_list[movieID]
            nodeInfo = {}
            nodeInfo["node_type"] = "movie"

            nodeDict[movieNode] = nodeInfo
            key = int(key)
            keywords_list = keywords_dict[key]
            for keyword in keywords_list:
                movieGraph.add_edge(movieNode, keyword)

        if count == num_keywords:
            break
            
            
    nx.set_node_attributes(movieGraph, nodeDict)

## a function to read directors information into a dictionary and a list
## input: path to movie credits file
## the list keeps tracks of all directors in the file (including duplicates)
## the dictionary stores movie director info -- key: movieID, value: directors_list
## returns: a  director dict and director list 
def readDirectors(credits_path):

    credits = pd.read_csv(credits_path, low_memory=False)
    director_dict = {}
    all_directors = []
    for idx in range(len(credits)):
        d = []
        for i in credits.iloc[idx]["crew"].split("\'job\': \'Director\', \'name\': \'")[1:]:
            d.append(i.split("'")[0])
            all_directors.append(i.split("'")[0])
            director_dict[credits.iloc[idx]["id"]] = d
            
            
    return director_dict, all_directors
            
        
## a function to add director edges to the movieGraph 
## input: movieGraph, list of all directors, directors dict, num_directors(the number of director lists to read)
## each director from the director list (all_directors) is added to the movieGraph as a node 
## an edge is added between each movie and each directors in its associated list of directors  (using the directors_dict)       
def addDirectorEdges(movieGraph, director_dict, all_directors, num_directors):
    count = 0
    
    nodeDict = {}


    for director in all_directors:
        movieGraph.add_node(director) 
        nodeInfo = {}
        nodeInfo["node_type"] = "director"

        nodeDict[director] = nodeInfo
        
    for key in director_dict.keys():
        key = str(key)
        count +=1
        if key in movie_list:
            movieID = key
            movieNode = movie_list[movieID]
            nodeInfo = {}
            nodeInfo["node_type"] = "movie"
            nodeDict[movieNode] = nodeInfo
            key = int(key)
            for director in director_dict[key]:
                movieGraph.add_edge(movieNode, director)

        if count == num_directors:
            break
            
    nx.set_node_attributes(movieGraph, nodeDict)

## a function to create a dictionary of the number of times each keyword appears in the dictionary 
## inputs: keyword_dict (the dictionary stores movie keyword info -- key: movieID, value: keywords_list), 
## all_keywords (a list of all keywords read from the file including duplicates)
## returns: weighted_keyword_dict (key of the dictionary is the keyword, value is the number of appearances )
def get_keyword_dict(keyword_dict, all_keyword):
    weighed_keyword_dict = {}
    
    #sets the inital value of the keyword
    for keyword in all_keyword:
        #if the keyword isn't in the dictionary
        if keyword not in weighed_keyword_dict.keys():
            #set its value to 1
            weighed_keyword_dict[keyword] = 1
        #otherwise increase values by 1 
        else:
            weighed_keyword_dict[keyword] += 1
    
    for keyword_list in keyword_dict.values():
        for keyword in keyword_list:
            if keyword not in weighed_keyword_dict.keys():
                 weighed_keyword_dict[keyword] = 1
            else:
                weighed_keyword_dict[keyword] += 1
    
    return weighed_keyword_dict 


## run the functions defined above 
movieGraph = readMovies(movies_metadata_path, 1000)
genre_dict, all_genres = readGenres(movies_metadata_path) 
addGenreEdges(movieGraph, genre_dict, all_genres, 1000)
keywords_dict, all_keywords = readKeywords(keywords_path)
weighed_keyword_dict = get_keyword_dict(keywords_dict, all_keywords)
addKeywordsEdges(movieGraph, keywords_dict, all_keywords, 1000)
director_dict, all_directors = readDirectors(credits_path)
addDirectorEdges(movieGraph, director_dict, all_directors, 1000) 

## a function to get a movie that a user likes 
## prints a random list of movies to the console and asks user to choose one
## takes input from the user and saves it into a variable i.e. start_movie
## returns start_movie
def get_user_liked():
    # get random list from database to present to user
    random_list = random.sample(list(movie_list.values()), 30)
    print("Movie List: ", list(random_list))
   
    # ask user to choose a movie
    print("Choose a movie you like the most from the list above: ")
    start_movie = input("Choice #1: ")
    return start_movie

## init current and previous movie
current_movie = None
previous_movie = None

## Takes a random walk on a graph given certain probabilities/weights 
## Records how often each node is visited and uses that to calculate probability of visiting each node
## inputs: movieGraph, start_movie (the node where the random walk in the graph will start),
## run_len (how many steps of the algorithm to run)
## returns: nodes_visited (a dictionary where key is the node and value is probability of visiting that node),
## movie_subgraph (a networkx graph of the ego network -- i.e. node and its neighbors -- of the current node in the simulation)
def personalized_PageRank(movieGraph, start_movie, run_len):

    ## weights of each type of edge 
    key_word_match = 1
    genre_match = 1
    director_match = 1

    global current_movie
    global previous_movie
    previous_movie = current_movie
    nodes_visited = {}

    start_movie_neighbors = list(movieGraph.neighbors(start_movie))
    
    # start traveler on movie generated above
    
    for i in range(run_len):
        if movieGraph.nodes[current_movie]['node_type'] == 'movie':
            nodes_list = list(movieGraph.neighbors(current_movie))
            nodes_list.append(current_movie)
            movie_subgraph = movieGraph.subgraph(nodes_list)
        else:
            nodes_list = []
            nodes_list.append(current_movie)
            movie_subgraph = movieGraph.subgraph(nodes_list)
        # generate random percentage
        percentage = np.random.random()
        # random walk from start movie
        if percentage > .15:
            out_edges = list(movieGraph.neighbors(current_movie))
            # send traveler to random node
            if len(out_edges) > 0:
                # choose randomly and send traveler to that node
                rand_idx = np.random.randint(len(out_edges))
                current_movie = out_edges[rand_idx]
                current_movie_neighbors = list(movieGraph.neighbors(current_movie))
                shared_elements = [value for value in start_movie_neighbors if value in current_movie_neighbors]

                # if movie has been visited
                if current_movie in nodes_visited.keys():
                    count = 0
                    for node in shared_elements:
                        element_attribute = movieGraph.nodes[node]['node_type']
                        if element_attribute == 'keyword':
                            node_freq = weighed_keyword_dict[node]
                            key_word_match = 1/ (node_freq)
                            count += key_word_match  
                        if element_attribute == 'director':
                            count += director_match  
                        if element_attribute == 'genre':
                            count += genre_match  

                    nodes_visited[current_movie] += count

               
                # if movie has NOT been visited
                else:
                    count = 0
                    for node in  shared_elements:
                        element_attribute = movieGraph.nodes[node]['node_type']
                        if element_attribute == 'keyword':
                            node_freq = weighed_keyword_dict[node]
                            key_word_match = 1/ (node_freq)
                            count += key_word_match  
                        if element_attribute == 'director':
                            count += director_match  
                        if element_attribute == 'genre':
                            count += genre_match  
                        
                    nodes_visited[current_movie] = count
                    
        else:
            current_movie = start_movie
            shared_elements = [value for value in start_movie_neighbors if value in start_movie_neighbors]

            if start_movie in nodes_visited.keys():
                count = 0
                for node in shared_elements:
                    element_attribute = movieGraph.nodes[node]['node_type']
                    if element_attribute == 'keyword':
                        node_freq = weighed_keyword_dict[node]
                        key_word_match = 1/ (node_freq)
                        count += key_word_match  
                    if element_attribute == 'director':
                        count += director_match  
                    if element_attribute == 'genre':
                        count += genre_match  
                        
                nodes_visited[current_movie] += count


                # if movie has NOT been visited
            else:
                count = 0
                for node in shared_elements:
                    element_attribute = movieGraph.nodes[node]['node_type']
                    if element_attribute == 'keyword':
                        node_freq = weighed_keyword_dict[node]
                        key_word_match = 1/ (node_freq)
                        count += key_word_match  
                    if element_attribute == 'director':
                        count += director_match 
                    if element_attribute == 'genre':
                        count += genre_match  
                        
                nodes_visited[current_movie] = count

                
     
    # calculating probability for each node being visited
    for node in movieGraph.nodes():
        # if node is in dictionary
        if node in nodes_visited.keys():
            nodes_visited[node] = nodes_visited[node] / run_len
        # if node is NOT in dictionary
        else:
            nodes_visited[node] = 0
            
    return nodes_visited, movie_subgraph

## get the movie the user likes 
start_movie = get_user_liked()

## set the current movie to the start movie the user choose 
current_movie = start_movie

## this list will store the movie recommendations
movies_to_sort = [] 

## define paramaters of the plot and define figure 
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()

## produce an animation of each step of the page rank algorithm 
## the function calls the page rank algorithm in each frame and draws the movie subgraph that it returns
## input: frame (the current frame in the algorithm)
def animate(frame):
   global start_movie
   global previous_movie
   fig.clear()
   nodes_visited, movie_subgraph = personalized_PageRank(movieGraph, start_movie, 1)
   ## label the central node red 
   color_map = ['blue' if node == previous_movie else 'orange' for node in movie_subgraph.nodes] 

   nx.draw(movie_subgraph, node_color=color_map, pos=nx.spring_layout(movie_subgraph))
   nx.draw_networkx_labels(movie_subgraph, verticalalignment = 'top', horizontalalignment='left', font_size=10, font_weight ='bold', pos=nx.spring_layout(movie_subgraph))

## run our page rank algorithm and get decent results
## we have this in addition to the animation because the animation takes long to run through thousands of steps 
## to run this code, comment out the animation code and look at results in console
nodes_visited, movie_subgraph = personalized_PageRank(movieGraph, start_movie, 10000)

## sort the nodes visited dict so that nodes with highest probability of being visited appear first
nodes_visited = dict(sorted(nodes_visited.items(), key=lambda node: node[1], reverse=True))

## launch the animation and show the plot
ani = animation.FuncAnimation(fig, animate, frames=100, interval=4000, repeat=True)
plt.show()

## get the top 10 nodes most likely to visit and add them to a list 
for node in nodes_visited:
    if len(movieGraph.nodes[node]) > 1:
        if movieGraph.nodes[node]['node_type'] == 'movie':
            movies_to_sort.append(node) 
                

## print out the 10 recommendations (top 10 nodes most likely to visit according to pagerank)
for movie in movies_to_sort[0:10]:
    print(movie, "\n")
     




    



