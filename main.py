import sys
import requests
import cookielib
import re
import json

##################################################################################################################
# If you put your username and password here then the script will run automatically and not require an input.
username = ""
password = ""
free_or_all = "free"
##################################################################################################################
 
def Ustvnow(user, password, free_or_all = "free"):
    stations=["ABC", "CBS", "CW", "FOX", "NBC", "PBS", "My9"]
    if free_or_all == 'all':
        stations.extend(["AETV", "AMC", "Animal Planet", "Bravo", "Cartoon Network", "CNBC", "CNN", "Comedy Central", "Discovery Channel", "ESPN", "Fox News Channel", "FX", "History", "Lifetime", "National Geographic Channel", "Nickelodeon", "SPIKE TV", "Syfy", "TBS", "TNT", "USA"])
   
    with requests.Session() as s:
        ### Get CSRF Token ###       
        url="https://watch.ustvnow.com/account/signin"
        r = s.get(url)
        html = r.text
        html = ' '.join(html.split())
        ultimate_regexp = "(?i)<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)\/?>"
        for match in re.finditer(ultimate_regexp, html):
            i = repr(match.group())
            if '<input type="hidden" name="csrf_ustvnow" value="' in i:
                csrf = i.replace('<input type="hidden" name="csrf_ustvnow" value="','').replace('">','')
                csrf = str(csrf).replace("u'","").replace("'","")
        ### Done ###

        ### Get Token ###
        url = "https://watch.ustvnow.com/account/login"
        payload = {'csrf_ustvnow': csrf, 'signin_email': user, 'signin_password':password, 'signin_remember':'1'}
        r = s.post(url, data=payload)
        html = r.text
        html = ' '.join(html.split())
        html = html[html.find('var token = "')+len('var token = "'):]
        html = html[:html.find(';')-1]
        token = str(html)
        ### Done ###

        ### Get Stream ###
        device = "gtv"        
        url = "http://m-api.ustvnow.com/"+device+"/1/live/login"
        payload = {'username': user, 'password': password, 'device':device}
        r = s.post(url, data=payload)
        html = r.text
        j = json.loads(html)
        result = j['result']
        url = "http://m-api.ustvnow.com/gtv/1/live/playingnow?token="+token
        r = s.get(url)
        html = r.text
        j = json.loads(html)
        n = 0
        print "#EXTM3U\n"
        while True:
            try:
                scode = j['results'][n]['scode']
                stream_code = j['results'][n]['stream_code']
                if stream_code in stations:
                    url = "http://m.ustvnow.com/stream/1/live/view?scode="+scode+"&token="+token+"&br_n=Firefox&br_v=54&br_d=desktop"
                    r = s.get(url)
                    html = r.text
                    i = json.loads(html)
                    print "#EXTINF:-1,"+stream_code
                    print i["stream"]+"\n"
                    n += 1
            except:
                break
        ### Done ###
        
Ustvnow(username, password, free_or_all)
