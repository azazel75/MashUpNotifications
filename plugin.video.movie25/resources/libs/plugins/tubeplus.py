import urllib, urllib2, re, string, urlparse, sys,   os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, HTMLParser
from resources.libs import main
from t0mm0.common.addon import Addon

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)

    
art = main.art
error_logo = art+'/bigx.png'

try:
    import urllib, urllib2, re, string, urlparse, sys, os
    
    from t0mm0.common.net import Net
    from metahandler import metahandlers
    from sqlite3 import dbapi2 as database
    from universal import playbackengine, watchhistory
    import urlresolver
except Exception, e:
    addon.log_error(str(e))
    addon.show_small_popup('MashUP: tubePLUS','Failed To Import Modules', 5000, error_logo)
    addon.show_ok_dialog(['Failed To Import Modules','Please Post Logfile In MashUP Forum @','http://www.xbmchub.com'],
                          'MashUP: TV-Release')
net = Net()
BASE_URL = 'http://www.tubeplus.me/'
wh = watchhistory.WatchHistory(addon_id)




def MAINMENU():
    main.addDir('Search',    BASE_URL+'?s=',1024,art+'/tpsearch.png')
    main.addDir('TV Shows',BASE_URL,1021,art+'/tptvshows.png')
    main.addDir('Movies',BASE_URL,1022,art+'/tpmovies.png')
    #main.addDir('TubePLUS Movie Charts','http://www.tubeplus.me/tool/',1023,'')
    main.addPlayc('Resolver Settings',BASE_URL,1004,art+'/tpsettings.png','','','','','')
    main.VIEWSB()


def TVMENU():
    main.addDir('[COLOR=FF67cc33][B]Last Aired TV Shows/Episodes[/B][/COLOR]',BASE_URL,1042,'')
    main.addDir('[COLOR=FF67cc33][B]All latest Aired TV Shows/Episodes[/B][/COLOR]',BASE_URL+'browse/tv-shows/Last/ALL/',1041,'')
    main.addDir('[COLOR=FF67cc33][B]Top 10 Tv Episodes[/B][/COLOR]',BASE_URL,1043,'')
    main.addDir('[COLOR=FF67cc33][B]TV Shows by Genres[/B][/COLOR]',BASE_URL+'browse/tv-shows/',1044,'')
    main.addDir('[COLOR=FF67cc33][B]TV Shows A to Z[/B][/COLOR]',BASE_URL,'mode','')
    #main.addDir('[COLOR=FF67cc33][B]S[/B]earch TV Shows[/COLOR]',BASE_URL+'search/','mode','')

def MOVIE_MENU():
    html = main.OPENURL2(BASE_URL)
    r = re.findall(r'<h1 id="list_head" class="short">&nbsp;&nbsp;&nbsp;(.+?)</h1>',html)
    for movies_special in r:
        main.addDir('[COLOR=FF67cc33]'+movies_special+'[/COLOR]',BASE_URL,1040,'')
    main.addDir('[COLOR=FF67cc33][B]Most Popular Movies[/B][/COLOR]',BASE_URL+'browse/movies/Last/ALL/','mode','')
    main.addDir('[COLOR=FF67cc33][B]Movies By Genres[/B][/COLOR]',BASE_URL+'browse/movies/',1044,'')
    main.addDir('[COLOR=FF67cc33][B]Most Popular Genres[/B][/COLOR]',BASE_URL,'mode',art+'/tpmostpopgenre.png')
    main.addDir('[COLOR=FF67cc33][B]Movies by A to Z[/B][/COLOR]',BASE_URL+'browse/movies/','1047','')
    


