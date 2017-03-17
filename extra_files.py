from bs4 import BeautifulSoup
import urllib.request
import glob

def get_top_djs():
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    url = "http://thedjlist.com/djs/genre/house/"
    headers={'User-Agent':user_agent,} 
    
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
#r = urllib.request.urlopen("http://thedjlist.com/djs/genre/house/").read()

    soup = BeautifulSoup(response)
    top_djs = [x.text.lower() for x in soup.contents[16].findAll("div", { "class" : "name-dj" })]
    url2 = "https://en.wikipedia.org/wiki/List_of_house_music_artists"
    headers={'User-Agent':user_agent,} 

    request=urllib.request.Request(url2,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
#r = urllib.request.urlopen("http://thedjlist.com/djs/genre/house/").read()

    soup = BeautifulSoup(response)
    top_djs += list(filter(lambda a: a != -1, [x.get("title",-1) for x in soup.contents[2].find_all('a')]))
    augmented_top_djs = []
    for dj in top_djs:
        dj = dj.strip()
        row = [
            dj,
            dj.replace(" ", "_"),
            dj.replace(" ", "-"),
            dj.replace(" ", ""),
        ]
        augmented_top_djs += row
    return augmented_top_djs


def extract_top_artists(top_artists, filename):
    if 'Classical_Guitar_classicalguitarmidi.com_MIDIRip' in filename:
        return False
    for dj in top_artists:
        if dj.lower() in filename.lower():
            return True
    return False


def get_midi_house_files(path):
    filenames = (glob.glob(path+"*/*.mid") 
             + glob.glob(path+"*/*.MID") 
             + glob.glob(path+"*/*/*.mid")
             + glob.glob(path+"*/*/*.MID"))
    augmented_top_djs = get_top_djs()
    reduced_files = filter(lambda a: extract_top_artists(augmented_top_djs, a),filenames)
    return list(reduced_files)