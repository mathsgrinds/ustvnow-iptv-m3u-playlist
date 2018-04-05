import sys
import requests
import cookielib
import re
import json
import os
import sys
import random
debug = False

# 22/03/18 - updated file to work with slightly altered api of ustvnow. - MikeC
##################################################################################################################
# CONFIG
##################################################################################################################

try:
    username = sys.argv[1]
except:
    username = ""                       # Set username manually here if not using the command line

try:
    password = sys.argv[2]
except:
    password = ""                       # Set username manually here if not using the command line

try:
    channel = sys.argv[3]
except:
    channel = "ALL"                     # Set channel manually here if not using the command line (use ALL to show all)

try:
    CreateSTRM = sys.argv[4]
except:
    CreateSTRM = False                  # Set if you would like to create the STRM file

try:
    hideTitle = sys.argv[4]             
except:
    hideTitle = True                    # For those of you who would like to hide the showing now show title
    
##################################################################################################################
## FUNCTIONS
##################################################################################################################

###########
# Decoder #
###########
def robust_decode(bs):
    '''Takes a byte string as param and convert it into a unicode one. First tries UTF8, and fallback to Latin1 if it fails'''
    bs.decode(errors='replace')
    cr = None
    try:
        cr = bs.decode('utf8')
    except UnicodeDecodeError:
        cr = bs.decode('latin1')
    return cr

###########
# Scraper #
###########
def Ustvnow(username, password, exclude=[]):
    result = ""
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
        if debug:
            print csrf
        ### Get Token ###
        url = "https://watch.ustvnow.com/account/login"
        payload = {'csrf_ustvnow': csrf, 'signin_email': username, 'signin_password':password, 'signin_remember':'1'}
        r = s.post(url, data=payload)
        html = r.text
        html = ' '.join(html.split())
        html = html[html.find('var token = "')+len('var token = "'):]
        html = html[:html.find(';')-1]
        token = str(html)
        if debug:
            print token
        ### Get Stream ###
        device = "gtv"        
        url = "http://m-api.ustvnow.com/"+device+"/1/live/login"
        payload = {'username': username, 'password': password, 'device':device}
        r = s.post(url, data=payload)
        html = r.text
        j = json.loads(html)
        if debug:
            print j
        if j['result'] != "success":
            if debug:
                print "error"
            return False
        url = "http://m-api.ustvnow.com/gtv/1/live/playingnow?token="+token
        if debug:
            print url
        r = s.get(url)
        html = r.text
        j = json.loads(html)
        if debug:
            print j        
        n = 0
        if channel=="ALL":
            result += "#EXTM3U\n"
        while True:
            try:
                scode = j['results'][n]['scode']
            except:
                break
            stream_code = j['results'][n]['stream_code']
            title = j['results'][n]['title']
            title = u' '.join((title,"")).encode('utf-8').strip()
            title = str(title)
            url = "http://m.ustvnow.com/stream/1/live/view?scode="+scode+"&token="+token+"&br_n=Firefox&pr=ec&tr=expired&pl=vjs&pd=1&br_n=Firefox&br_v=54&br_d=desktop"
            if debug:
                print url
            r = s.get(url)
            html = r.text
            try:
                i = json.loads(html)
                #URL = i["stream"].replace("\n","")[:-1]
                URL = i["stream"]
                #if "&jwt=" in URL:
                #    URL = URL.split("&jwt=")[0]
            except:
                break
            # Create STRM file
            if(CreateSTRM):
                fname = stream_code+".strm"
                if os.path.isfile(fname):
                    f= open(fname,"wb")
                    f.write(URL)
                    f.close
                else:
                    f= open(fname,"wb+")
                    f.write(URL)
                    f.close
            # Print Link
            if channel=="ALL":
                if robust_decode(stream_code) not in exclude:
                    if not hideTitle:
                        result += "#EXTINF:-1,"+robust_decode(stream_code)+" - "+robust_decode(title)+"\n"
                    else:
                        result += "#EXTINF:-1,"+robust_decode(stream_code)+"\n"                        
                    result += URL+"\n"
            else:
                if debug:
                    print stream_code
                if channel==stream_code:
                    result += URL+"\n"
                    break
            n += 1
        return(result.strip("\n"))

##################################################################################################################
## EXCLUDE THESE CHANNELS
##
## exclude = ["ABC", "My9" "FOX"] these channels would be excluded from the result
##
##################################################################################################################

exclude = []

##################################################################################################################
## MAIN
##################################################################################################################