def TV_TOP10(url):
    html = main.OPENURL2(url)
    if html == None:
        return
    r = re.findall('Top 10 TV Episodes</h1>(.+?)&laquo;More TV Shows&raquo;', html, re.M|re.DOTALL)
    pattern  = '<a target="_blank" title="Watch online: (.+?)".+?href="/(.+?)"><img'
    r = re.findall(r''+pattern+'', str(r), re.M|re.DOTALL)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(r)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    
    for tname, url in r:
        r = re.findall(r'\d+/(.+?)/season_(\d+)/episode_(\d+)/', url)
        for name, season, episode in r:
            name = name.replace('_', ' ')
            name = name.strip()+' Season '+season.strip()+' Episode '+episode.strip()+' ('+season.strip()+'x'+episode.strip()+')'
        if ':' in name:
            name = re.findall('(.+?)\:', name)[0]
            name = name.strip()+' Season '+season.strip()+' Episode '+episode.strip()+' ('+season.strip()+'x'+episode.strip()+')'
        main.addDirTE(name.replace('.',''),url,1026,'','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()

            
def LAST_AIRED(url):
    html = main.OPENURL2(url)
    html = html.decode('ISO-8859-1').encode('utf-8', 'ignore')
    if html == None:
        return
    r = re.findall(r'Last Aired TV Shows/Episodes</div>(.+?)&laquo;Browse all latest TV Episodes&raquo;',html, re.M|re.DOTALL)[0]
    pattern = 'href="/(player.+?)">'
    r = re.findall(r''+pattern+'', r, re.M|re.DOTALL)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(r)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for url in r:
        r = re.findall(r'player/\d+/(.+?)/season_(\d+)/episode_(\d+)/.+?/',url)#.replace('_', ' ')
        for name, season, episode in r:
            name = name.replace('_', ' ')
            name = name.strip()+' Season '+season.strip()+' Episode '+episode.strip()+' ('+season.strip()+'x'+episode.strip()+')'
        if ':' in name:
            name = re.findall('(.+?)\:', name)[0]
            name = name.strip()+' Season '+season.strip()+' Episode '+episode.strip()+' ('+season.strip()+'x'+episode.strip()+')'
        main.addDirTE(name.replace('.',''),url,1026,'','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()
        

def LATEST_TV(url):
    html = main.OPENURL2(url)
    html = html.replace('&rsquo;',"'")
    if html == None:
        return
    pattern  = '<a target="_blank" title="Watch online: (.+?)"'#name
    pattern += '.+?href="/(player/.+?)"><img.+?'#url
    r = re.findall(r''+pattern+'',html, re.I|re.M|re.DOTALL)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(r)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for name, url in r:
        r = re.findall(r'(.+?) - Season: (\d+) Episode: (\d+)  -', name)
        for  name, season, episode in r:
            name = name.strip()+' Season '+season.strip()+' Episode '+episode.strip()+' ('+season.strip()+'x'+episode.strip()+')'
        if ':' in name:
            name = re.findall('(.+?)\:', name)[0]
            name = name.strip()+' Season '+season.strip()+' Episode '+episode.strip()+' ('+season.strip()+'x'+episode.strip()+')'
        main.addDirTE(name.replace('.',''),url,1026,'','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()

def GENRES(url):
    Curl = url
    html = main.OPENURL2(url)
    if html == None:
        return
    r = re.findall(r'{value:1, te(.+?)var selected_genre', html, re.M)
    pattern = 'xt: "(.+?)"'
    r = re.findall(r''+pattern+'', str(r), re.I|re.DOTALL)
    res_genre = []
    res_url = []
    for genre in r:
        res_genre.append(genre.encode('utf8'))
        res_url.append(genre.encode('utf8'))
    dialog = xbmcgui.Dialog()
    ret = dialog.select('Choose Genre', res_genre)
    if ret == -1:
        return
    elif ret >= 0:
        genre = res_url [ret - 0]
        url = url+genre+'/ALL/'
    try:
        html = main.OPENURL2(url)
        #html = html.replace('xc2\x92', "'")
        if html == None:
            print 'html None'
            return
    except:#Mash can you add your error calling function
        pass#remove the pass and add call to your error routine
    r = re.findall(r'Alphabetically \[\<b\>'+genre+', ALL\<\/b\>\]\<\/div\>(.+?)\<div id=\"list_footer\"\>\<\/div\>', html, re.I|re.M|re.DOTALL)
    pattern = '<div class="left">.+?<a target="_blank" title="Watch online: (.+?)" href="/(.+?)">'
    r = re.findall(pattern, str(r), re.I|re.M|re.DOTALL)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(r)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    
    for name, url in r:
        url = BASE_URL+url
        if 'tv-shows' in Curl:
             main.addDir(name, url, '1042','')

        else:
            name = name.replace('\\','').replace('xc2x92','')
            main.addDirM(name,url,'mode','','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()
    if re.findall(r'<div id="paging">', html):
        r = re.findall('\<li title="Page (\d+)"\>.+?"\>(\d+)(?=\<\/a\>\<\/li\>\<li title="Next Page"\>\<a href="/(.+?)")',html)
        for current, total, npurl in r:
            name = '[COLOR=FF67cc33]Page '+current+' of '+total+', Next Page >>>[/COLOR]'
            main.addDir(name, BASE_URL+url, '', art+'/nextpage.png')
            url = url+':'+total
            name = '[COLOR=FF67cc33]Goto Page[/COLOR]'
            main.addDir(name, url, 1002, art+'/gotopagetr.png')
    main.VIEWS()
            
def SEARCHhistory():
    dialog = xbmcgui.Dialog()
    ret = dialog.select('[COLOR=FF67cc33][B]Choose A Search Type[/COLOR][/B]',['[B][COLOR=FF67cc33]TV Shows[/COLOR][/B]','[B][COLOR=FF67cc33]Movies[/COLOR][/B]'])
    if ret == -1:
        return MAINMENU()
    if ret == 0:
        searchType = 'tv'
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            SEARCH(searchType)
        else:
            main.addDir('Search','tv',1025,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    url = 'http://www.tubeplus.me/search/tv-shows/'+url+'/0/'
                    
                    main.addDir(seahis,url,1025,thumb)
    if ret == 1:
        searchType = 'movie'
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        if not os.path.exists(SeaFile):
            SEARCH(searchType)
        else:
            main.addDir('Search','movie',1025,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    url = 'http://www.tubeplus.me/search/movies/'+url+'/0/'
                    main.addDir(seahis,url,1025,thumb)



def SEARCH(murl):
    if murl == 'tv':
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        try:
            os.makedirs(seapath)
        except:
            pass
            keyb = xbmc.Keyboard('', '[COLOR=FF67cc33]MashUP: Search For Shows or Episodes[/COLOR]')
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
                    surl = 'http://www.tubeplus.me/search/tv-shows/'+encode+'/0/'
                    #SEARCH(url)
            else:
                return TVMENU()
    elif murl=='movie':
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        try:
            os.makedirs(seapath)
        except:
            pass
            keyb = xbmc.Keyboard('', '[COLOR=FF67cc33]MashUP: Search For Movies[/COLOR]')
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
                    surl = 'http://www.tubeplus.me/search/movies/'+encode+'/0/'
                    #SEARCH(url)
            else:
                return MOVIE_MENU()       

    else:
        surl=murl
    html = main.OPENURL2(surl)
    r = re.compile(r'<div id="list_body">(.+?)<div id="list_footer"></div>', re.DOTALL|re.I|re.M).findall(html)
    match = re.compile(r'title="Watch online: ([^"]*)" href="/([^"]*)"><img border="0" alt=".+?" src="([^"]*)"></a>', re.I).findall(str(r))# href',str(r),flags=re.I)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for name, url, image in match:
        name = name.replace('_',' ').replace('/','').replace('\\x92',"'").replace('&rsquo;',"'").replace('&quot;','"').replace('&#044;',',')
        if 'tv-shows' in surl:
            main.addDirT(name.replace('.',''),url,1026,'http://www.tubeplus.me'+image,'','','','','')
        else:
            main.addDirM(name.replace('.',''),url,1026,'http://www.tubeplus.me'+image,'','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()
    del dialogWait          

       

    
def POPGENRES(url):
    print 'popgenre'
    print url
    html = main.OPENURL2(url)
    if html == None:
        return
    r = re.findall('<div id="popular">(.+?)<div id="popular_footer"></div>', html, re.M|re.DOTALL)
    pattern = '<li><a href="/(.+?)">(.+?)</a>'
    r = re.findall(r''+pattern+'', str(r))
    for url, name in r:
        url = BASE_URL+url
        main.addDir(name, url, '1046', '')

def INDEXONE(url):
    print 'INDEXONE'
    print url
    html = main.OPENURL2(url)
    if html == None:
        return
    r = re.findall(r'var chart_movies(.+?)for\s\(movie in chart_movies\)', html, re.M|re.DOTALL)
    pattern = 'tt: \"(.+?)\".+?url: \"/(.+?)\"'
    r = re.findall(r''+pattern+'', str(r))
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(r)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for name, url in r:
        main.addDirM(name,url,'mode','','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()



def MOVIEAZ(url):
    print 'movie a-z'
    print url
    html = main.OPENURL2(url)
    if html == None:
        return
    r = re.findall('<div id="alphabetic">(.+?)<!-- ###', html, re.M|re.DOTALL)
    print r
    pattern = '<a href=\"\/(.+?)\"\>(.+?)\</a>'
    r = re.findall(r''+pattern+'', str(r))
    print r
    for url, name in r:
        url = BASE_URL+url
        main.addDir(name, url, 'mode', '')
        
        


def MOVIES_SPECIAL(url):
    html = main.OPENURL2(url)
    if html == None:
        return
    r = re.findall(r'<h1 id="list_head" class="short">.+?Movies Special</h1>(.+?)&laquo;More Movies&raquo;</a>',html, re.M|re.DOTALL)
    pattern = '<a target="_blank" title="Watch online: (.+?)" href="/(.+?)"><img'
    r = re.findall(r''+pattern+'',str(r))
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(r)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for name, url in r:
        url = BASE_URL+url
        main.addDirM(name,url,1026,'','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()
    
    
def LINK(mname,murl):      
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Hosts,1500)")
        murl=BASE_URL+murl
        html = main.OPENURL(murl)
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        r = re.compile(r'class="(o.+?)">.+?javascript:show\(\'(.+?)\'\,\'.+?\'\,\s\'(.+?)\'\)\;.+?<b>(.+?)said work',re.M|re.DOTALL).findall(html)
        for status, url, hoster, said in r:
            percentage = said.replace('%','')
            host=hoster
            hoster = hoster.replace('www.','').replace('.in','').replace('.net','').replace('.com','').replace('.to','').replace('.org','').replace('.ch','').replace('.eu','')
            if int(percentage) in range(0,25):
                title = '[COLOR blue]'+hoster.upper()+'[/COLOR][COLOR red]           '+status+' '+said+'[/COLOR]'
            if int(percentage) in range(25,50):
                title = '[COLOR blue]'+hoster.upper()+'           '+status+' '+said+'[/COLOR]'
            if int(percentage) in range(50,75):
                title = '[COLOR blue]'+hoster.upper()+'[/COLOR][COLOR orange]           '+status+' '+said+'[/COLOR]'
            if int(percentage) in range(75,101):
                title = '[COLOR blue]'+hoster.upper()+'[/COLOR][COLOR=FF67cc33]          '+status+' '+said+'[/COLOR]'
            main.addDown2(mname+' '+title,'xoxv'+host+'xoxe'+url+'xoxc',1027,art+'/hosts/'+hoster.lower()+'.png',art+'/hosts/'+hoster.lower()+'.png')    
    
def VIDEOLINKS(mname,url):
        ok=True
        hname=mname
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,3000)")
        r=re.findall('Season(.+?)Episode([^<]+)',mname)
        if r:
            mname=mname.split(' [COLOR blue]')[0]
            infoLabels =main.GETMETAEpiT(mname,'','')
            video_type='episode'
            season=infoLabels['season']
            episode=infoLabels['episode']
        else:
            mname=mname.split(' [COLOR blue]')[0]
            infoLabels =main.GETMETAT(mname,'','','')
            video_type='movie'
            season=''
            episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        r=re.findall('xoxv(.+?)xoxe(.+?)xoxc',url)
        for hoster, url in r:
            hosted_media = urlresolver.HostedMediaFile(host=hoster, media_id=url)
        source=hosted_media
        try :
            if source:
                    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                    stream_url = source.resolve()
            else:
                    stream_url = False
                    return
                
            infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
            # play with bookmark
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                wh.add_item(hname+' '+'[COLOR=FF67cc33]TubePlus[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=str(img), fanart=str(fanart), is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
            if stream_url != False:
                    main.ErrorReport(e)
            return ok     
    
