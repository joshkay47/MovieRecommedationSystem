from flask import current_app
import matplotlib.pyplot as plt
from matplotlib import animation
import networkx as nx
from csv import reader
import pandas as pd
import random
from random import sample
import numpy as np

from pyvis import network as net
from pyvis.network import Network
from IPython.display import display, HTML

from pyvis import network as net
from IPython.display import display, HTML

net = Network()


keywords_path = "Downloads/keywords.csv/keywords.csv"
movies_metadata_path = "Downloads/movies_metadata.csv/movies_metadata.csv"
credits_path = "Downloads/credits.csv/credits.csv"
saved_movie_path = "movieGraph.graphml"


movie_list = {}

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
                ##print(count)
                if count == num_movies:
                    break 

            else:
                firstRow = False 
                

    print(movieGraph.nodes)       
    return movieGraph
            

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
        if key in movie_list:
            movieID = str(key)
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


def readKeywords(keywords_path, movieGraph):

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
        count +=1
        if key in movie_list:
            movieID = str(key)
            movieNode = movie_list[movieID]
            print(movieNode)
            nodeInfo = {}
            nodeInfo["node_type"] = "movie"

            nodeDict[movieNode] = nodeInfo
            keywords_list = keywords_dict[key]
            for keyword in keywords_list:
                movieGraph.add_edge(movieNode, keyword)

        if count == num_keywords:
            break
            
            
    nx.set_node_attributes(movieGraph, nodeDict)

def readDirectors(credits_path, movieGraph):

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
            
        
        
def addDirectorEdges(movieGraph, director_dict, all_directors, num_directors):
    count = 0
    
    nodeDict = {}


    for director in all_directors:
        movieGraph.add_node(director) 
        nodeInfo = {}
        nodeInfo["node_type"] = "keyword"

        nodeDict[director] = nodeInfo
        
    for key in director_dict.keys():
        count +=1
        if key in movie_list:
            movieID = str(key)
            movieNode = movie_list[movieID]
            nodeInfo = {}
            nodeInfo["node_type"] = "movie"
            nodeDict[movieNode] = nodeInfo
            for director in director_dict[key]:
                movieGraph.add_edge(movieNode, director)

        if count == num_directors:
            break
            
    nx.set_node_attributes(movieGraph, nodeDict)

movieGraph = readMovies(movies_metadata_path, 1000)

genre_dict, all_genres = readGenres(movies_metadata_path) 

addGenreEdges(movieGraph, genre_dict, all_genres, 1000)

keywords_dict, all_keywords = readKeywords(keywords_path, movieGraph)

addKeywordsEdges(movieGraph, keywords_dict, all_keywords, 1000)

director_dict, all_directors = readDirectors(credits_path, movieGraph)

addDirectorEdges(movieGraph, director_dict, all_directors, 1000) 

movieGraph = nx.read_graphml(saved_movie_path)


movieList = list(movieGraph.nodes) 

##print (len(movieList))


def get_user_liked():
    user_choice_list = {}
    # get random list from database to present to user
    random_list = random.sample(list(movie_list.values()), 30)
    print("Movie List: ", list(random_list))
   
    # ask user to choose three
    print("Choose a movie you like the most from the list above: ")
    start_movie = input("Choice #1: ")
    ##input2 = input("Choice #2: ")
    ##input3 = input("Choice #3: ")
   
    # take user input and add to list
    ##user_choice_list[input1] = movie_list[input1]
    ##user_choice_list[input2] = movie_list[input2]   
    ##user_choice_list[input3] = movie_list[input3]
    
   ## sample_list = [] 
    
    ##for movie in random_list:
      ##  if movie in user_choice_list:
       ##     sample_list.append(movie) 
    
    ##start_movie_id = movie_list[start_movie] 
    
   ## print (start_movie)
    
    ##print("start movie: ", start_movie[1]) 
   
    return start_movie

## init current movie
current_movie = None




# personalized PageRank algorithm
def personalized_PageRank(movieGraph, start_movie, run_len):
    global current_movie
    nodes_visited = {}
    ##keys = list(movie_list.values())
    ##movie_index = keys.index(current_movie)


    ##movie_graph_list = list(movieGraph.nodes)
    
    # start traveler on movie generated above
    #current_movie = start_movie
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
               
                # if movie has been visited
                if current_movie in nodes_visited.keys():
                    nodes_visited[current_movie] += 1
               
                # if movie has NOT been visited
                else:
                    nodes_visited[current_movie] = 1
                    
        else:
             # if movie has been visited
                if start_movie in nodes_visited.keys():
                    nodes_visited[start_movie] += 1
               
                # if movie has NOT been visited
                else:
                    nodes_visited[start_movie] = 1

                current_movie = start_movie
     
    # calculating probability for each node being visited
    for node in movieGraph.nodes():
        # if node is in dictionary
        if node in nodes_visited.keys():
            nodes_visited[node] = nodes_visited[node] / run_len
        # if node is NOT in dictionary
        else:
            nodes_visited[node] = 0
            
    return nodes_visited, movie_subgraph


##print(list(movieGraph.nodes))

start_movie = get_user_liked()

current_movie = start_movie

##print(start_movie)

movies_to_sort = [] 

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig = plt.figure()
onMovie = True 

def animate(frame):
   global start_movie
   fig.clear()
   nodes_visited, movie_subgraph = personalized_PageRank(movieGraph, start_movie, 1)
   nx.draw(movie_subgraph, with_lables=True)

nodes_visited, movie_subgraph = personalized_PageRank(movieGraph, start_movie, 1)
nodes_visited = dict(sorted(nodes_visited.items(), key=lambda node: node[1], reverse=True))
ani = animation.FuncAnimation(fig, animate, frames=100, interval=1000, repeat=True)

plt.show()

##print(nodes_visited)



##print (nodes_visited)


for node in nodes_visited:
    ##print ("node visited " + nodes_visited[node])
    
    if len(movieGraph.nodes[node]) > 1:
        if movieGraph.nodes[node]['node_type'] == 'movie':
            movie_title = movieGraph.nodes[node]["movie_title"]  
            movies_to_sort.append(movie_title) 
                
        
##print(nodes_visited)

##print(movies_to_sort) 


##movies_to_sort = sorted(movies_to_sort, key=lambda movie: nodes_visited[movie_list[movie]]) 


print(movies_to_sort[0:10])   



##net.from_nx(movie_subgraph)

    



