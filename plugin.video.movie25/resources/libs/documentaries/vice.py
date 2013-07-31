import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urlresolver
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art   
wh = watchhistory.WatchHistory('plugin.video.movie25')



def Vice(murl):
    main.GA("Documentary","Vice")
    link=main.OPENURL(murl)
    match=re.compile('<a href="(.+?)"><img width=".+?" height=".+?" src="(.+?)" /></a>    <h2><a href=".+?">(.+?)</a></h2>\n    <p>(.+?)</p>').findall(link)
    for url,thumb,name,desc in match:
        url='http://www.vice.com'+url
        main.addDirc(name,url,105,thumb,desc,'','','','')

def ViceList(murl):
    main.GA("Vice","Vice-list")
    link=main.OPENURL(murl)
    match=re.compile('<img src="(.+?)" alt="" width=".+?" height=".+?">\n                    <span class=".+?"></span>\n            </a>\n    <h2><a onClick=".+?" href="(.+?)">(.+?)</a></h2>').findall(link)
    for thumb,url,name in match:
        url='http://www.vice.com'+url
        main.addPlayMs(name,url,106,thumb,'','','','','')

def ViceLink(mname,murl,thumb2):
    main.GA("Vice","Watched")
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Playing Link,5000)")
    link=main.OPENURL(murl)
    ok=True
    desci=re.compile('<meta name="description" content="(.+?)" />').findall(link)
    if len(desci)>0:
        desc=desci[0]
    else:
        desc=''
    thumbi=re.compile('<meta property="og:image" content="(.+?)" />').findall(link)
    if len(thumbi)>0:
        thumb=thumbi[0]
    else:
        thumb=''
    match=re.compile('content="http://player.ooyala.com/player.swf.?embedCode=(.+?)&keepEmbedCode=true&autoplay=1"').findall(link)
    if len(match)>0:
        
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        durl='http://player.ooyala.com/player/ipad/'+match[0]+'.m3u8'
        link2=main.OPENURL(durl)
        match=re.compile('http://(.+?).m3u8').findall(link2)
        if len(match)==0:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Cannot Be Played,5000)")
        else:
            if selfAddon.getSetting("vice-qua") == "0":
                try:
                    stream_url = 'http://'+match[3]+'.m3u8'
                except:
                    stream_url = 'http://'+match[0]+'.m3u8'
            elif selfAddon.getSetting("vice-qua") == "1":
                try:
                    stream_url = 'http://'+match[0]+'.m3u8'
                except:
                    stream_url = 'http://'+match[2]+'.m3u8'
            else:
                    stream_url = durl
                
            infoL={ "Title": mname, "Plot": desc}
            # play with bookmark
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='', title=mname,season='', episode='', year='',img=thumb,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id='')
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                wh.add_item(mname+' '+'[COLOR green]Vice[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
            player.KeepAlive()
            return ok
    
    match2=re.compile('content="http://www.youtube.com/v/(.+?)" />').findall(link)
    if len(match2)>0:
        url='http://www.youtube.com/watch?v='+match2[0]
        
        media = urlresolver.HostedMediaFile(str(url))
        source = media
        listitem = xbmcgui.ListItem(mname)
        if source:
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                stream_url = source.resolve()
                if source.resolve()==False:
                        xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Cannot Be Resolved,5000)")
                        return
        else:
              stream_url = False  
        # play with bookmark
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='', title=mname,season='', episode='', year='',img=thumb,infolabels='', watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id='')
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]Vice[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb2, fanart='', is_folder=False)
        player.KeepAlive()
        return ok
