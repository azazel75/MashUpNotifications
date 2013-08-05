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
    main.addDir('',    BASE_URL+'?s=',1021,art+'/tpsearch.png')
    main.addDir('',BASE_URL,1021,art+'/tptvshows.png')
    main.addDir('',BASE_URL,1022,art+'/tpmovies.png')
    #main.addDir('TubePLUS Movie Charts','http://www.tubeplus.me/tool/',1023,'')
    main.addSpecial('',BASE_URL,1004,art+'/tpsettings.png')
    main.VIEWSB()

def TVMENU():
    main.addDir('[COLOR green][B]L[/B]ast Aired TV Shows/Episodes[/COLOR]',BASE_URL,1042,'')
    main.addDir('[COLOR green][B]A[/B]ll latest Aired TV Shows/Episodes[/COLOR]',BASE_URL+'browse/tv-shows/Last/ALL/',1041,'')
    main.addDir('[COLOR green][B]T[/B]op 10 Tv Episodes[/COLOR]',BASE_URL,1043,'')
    main.addDir('[COLOR green][B]T[/B]V Shows by Genres[/COLOR]',BASE_URL+'browse/tv-shows/',1044,'')
    main.addDir('[COLOR green][B]T[/B]V Shows A to Z[/COLOR]',BASE_URL,'mode','')
    #main.addDir('[COLOR green][B]S[/B]earch TV Shows[/COLOR]',BASE_URL+'search/','mode','')

def MOVIE_MENU():
    html = main.OPENURL2(BASE_URL)
    r = re.findall(r'<h1 id="list_head" class="short">&nbsp;&nbsp;&nbsp;(.+?)</h1>',html)
    for movies_special in r:
        main.addDir('[COLOR green]'+movies_special+'[/COLOR]',BASE_URL,1040,'')
    main.addDir('[COLOR green][B]M[/B]ost Popular Movies[/COLOR]',BASE_URL+'browse/movies/Last/ALL/','mode','')
    main.addDir('[COLOR green][B]M[/B]ovies By Genres[/COLOR]',BASE_URL+'browse/movies/',1044,'')
    main.addDir('[COLOR green][B]M[/B]ost Popular Genres[/COLOR]',BASE_URL,'mode',art+'/tpmostpopgenre.png')
    main.addDir('[COLOR green][B]M[/B]ovies by A to Z[/COLOR]',BASE_URL+'browse/movies/All_Genres/-/','mode','')

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
        main.addDirTE(name.replace('.',''),url,'1003','','','','','','')
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
        main.addDirTE(name.replace('.',''),url,'1003','','','','','','')
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
        main.addDirTE(name.replace('.',''),url,'1003','','','','','','')
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
    print url
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
            print url#add in the tv show adddir

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
            name = '[COLOR green]Page '+current+' of '+total+', Next Page >>>[/COLOR]'
            main.addDir(name, BASE_URL+url, '', art+'/nextpage.png')
            url = url+':'+total
            name = '[COLOR green]Goto Page[/COLOR]'
            main.addDir(name, url, 1002, art+'/gotopagetr.png')
    main.VIEWS()
            
        
        

    
def TEST(url):
    print 'test'
    print url
        


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
        main.addDirM(name,url,'mode','','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()
    
    
    
    
