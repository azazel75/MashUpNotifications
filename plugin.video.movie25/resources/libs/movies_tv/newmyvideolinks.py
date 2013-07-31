import urllib,urllib2,re,cookielib,urlresolver,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
    
wh = watchhistory.WatchHistory('plugin.video.movie25')

def LISTSP2(murl):
        if murl=='3D':
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,5000)")
                main.addDir('Search Newmyvideolinks','movieNEW',102,art+'/search.png')
                check=main.OPENURL('http://www.myvideolinks.eu/category/movies/3-d-movies/')
                match=re.compile('<p><a href=".+?" >Next Page &raquo;</a></p>').findall(check)
                if len(match)>0:
                        urllist=main.OPENURL('http://www.myvideolinks.eu/category/movies/3-d-movies/')+main.OPENURL('http://www.myvideolinks.eu/category/movies/3-d-movies/page/2/')
                else:
                        urllist=main.OPENURL('http://www.myvideolinks.eu/category/movies/3-d-movies/')
        elif murl=='TV':
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,10000)")
                main.addDir('Search Newmyvideolinks','tvNEW',102,art+'/search.png')
                urllist=main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/2/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/3/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/4/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/5/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/6/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/7/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/8/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/9/')+main.OPENURL('http://www.myvideolinks.eu/category/tv-shows/page/10/')
        else:
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,10000)")
                main.addDir('Search Newmyvideolinks','movieNEW',102,art+'/search.png')
                urllist=main.OPENURL('http://www.myvideolinks.eu/category/movies/bluray/')+main.OPENURL('http://www.myvideolinks.eu/category/movies/bluray/page/2/')+main.OPENURL('http://www.myvideolinks.eu/category/movies/bluray/page/3/')+main.OPENURL('http://www.myvideolinks.eu/category/movies/bluray/page/4/')+main.OPENURL('http://www.myvideolinks.eu/category/movies/bluray/page/5/')+main.OPENURL('http://www.myvideolinks.eu/category/movies/bluray/page/6/')+main.OPENURL('http://www.myvideolinks.eu/category/movies/bluray/page/7/')+main.OPENURL('http://www.myvideolinks.eu/category/movies/bluray/page/8/')
        
        if urllist:
                urllist=main.unescapes(urllist)
                #link=main.OPENURL(xurl)
                match=re.compile("""<a href=".+?" rel=".+?" title=".+?"> <img src="(.+?)" width=".+?" height=".+?" title="(.+?)" class=".+?"></a><h4><a href="(.+?)" rel""").findall(urllist)

                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Movie list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Movies/Episodes Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                if len(match)>0:
                        for thumb,name,url in match:
                                if murl=='TV':
                                        match=re.compile('720p').findall(name)
                                        if (len(match)>0):
                                                main.addDirTE(name,url,35,thumb,'','','','','')
                                     
                                else:
                                        main.addDirM(name,url,35,thumb,'','','','','')
                                        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                                loadedLinks = loadedLinks + 1
                                percent = (loadedLinks * 100)/totalLinks
                                remaining_display = 'Movies/Episodes Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                                if (dialogWait.iscanceled()):
                                    return False   
 
        dialogWait.close()
        del dialogWait
        main.GA("HD-3D-HDTV","Newmyvideolinks")
        main.VIEWS()

def SearchhistoryNEW(murl):
        if murl == 'tvNEW':
            seapath=os.path.join(main.datapath,'Search')
            SeaFile=os.path.join(seapath,'SearchHistoryTv')
            if not os.path.exists(SeaFile):
                url='tvNEW'
                SEARCHNEW('',url)
            else:
                main.addDir('Search','tvNEW',101,art+'/search.png')
                main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
                thumb=art+'/link.png'
                searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
                for seahis in reversed(searchis):
                        url='tNEW'
                        seahis=seahis.replace('%20',' ')
                        main.addDir(seahis,url,101,thumb)
        elif murl == 'movieNEW':
            seapath=os.path.join(main.datapath,'Search')
            SeaFile=os.path.join(seapath,'SearchHistory25')
            if not os.path.exists(SeaFile):
                url='movieNEW'
                SEARCHNEW('',url)
            else:
                main.addDir('Search','movieNEW',101,art+'/search.png')
                main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
                thumb=art+'/link.png'
                searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
                for seahis in reversed(searchis):
                        url='mNEW'
                        seahis=seahis.replace('%20',' ')
                        main.addDir(seahis,url,101,thumb)
            

