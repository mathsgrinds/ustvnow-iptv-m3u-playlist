# ustvnow-iptv-m3u-playlist


## About:
Using your login details this script can grab the m3u8 links from the USTVNOW website. It's nothing fancy, I made it because the current scripts out there don't work! And I wanted to watch American TV via an IPTV client rather than via a website or addon. Running this script with print out the video links. Enjoy :)


## CLI Usage Examples:


### Get link for CBS


python ustvnow-iptv-m3u-playlist.py 'username' 'password' 'CBS';


### Get link for ALL stations


python ustvnow-iptv-m3u-playlist.py 'username' 'password' 'ALL';

### Get link for ALL stations with strm


python ustvnow-iptv-m3u-playlist.py 'username' 'password' 'ALL' 'True';


### Non Command Line Interface


It is possible just to input the username and passwords into the python file and generate playlists and strm files

### TL;DR


Just run it (double-click the python .py file)