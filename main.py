import requests
import cookielib
from bs4 import BeautifulSoup
import json

######################################################################################################
# FUNCTIONS
######################################################################################################
def UstvnowToken(user, password):
    cj = cookielib.CookieJar()
    url = "http://m.ustvnow.com/iphone/1/live/login"
    payload = {'username': user, 'password': password, 'device':'gtv', 'redir':'0'}
    with requests.Session() as s:
        r = s.post(url, data=payload)
    html = r.text
    j = json.loads(html)
    return j['token']

def UstvnowSname(token, station, user, password):
    cj = cookielib.CookieJar()
    url = "http://m.ustvnow.com/iphone/1/live/login"
    payload = {'username': user, 'password': password, 'device':'gtv', 'redir':'0'}
    with requests.Session() as s:
        r = s.post(url, data=payload)
        R = s.get("http://m.ustvnow.com/iphone/1/live/playingnow")
    html = R.text
    try:
        soup = BeautifulSoup(html,"lxml")
    except:
        soup = BeautifulSoup(html)
    for tag in soup.findAll('div'):
        try:          
           sname = tag["sname"]
           if "content" in tag['id']:
               chunk = html[ html.find(sname) : html.find(sname) + 200 ]
               chunk = ' '.join(chunk.split())
               if "<h1>"+station+"</h1>" in chunk:
                   break
        except:
            pass
    url = "http://m.ustvnow.com/iphone/1/live/viewlive?streamname="+sname+"&stream_origin=ilv10.oedg.ustvnow.com&app_name=ilv10&token="+token+"&passkey=tbd&extrato=tbd"
    r = s.get(url)
    html =  r.text
    try:
        soup = BeautifulSoup(html,"lxml")
    except:
        soup = BeautifulSoup(html)
    link = "None"
    for tag in  soup.findAll('video'):
        link = str(tag['src'])
        return link

######################################################################################################
# LOGIN DETAILS
######################################################################################################
username = " Your USTVNOW Username  "
password = " Your USTVNOW Passoword "

######################################################################################################
# MAIN
######################################################################################################
token = UstvnowToken(username, password)
print "#EXTM3U\n"
for station in ["ABC", "CBS", "CW", "FOX", "NBC", "PBS", "My9"]:
    print "#EXTINF:-1," + station
    print UstvnowSname(token, station, username, password) + "\n"
