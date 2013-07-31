# -*- coding: cp1252 -*-
import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urlresolver
from t0mm0.common.net import Net
net = Net()
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
    
wh = watchhistory.WatchHistory('plugin.video.movie25')


def MAINFMA():
        main.GA("Plugin","FMA")
        main.addDir('Search','http://www.fma.com',646,art+'/wfs/search.png')
        main.addDir('All Movies','movies',570,art+'/wfs/az.png')
        main.addDir('Latest','http://www.freemoviesaddict.com/',568,art+'/wfs/latest2.png')
        main.addDir('Genre','genre',571,art+'/wfs/genre.png')
        main.addDir('Year','year',571,art+'/wfs/year.png')

def SearchhistoryM():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        if not os.path.exists(SeaFile):
            url='ws'
            SEARCHM(url)
        else:
            main.addDir('Search','ws',647,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,647,thumb)
            
            


def SEARCHM(murl):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'ws':
            keyb = xbmc.Keyboard('', 'Search For Shows or Episodes')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
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


        else:
            encode = murl
        search_url = 'http://www.freemoviesaddict.com/search'
        search_content = net.http_POST(search_url, { 'search_term' : encode} ).content
        r=main.unescapes(search_content)
        match=re.compile('<img class=\'.+?\' src=\'(.+?)\' alt=\'.+?\' />.+?<a class=\'.+?\' href=\'/(.+?)\'>(.+?)</a>.+?<a href=\'/movies/year/.+?\'>(.+?)</a>.+?<a href=\'/movies/genre/.+?\'>(.+?)</a>.+?</span><span class=".+?">(.+?)</span>').findall(r)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for thumb,url,name, year, gen, desc in match:
                main.addPlayM(name,'http://www.freemoviesaddict.com/'+url,569,thumb,desc,'','',gen,year)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                    return False   
        dialogWait.close()
        del dialogWait
        main.GA("FMA","Search")

def AtoZFMA():
        main.addDir('0-9','http://www.freemoviesaddict.com/movies/letter/123',568,art+'/wfs/09.png')
        for i in string.ascii_uppercase:
                main.addDir(i,'http://www.freemoviesaddict.com/movies/letter/'+i,568,art+'/wfs/'+i+'.png')
        main.GA("FMA","A-Z")
        main.VIEWSB()

def GENREFMA(murl):
        url='http://www.freemoviesaddict.com/'
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        if murl=='genre':
            thumb=art+'/folder.png'
            match=re.compile('<li><a href="/movies/genre/(.+?)">(.+?)</a></li>').findall(link)
            for url, name in match:
                main.addDir(name,'http://www.freemoviesaddict.com/movies/genre/'+url,568,thumb)
            ("FMA","Genre")
        if murl=='year':
            thumb=art+'/folder.png'
            match=re.compile('<li><a href="/movies/year/(.+?)">(.+?)</a></li>').findall(link)
            for url, name in match:
                main.addDir(name,'http://www.freemoviesaddict.com/movies/year/'+url,568,thumb)
            ("FMA","Year")
    
def LISTFMA(murl):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('<img class=\'.+?\' src=\'(.+?)\' alt=\'.+?\' />.+?<a class=\'.+?\' href=\'/(.+?)\'>(.+?)</a>.+?<a href=\'/movies/year/.+?\'>(.+?)</a>.+?<a href=\'/movies/genre/.+?\'>(.+?)</a>.+?</span><span class=".+?">(.+?)</span>').findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for thumb,url,name, year, gen, desc in match:
        main.addPlayM(name,'http://www.freemoviesaddict.com/'+url,569,thumb,desc,'','',gen,year)
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False   
    dialogWait.close()
    del dialogWait
    paginate = re.compile('<span class="pagination_next"><a class="pagination_link" href="(.+?)">').findall(link)
    if len(paginate)>0:
        main.addDir('Next','http://www.freemoviesaddict.com/'+paginate[0],568,art+'/next2.png')
    main.GA("FMA","list")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    main.VIEWS()



def LINKFMA(mname,murl,thumb,desc):
        main.GA("FMA","Watched")
        sources = []
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting hosts,3000)")
        infoLabels =main.GETMETAT(mname,'','',thumb)
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<span class=\'.+?\'>(.+?)</span></p><div class=\'.+?\'><img src=\'.+?\' /></div><a class=\'.+?\' href="(.+?)"').findall(link)
        for host, url in match:
                durl='http://www.freemoviesaddict.com/'+url
                redirect=main.REDIRECT(durl)
                hosted_media = urlresolver.HostedMediaFile(url=redirect, title=host)
                sources.append(hosted_media)
                
        if (len(sources)==0):
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Show doesn't have playable links,5000)")
      
        else:
                source = urlresolver.choose_source(sources)
        try:
                if source:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving links,3000)")
                        stream_url = source.resolve()
                else:
                      stream_url = False
                      return
                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]FMA[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
                player.KeepAlive()
                return ok
        except:
                return ok
