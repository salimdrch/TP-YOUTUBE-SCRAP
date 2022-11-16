import argparse
from ast import arg
from email import parser
from tkinter.tix import Tree
from webbrowser import get
from bs4 import BeautifulSoup as bs
import re
import json as json  
from requests_html import HTMLSession   
import requests
import pandas as pd
import argparse

# return data of json file
def json_to_dataframe(filename):
    videosID = pd.read_json(filename)
    print(f"\n{videosID.head()}\n")
    return videosID

# push data to json file
def dict_to_json(filename, dict):
    with open(filename, "w") as fp:
        json.dump(dict,fp, indent=4)

# get title of video
def title_of_video(soup):
    return soup.title.text

# get videaste of video
def videaste_of_video(soup):
    return soup.find("meta", property="og:video:tag")['content']

# get videoID of video
def videoId_of_video(soup):
    return soup.find("meta",itemprop="videoId")['content']

# get like of video
def likes_of_video(soup):
    # Récupérer le nombre de like
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
    data_json = json.loads(data) 
    videoPrimaryInfoRendererBuilder = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents']

    indice = 0
    if 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[0]:
        indice = 0
    elif 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[1]:
        indice = 1
    else :
        indice = 2

    videoPrimaryInfoRenderer = videoPrimaryInfoRendererBuilder[indice]['videoPrimaryInfoRenderer']
    #videoSecondaryInfoRenderer = videoPrimaryInfoRendererBuilder[(indice + 1)]['videoSecondaryInfoRenderer'] 

    likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']
    likes_str = likes_label.split(' ')[0].replace(' ','')  # on supprime les espaces
    likes_tab = re.findall('\d+', likes_str) # on recupères les chiffres 
    likes = ""
    for e in likes_tab:
        likes = likes + e

    return likes

# get description of video
def description_of_video(soup):
    pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
    return pattern.findall(str(soup))[0].replace('\n','\n')

# get descriptionUrl of video
def description_url_of_video(soup):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', description_of_video(soup))

def get_soup(id): 
    url = "https://www.youtube.com/watch?v=" + id
    session = HTMLSession()  
    response = session.get(url)  
    response.html.render(timeout=30)  
    soup = bs(response.html.html, "html.parser")  
    page = requests.get(url)
    soup = bs(page.text, "html.parser")
    return soup


def get_data_video(id):
    soup = get_soup(id)
    print(soup.title.text)
    # Dictionnaire de donnée
    result = {}
    result["title"] = title_of_video(soup)
    result["videaste"] = videaste_of_video(soup)
    result["video_id"] =  videoId_of_video(soup) 
    result["likes"] = likes_of_video(soup)
    result["description"] = description_of_video(soup)
    result["description_url"] = description_url_of_video(soup)
    return result


def get_page(id): 
    url = "https://www.youtube.com/watch?v=" + id
    session = HTMLSession()  
    response = session.get(url)  
    response.html.render(timeout=30)  
    soup = bs(response.html.html, "html.parser")  
    page = requests.get(url)
    toto = page.status_code # si = 200 page chargé vec succes
    return toto