if(username==""):
    #no username given, try predefined username and password
    usernames = ["jabt@mailed.ro","cslr@kotsu01.info","wdbt@pagamenti.tk","subt@o.cfo2go.ro","tbbt@kusrc.com","libt@uacro.com","cfbt@dfg6.kozow.com","ffbt@phpbb.uu.gl","nulr@at.mycamx.com","mcbt@fls4.gleeze.com","scbt@drivetagdev.com","uhbt@adrianou.gq","idbt@pagamenti.tk","kbbt@kazelink.ml","lcbt@inclusiveprogress.com","uvlr@at.mycamx.com","hbbt@4tb.host","wcbt@hukkmu.tk","jemt@w.0w.ro","pomr@aas.mycamx.com","jcbt@eqiluxspam.ga","adbt@fls4.gleeze.com","nbbt@4tb.host","nbbt@kusrc.com","ebbt@freemail.tweakly.net","rsp@themail.krd.ag","ecbt@hukkmu.tk","rcbt@kusrc.com","gfbt@urfey.com","ucbt@kusrc.com","ndbt@o.spamtrap.ro","cdbt@inclusiveprogress.com","hbbt@caseedu.tk","xgbt@117.yyolf.net","avbt@o.cfo2go.ro","pcbt@hukkmu.tk","edbt@u.dmarc.ro","adbt@eqiluxspam.ga","wdbt@drivetagdev.com","lrqr@mnode.me","ieas@mailfs.com","lebt@dff55.dynu.net","mibt@tvchd.com","qjbt@t.psh.me","cebt@hasanmail.ml","jdbt@eqiluxspam.ga","jdbt@arurgitu.gq","kebt@1clck2.com","pcbt@kusrc.com","hfbt@arur01.tk","yhbt@dfg6.kozow.com","ugbt@laoho.com","iott@szerz.com","fjlr@asm.snapwet.com","xfbt@dff55.dynu.net","wgmt@w.0w.ro","okbt@uacro.com","apps@wierie.tk","ahbt@rudymail.ml","ifbt@yordanmail.cf","bfas@mailfs.com","ffbt@getnowtoday.cf","cdbt@kusrc.com","sfbt@lpo.ddnsfree.com","eebt@cobarekyo1.ml","xdbt@c.andreihusanu.ro","lfbt@pagamenti.tk","zdbt@c.andreihusanu.ro","nfbt@pagamenti.tk","zfbt@lpo.ddnsfree.com","mhbt@rudymail.ml","mzut@oing.cf","lwbt@o.cfo2go.ro","rgbt@getnowtoday.cf","wdbt@bdmuzic.pw","ifbt@s.proprietativalcea.ro","gfbt@lpo.ddnsfree.com","ndbt@mailed.ro","egbt@ppetw.com","lgbt@xing886.uu.gl","lgbt@itmtx.com","dawt@lordsofts.com","cjbt@psles.com","ogbt@cutout.club","vdx@penoto.tk","spor@aw.kikwet.com","yfbt@barryogorman.com","dfbt@kazelink.ml","cjbt@hackersquad.tk","nylr@at.mycamx.com","hjbt@furusato.tokyo","ugbt@nezzart.com","qhbt@fls4.gleeze.com","ilbt@tvchd.com","apor@aw.kikwet.com","fibt@zhcne.com","ygbt@smallker.tk","zgbt@hukkmu.tk","bhbt@o.spamtrap.ro","zibt@itmtx.com","dibt@xing886.uu.gl","tlbt@psles.com","ngbt@e.milavitsaromania.ro","sibt@getnowtoday.cf","jgbt@arurgitu.gq","skbt@rudymail.ml","gibt@itmtx.com","scut@oing.cf","mpor@aw.kikwet.com","twbt@reddit.usa.cc","phbt@cutout.club","ifbt@freemail.tweakly.net","yex@penoto.tk","dmbt@tvchd.com","kijr@morriesworld.ml","qobt@uacro.com","cgbt@4tb.host","fjbt@laoho.com","tibt@p.9q.ro","nlmu@xww.ro","yibt@o.spamtrap.ro","ajbt@poliusraas.tk","wibt@lpo.ddnsfree.com","kkbt@hackersquad.tk","fzbt@o.cfo2go.ro","ikbt@glubex.com","xjbt@ppetw.com","fkbt@rkomo.com","qkmt@w.0w.ro","bhbt@i.xcode.ro","djbt@itmtx.com","hmbt@adrianou.gq","swlr@dwse.edu.pl","uhbt@4tb.host","uibt@e.milavitsaromania.ro","tkbt@zhcne.com","cibt@mail.ticket-please.ga","nibt@lpo.ddnsfree.com","rrpr@aw.kikwet.com","xkbt@zhcne.com","ahbt@kusrc.com","afx@penoto.tk","erut@toon.ml","wkbt@xing886.uu.gl","ngbt@taglead.com","hjbt@dff55.dynu.net","arpr@aw.kikwet.com","klbt@sroff.com","rmbt@phpbb.uu.gl","nlbt@sroff.com","munr@aas.mycamx.com","klbt@117.yyolf.net","xkjr@morriesworld.ml","skbt@e.blogspam.ro","yobt@tvchd.com","ulbt@vssms.com","npbt@uacro.com","ugx@penoto.tk","sbbt@o.cfo2go.ro","aobt@t.psh.me","zjbt@e.milavitsaromania.ro","tibt@mailed.ro","dkbt@dff55.dynu.net","wkbt@s.proprietativalcea.ro","csut@cetpass.com","qlbt@itmtx.com","egx@penoto.tk","bmbt@rkomo.com","mmbt@sroff.com","ribt@caseedu.tk","uomu@xww.ro","ljbt@cobarekyo1.ml","clbt@isdaq.com","fkbt@hasanmail.ml","unbt@dfg6.kozow.com","ijbt@smallker.tk","mnmt@v.0v.ro","albt@pagamenti.tk","rkbt@ucupdong.ml","xmbt@hezll.com","dobt@psles.com","stpr@aw.kikwet.com"]
    random.shuffle(usernames)
    for username in usernames:
        try:
            password = username
            result = Ustvnow(username, password, exclude)
            if result != False:
                break #success
        except:
            next #try again
else:
    result = Ustvnow(username, password, exclude)

print result

##################################################################################################################