def SEARCHNEW(mname,murl):
        if murl == 'movieNEW':
                seapath=os.path.join(main.datapath,'Search')
                SeaFile=os.path.join(seapath,'SearchHistory25')
                try:
                    os.makedirs(seapath)
                except:
                    pass
                keyb = xbmc.Keyboard('', 'Search Movies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText()
                        encode=urllib.quote(search)
                        surl='http://www.myvideolinks.eu/index.php?s='+encode
                        if not os.path.exists(SeaFile) and encode != '':
                            open(SeaFile,'w').write('search="%s",'%encode)
                        else:
                            if encode != '':
                                open(SeaFile,'a').write('search="%s",'%encode)
                        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
                        for seahis in reversed(searchis):
                            print seahis
                        if len(searchis)>=10:
                            searchis.remove(searchis[0])
                            os.remove(SeaFile)
                            for seahis in searchis:
                                try:
                                    open(SeaFile,'a').write('search="%s",'%seahis)
                                except:
                                    pass
                link=main.OPENURL(surl)
                link=main.unescapes(link)
                match=re.compile("""<a href=".+?" rel=".+?" title=".+?"> <img src="(.+?)" width=".+?" height=".+?" title="(.+?)" class=".+?"></a><h4><a href="(.+?)" rel""").findall(link)
                if len(match)>0:
                    for thumb,name,url in match:
                            if not re.findall('HDTV',name):
                                main.addDirM(name,url,35,thumb,'','','','','')


                                
        elif murl == 'tvNEW':
                seapath=os.path.join(main.datapath,'Search')
                SeaFile=os.path.join(seapath,'SearchHistoryTv')
                try:
                    os.makedirs(seapath)
                except:
                    pass
                keyb = xbmc.Keyboard('', 'Search TV Shows')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText()
                        encode=urllib.quote(search)
                        surl='http://www.myvideolinks.eu/index.php?s='+encode
                        if not os.path.exists(SeaFile) and encode != '':
                            open(SeaFile,'w').write('search="%s",'%encode)
                        else:
                            if encode != '':
                                open(SeaFile,'a').write('search="%s",'%encode)
                        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
                        for seahis in reversed(searchis):
                            continue
                        if len(searchis)>=10:
                            searchis.remove(searchis[0])
                            os.remove(SeaFile)
                            for seahis in searchis:
                                try:
                                    open(SeaFile,'a').write('search="%s",'%seahis)
                                except:
                                    pass
                link=main.OPENURL(surl)
                link=main.unescapes(link)
                match=re.compile("""<a href=".+?" rel=".+?" title=".+?"> <img src="(.+?)" width=".+?" height=".+?" title="(.+?)" class=".+?"></a><h4><a href="(.+?)" rel""").findall(link)
                if len(match)>0:
                    for thumb,name,url in match:
                            main.addDirTE(name,url,35,thumb,'','','','','')


                
        else:
            if murl == 'tNEW':
                mname=mname.replace(' ','%20')
                encode = mname
                surl='http://www.myvideolinks.eu/index.php?s='+encode
                link=main.OPENURL(surl)
                link=main.unescapes(link)
                match=re.compile("""<a href=".+?" rel=".+?" title=".+?"> <img src="(.+?)" width=".+?" height=".+?" title="(.+?)" class=".+?"></a><h4><a href="(.+?)" rel""").findall(link)
                if len(match)>0:
                    for thumb,name,url in match:
                        if re.findall('HDTV',name):
                           main.addDirTE(name,url,35,thumb,'','','','','')

            elif murl == 'mNEW':
                mname=mname.replace(' ','%20')
                encode = mname
                surl='http://www.myvideolinks.eu/index.php?s='+encode
                link=main.OPENURL(surl)
                link=main.unescapes(link)
                match=re.compile("""<a href=".+?" rel=".+?" title=".+?"> <img src="(.+?)" width=".+?" height=".+?" title="(.+?)" class=".+?"></a><h4><a href="(.+?)" rel""").findall(link)
                if len(match)>0:
                    for thumb,name,url in match:
                            if not re.findall('HDTV',name):
                                main.addDirM(name,url,35,thumb,'','','','','')

        main.GA("Newmyvideolinks","Search")
        


def LINKSP2(mname,url):
        link=main.OPENURL(url)
        link=main.unescapes(link)
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        match=re.compile('<li><a href="h(.+?)">(.+?)</a></li>').findall(link)
        for murl, name in match:
                thumb=name.lower()
                murl='h'+murl
                hosted_media = urlresolver.HostedMediaFile(url=murl, title=name)
                match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
                for murl,host in match2:
                        main.addDown2(mname+' [COLOR blue]'+name+'[/COLOR]',murl,209,art+'/hosts/'+thumb+".png",art+'/hosts/'+thumb+".png")
       

def LINKSP2B(mname,murl):
        main.GA("Newmyvideolinks","Watched") 
        ok=True
        r = re.findall('(.+?)\ss(\d+)e(\d+)\s',mname,re.I)
        if r:
            infoLabels =main.GETMETAEpiT(mname,'','')
            video_type='episode'
            season=infoLabels['season']
            episode=infoLabels['episode']
        else:
            infoLabels =main.GETMETAT(mname,'','','')
            video_type='movie'
            season=''
            episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        hosted_media = urlresolver.HostedMediaFile(murl)
        source = hosted_media
        try :
                if source:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                        stream_url = source.resolve()
                else:
                      stream_url = False
                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=infoLabels['title'],season=season, episode=episode, year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]NewmyVideoLink[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=infoLabels['cover_url'], fanart=infoLabels['backdrop_url'], is_folder=False)
                player.KeepAlive()
                return ok
        except:
                return ok
            

def UFCNEW():
        try: 
                urllist=['http://www.myvideolinks.eu/index.php?s=ufc']
        except:
                urllist=['http://www.myvideolinks.eu/index.php?s=ufc']
        for surl in urllist:
                link=main.OPENURL(surl)
                link=main.unescapes(link)
                match=re.compile("""<a href=".+?" rel=".+?" title=".+?"> <img src="(.+?)" width=".+?" height=".+?" title="(.+?)" class=".+?"></a><h4><a href="(.+?)" rel""").findall(link)
                if len(match)>0:
                        for thumb,name,url in match:
                                match=re.compile('UFC').findall(name)
                                if len(match)>0:
                                        main.addDir(name,url,35,thumb)

        main.GA("Newmyvideolinks","UFC")

