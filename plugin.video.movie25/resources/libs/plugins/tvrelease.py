import urllib, urllib2, re, string, urlparse, sys,   os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, HTMLParser

from t0mm0.common.addon import Addon
from resources.libs import main
from t0mm0.common.net import Net
from universal import playbackengine, watchhistory

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
net = Net()

BASEURL = 'http://www.tv-release.net/category/'

art = main.art
error_logo = art+'/bigx.png'
wh = watchhistory.WatchHistory(addon_id)


try:
    import urlresolver
except:
    addon.show_small_popup('MashUP: Tv-Release','Failed To import URLRESOLVER', 5000, error_logo)
    addon.show_ok_dialog(['Failed To Import URLRESOLVER','Please Post Logfile In MashUP Forum @','http://www.xbmchub.com'],
                             'MashUP: TV-Release')

def MAINMENU():
    main.addDir('TV 480',BASEURL+'tvshows/tv480p/',       1001,art+'/TV480.png')
    main.addDir('TV 720',BASEURL+'tvshows/tv720p/',       1001,art+'/TV720.png')
    main.addDir('TV MP4',BASEURL+'tvshows/tvmp4/',        1001,art+'/TVmp4.png')
    main.addDir('TV Xvid',BASEURL+'tvshows/tvxvid/',       1001,art+'/TVxvid.png')
    main.addDir('TV Packs',BASEURL+'tvshows/tvpack/',       1001,art+'/TVpacks.png')
    main.addDir('TV Foreign',BASEURL+'tvshows/tv-foreign/',   1001,art+'/TVforeign.png')
    main.addDir('Movies 480',BASEURL+'movies/movies480p/',    1001,art+'/Movies480.png')
    main.addDir('Movies 720',BASEURL+'movies/movies720p/',    1001,art+'/Movies720.png')
    main.addDir('Movies Xvid',BASEURL+'movies/moviesxvid/',    1001,art+'/Moviesxvid.png')
    main.addDir('Movies Foreign',BASEURL+'movies/moviesforeign/', 1001,art+'/Moviesforeign.png')
    main.VIEWSB()

def INDEX(url):
    types = []
    if '/tvshows/' in url:
        types = 'tv'
    elif '/movies/' in url:
        types = 'movie'
    html = GETHTML(url)
    if html == None:
        return
    pattern = 'text-align:left;">\n<a href="(.+?)"><b><font size="\dpx">(.+?)</font>'
    r = re.findall(pattern, html, re.I|re.M|re.DOTALL)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(r)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for url, name in r:
        if re.findall('\ss\d+e\d+\s', name, re.I|re.DOTALL):
            r = re.findall('(.+?)\ss(\d+)e(\d+)\s', name, re.I)
            for name, season, episode in r:
                name = name+' Season '+season+' Episode '+episode+' ('+season+'x'+episode+')'
        elif re.findall('\s\d{4}\s\d{2}\s\d{2}\s', name):
            r = re.findall('(.+?)\s(\d{4})\s(\d{2})\s(\d{2})\s',name)
            for name, year, month, day in r:
                name = name+' '+year+' '+month+' '+day
        elif re.findall('\d+p\s', name):
            r = re.findall('(.+?)\s\d+p\s', name)
            for name in r:
                pass
        elif re.findall('\shdtv\sx', name, re.I):
            r = re.findall('(.+?)\shdtv\sx',name, re.I)
            for name in r:
                pass
        if types == 'tv':
            main.addDirTE(name,url,1003,'','','','','','')
        elif types == 'movie':
            if re.findall('\s\d+\s',name):
                r = name.rpartition('\s\d{4}\s')
            main.addDirM(name,url,1003,'','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()
    del dialogWait
    if '<!-- Zamango Pagebar 1.3 -->' in html:
        r = re.findall('<span class=\'zmg_pn_current\'>(\d+)</span>\n<span class=\'zmg_pn_standar\'><a href=\'(http://tv-release.net/category/.+?/\d+)\' title=\'Page \d+ of (\d+)\'>\d+</a>',html, re.I|re.DOTALL|re.M)
        for current, url, total in r:
            name = '[COLOR green]Page '+current+' of '+total+', Next Page >>>[/COLOR]'
            main.addDir(name, url, 1001, art+'/nextpage.png')
            url = url+':'+total
            name = '[COLOR green]Goto Page[/COLOR]'
            main.addDir(name, url, 1002, art+'/gotopagetr.png')
    main.VIEWS()

def LISTHOSTERS(name,url):
    print 'LISTHOSTERS(url): '+url
    print 'LISTHOSTERS NAME: '+name
    html = GETHTML(url)
    if html == None: return
    main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    r = re.findall(r'class="td_cols"><a target=\'_blank\'.+?href=\'(.+?)\'>',html, re.M|re.DOTALL)
    sources = []
    for url in r:
        media = urlresolver.HostedMediaFile(url=url)
        sources.append(media)
    print sources
    sources = urlresolver.filter_source_list(sources)
    r = re.findall(r'\'url\': \'(.+?)\', \'host\': \'(.+?)\'', str(sources), re.M)
    for url, host in r:
        r = re.findall(r'(.+?)\.',host)
        if 'www.real-debrid.com' in host:
            host = re.findall(r'//(.+?)/', url)
            host = host[0].replace('www.','')
            print 'rd1'
            print host
            host = host.rpartition('.')
            print host
            host = host[0]
            print 'rd'
            print host
            
            
            
        else:
            host = r[0]

        main.addDown2(name+"[COLOR blue] :"+host.upper()+"[/COLOR]",url+'xocx'+url+'xocx',574,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')

                
def GOTOP(url):
    default = url
    r = url.rpartition(':')
    url = re.findall('(.+page\/)\d+',r[0])
    url = url[0]
    total = r[2]
    keyboard = xbmcgui.Dialog().numeric(0, '[B][I]Goto Page Number[/B][/I]')
    if keyboard > total or keyboard == '0':
        addon.show_ok_dialog(['Please Do Not Enter a Page Number bigger than',''+total+', Enter A Number Between 1 and '+total+'',
                              ''], 'MashUP: TV-Release')
        GOTOP(default)
    url = url+keyboard
    INDEX(url)
        
        
    


def GETHTML(url):
    try:
        h = net.http_GET(url).content
        #print h
        if '<h2>Under Maintenance</h2>' in h:
            addon.show_ok_dialog(['[COLOR green][B]TV-Release is Down For Maintenance,[/COLOR][/B]',
                                  '[COLOR green][B]Please Try Again Later[/COLOR][/B]',''],'MashUP: TV-Release')
            return MAINMENU()
        return h.encode("utf-8")
    except urllib2.URLError, e:
        addon.show_small_popup('MashUP: Tv-Release','TV-Release Web Site Failed To Respond, Check Log For Details', 9000, error_logo)
        addon.log_notice(str(e))
        return MAINMENU()
    
    


