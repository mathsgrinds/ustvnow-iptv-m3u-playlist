import sys
import requests
import cookielib
import re
import json
import os

##################################################################################################################
username = ""
password = ""
##################################################################################################################
 
def Ustvnow(user, password):
    #START
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
        ### Get Token ###
        url = "https://watch.ustvnow.com/account/login"
        payload = {'csrf_ustvnow': csrf, 'signin_email': user, 'signin_password':password, 'signin_remember':'1'}
        r = s.post(url, data=payload)
        html = r.text
        html = ' '.join(html.split())
        html = html[html.find('var token = "')+len('var token = "'):]
        html = html[:html.find(';')-1]
        token = str(html)
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
            # Print Links
            scode = j['results'][n]['scode']
            stream_code = j['results'][n]['stream_code']
            title = j['results'][n]['title']
            print stream_code
            print title
            url = "http://m.ustvnow.com/stream/1/live/view?scode="+scode+"&token="+token+"&br_n=Firefox&br_v=54&br_d=desktop"
            r = s.get(url)
            html = r.text
            try:
                i = json.loads(html)
            except:
                break
            print "#EXTINF:-1,"+stream_code
            print i["stream"]+"\n"
            # Create STRM file
            fname = stream_code+".strm"
            if os.path.isfile(fname):
                f= open(fname,"w")
                f.write(i["stream"])
                f.close
            else:
                f= open(fname,"w+")
                f.write(i["stream"])
                f.close
            n += 1
        #END 
         
Ustvnow(username, password)
