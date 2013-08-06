
import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urlresolver
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net
from metahandler import metahandlers
import datetime,time
from xgoogle.search import GoogleSearch, SearchError

#Mash Up - by Mash2k3 2012.

Mainurl ='http://www.movie25.com/movies/'
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
mashpath = selfAddon.getAddonInfo('path')
addon = Addon(addon_id)
grab = metahandlers.MetaData(preparezip = False)
Dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25', ''))
repopath = xbmc.translatePath(os.path.join('special://home/addons/repository.mash2k3', ''))


datapath = addon.get_profile()
if selfAddon.getSetting('visitor_ga')=='':
    from random import randint
    selfAddon.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))

VERSION = "1.3.6"
PATH = "MashUp-"            
UATRACK="UA-38312513-1" 

try:
    log_path = xbmc.translatePath('special://logpath')
    log = os.path.join(log_path, 'xbmc.log')
    logfile = open(log, 'r').read()
    match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
    if match:
        for build, PLATFORM in match:
            print 'XBMC '+build+' Platform '+PLATFORM
    else:
        PLATFORM=''
except:
    PLATFORM=''

sys.path.append( os.path.join( selfAddon.getAddonInfo('path'), 'resources', 'libs' ))
################################################################################ Common Calls ##########################################################################################################

art = 'https://github.com/mash2k3/MashupArtwork/raw/master/art'
error_logo = art+'/bigx.png'
elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/art/bigx.png')

def OPENURL(url):
    UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    try:
        print "MU-Openurl = " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #link = net(UserAgent).http_GET(url).content
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','').replace('&#038;','&').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        link=link.replace('%3A',':').replace('%2F','/')
        return link
    except:
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000,"+elogo+")")
        link ='website down'
        return link

def OPENURL2(url):
    UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    try:
        print "MU-Openurl = " + url
        link = net(UserAgent).http_GET(url).content
        return link.encode('utf-8', 'ignore')
    except:
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000,"+elogo+")")
        link ='website down'
        return link
        
def REDIRECT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.geturl()
        return link

def Clearhistory(url):
        os.remove(url)

def unescapes(text):
        try:            
            rep = {"&nbsp;": " ","\n": "","\t": "","\r": "","%5B": "[","%5D": "]","%3a": ":","%3A":":","%2f":"/","%2F":"/","%3f":"?","%3F":"?","%26":"&","%3d":"=","%3D":"=","%2C":",","%2c":",","%3C":"<","%20":" ","%22":'"',"%3D":"=","%3A":":","%2F":"/","%3E":">","%3B":",","%27":"'","%0D":"","%0A":""}
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text

def SwitchUp():
        if selfAddon.getSetting("switchup") == "false":
            selfAddon.setSetting(id="switchup", value="true")
        else:
            selfAddon.setSetting(id="switchup", value="false")
        xbmc.executebuiltin("XBMC.Container.Refresh")

def ErrorReport(e):
        elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/art/bigx.png')
        xbmc.executebuiltin("XBMC.Notification([COLOR green]MashUp Error[/COLOR],"+str(e)+",10000,"+elogo+")")
        xbmc.log('***********MashUp Error: '+str(e)+'**************')
################################################################################ Notifications #########################################################################################################

def CheckVersion():
    try:
        link=OPENURL('https://bitbucket.org/mash2k3/mash2k3-repository/raw/master/plugin.video.movie25/resources/libs/main.py')
    except:
        link='nill'

    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('VERSION = "(.+?)"').findall(link)
    if len(match)>0:
        if VERSION != str(match[0]):
                dialog = xbmcgui.Dialog()
                ok=dialog.ok('[B]New Update Available![/B]', "Your version of Mash Up is outdated." ,'The current available version is '+str(match[0]),'To update goto addons under system settings')
        else:
            print 'Mash Up is Up to Date'
    
    else:
        print 'BitBucket Link Down'

################################################################################ AutoView ##########################################################################################################


def VIEWS():
        if selfAddon.getSetting("auto-view") == "true":
                if selfAddon.getSetting("choose-skin") == "true":
                        if selfAddon.getSetting("con-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("con-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(51)")
                        elif selfAddon.getSetting("con-view") == "2":
                                xbmc.executebuiltin("Container.SetViewMode(500)")
                        elif selfAddon.getSetting("con-view") == "3":
                                xbmc.executebuiltin("Container.SetViewMode(501)")
                        elif selfAddon.getSetting("con-view") == "4":
                                xbmc.executebuiltin("Container.SetViewMode(508)")
                        elif selfAddon.getSetting("con-view") == "5":
                                xbmc.executebuiltin("Container.SetViewMode(504)")
                        elif selfAddon.getSetting("con-view") == "6":
                                xbmc.executebuiltin("Container.SetViewMode(503)")
                        elif selfAddon.getSetting("con-view") == "7":
                                xbmc.executebuiltin("Container.SetViewMode(515)")
                        return
                elif selfAddon.getSetting("choose-skin") == "false":
                        if selfAddon.getSetting("xpr-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("xpr-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(52)")
                        elif selfAddon.getSetting("xpr-view") == "2":
                                xbmc.executebuiltin("Container.SetViewMode(501)")
                        elif selfAddon.getSetting("xpr-view") == "3":
                                xbmc.executebuiltin("Container.SetViewMode(55)")
                        elif selfAddon.getSetting("xpr-view") == "4":
                                xbmc.executebuiltin("Container.SetViewMode(54)")
                        elif selfAddon.getSetting("xpr-view") == "5":
                                xbmc.executebuiltin("Container.SetViewMode(60)")
                        elif selfAddon.getSetting("xpr-view") == "6":
                                xbmc.executebuiltin("Container.SetViewMode(53)")
                        return
        else:
                return
        

def VIEWSB():
        if selfAddon.getSetting("auto-view") == "true":
                        if selfAddon.getSetting("home-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("home-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(500)")

                        return

def VIEWSB2():
        if selfAddon.getSetting("auto-view") == "true":
                        if selfAddon.getSetting("sub-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("sub-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(500)")

                        return
################################################################################ Movies Metahandler ##########################################################################################################


def GETMETA(mname,genre,year,thumb): 
        if selfAddon.getSetting("meta-view") == "true":
                mname  = mname.split('[COLOR blue]')[0]
                mname  = mname.split('[COLOR red]')[0]
                if re.findall('\s\d{4}',mname):
                    r = re.split('\s\d{4}',mname,re.DOTALL)
                    name = r[0]
                    mname=mname+' MU'
                    year = re.findall('\s(\d{4})\s',mname)
                    if year:
                        year = year[0]
                    else:
                        year=''
                else:
                    name=mname
                    year=''
                name=name.replace('-','').replace('&','').replace('acute;','').replace('C ','')
                name = name.decode("ascii", "ignore")
                if year =='':
                        year=''
                meta = grab.get_meta('movie',name,None,None,year)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
                print "Movie mode: %s"%name
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                  'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],
                  'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'], 'imdb_id' : meta['imdb_id']}
                if infoLabels['genre']=='':
                        infoLabels['genre']=genre
                if infoLabels['cover_url']=='':
                        infoLabels['cover_url']=thumb
                if infoLabels['backdrop_url']=='':
                        fan=Dir+'fanart.jpg'
                        infoLabels['backdrop_url']=fan
                if meta['overlay'] == 7:
                   infoLabels['playcount'] = 1
                else:
                   infoLabels['playcount'] = 0
        else:
                if thumb=='':
                    thumb=art+'vidicon.png'
                fan=Dir+'fanart.jpg'
                infoLabels = {'title': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': year,'plot': '','genre': genre,'imdb_id': ''}
        return infoLabels

def GETMETAB(mname,genre,year,thumb): 
        if selfAddon.getSetting("meta-view") == "true":
                mname  = mname.split('[COLOR blue]')[0]
                mname  = mname.split('[COLOR red]')[0]
                print "master "+mname
                try:
                    name=mname.split('(')[0]
                    mname=mname.split(')')[0]
                    year=mname.split('(')[1]
                    
                except:
                    name=mname
                    year=''
                
                meta = grab.get_meta('movie',name,None,None,year,overlay=6)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
                print "Movie mode: %s"%name
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                  'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],
                  'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'], 'imdb_id' : meta['imdb_id']}
                if infoLabels['genre']=='':
                        infoLabels['genre']=genre
                if infoLabels['cover_url']=='':
                        infoLabels['cover_url']=thumb
        else:
                if thumb=='':
                    thumb=art+'vidicon.png'
                fan=Dir+'fanart.jpg'
                infoLabels = {'title': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': year,'plot': '','genre': genre,'imdb_id': ''}
        return infoLabels

def GETMETAT(mname,genre,fan,thumb): 
        if selfAddon.getSetting("meta-view") == "true":
                mname  = mname.replace(' EXTENDED and UNRATED','').replace('[COLOR purple]','').replace('MaxPowers','').replace('720p','').replace('1080p','').replace('TS','').replace('HD','').replace('Cam','').replace('R6','').replace('CAM','').replace('H.M.','').replace('HackerMil','').replace('[COLOR green]','').replace('[COLOR yellow]','').replace('[COLOR aqua]','').replace('[COLOR blue]','').replace('[COLOR red]','').replace('[/COLOR]','').replace('(','').replace(')','').replace('[','').replace(']','')
                if re.findall('\s\d{4}',mname):
                    r = re.split('\s\d{4}',mname,re.DOTALL)
                    name = r[0]
                    mname=mname+' MU'
                    year = re.findall('\s(\d{4})\s',mname)
                    if year:
                        year = year[0]
                    else:
                        year=''
                else:
                    name=mname
                    year=''
                name = name.decode("ascii", "ignore")
                meta = grab.get_meta('movie',name,None,None,year='')# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
                print "Movie mode: %s"%name
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                  'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],
                  'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'], 'imdb_id' : meta['imdb_id']}
                if infoLabels['genre']=='':
                        infoLabels['genre']=genre
                if infoLabels['cover_url']=='':
                        infoLabels['cover_url']=thumb
                if infoLabels['backdrop_url']=='':
                        if fan=='':
                            fan=Dir+'fanart.jpg'
                        else:
                            fan=fan
                        infoLabels['backdrop_url']=fan
                if meta['overlay'] == 7:
                   infoLabels['playcount'] = 1
                else:
                   infoLabels['playcount'] = 0
                   
                if infoLabels['cover_url']=='':
                    thumb=art+'vidicon.png'
                    infoLabels['cover_url']=thumb
        else:
                if thumb=='':
                    thumb=art+'vidicon.png'
                if fan=='':
                    fan=Dir+'fanart.jpg'
                else:
                    fan=fan
                infoLabels = {'title': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': '','plot': '','genre': genre,'imdb_id': '','tmdb_id':''}
        return infoLabels

################################################################################ TV Shows Metahandler ##########################################################################################################


def GETMETAShow(mname): 
        if selfAddon.getSetting("meta-view") == "true":
                mname=mname.replace(' [COLOR red]Recently Updated[/COLOR]','').replace('.','').replace('M.D.','').replace('<span class="updated">Updated!</span>','')    
                mname  = mname.replace('[COLOR blue]','').replace('[COLOR red]','').replace('[/COLOR]','').replace('(','').replace(')','').replace('[','').replace(']','')
                mname= mname.replace('-','').replace('-2012','').replace('acute;','').replace('Vampire Diaries','The Vampire Diaries').replace('Comedy Central Roast','Comedy Central Roasts')
                mname= mname.replace('Doctor Who  2005','Doctor Who').replace(' (US)','(US)').replace(' (UK)','(UK)').replace(' (AU)','(AU)').replace('%','')
                if re.findall('\s\d{4}',mname):
                    r = re.split('\s\d{4}',mname,re.DOTALL)
                    name = r[0]
                    mname=mname+' MU'
                    year = re.findall('\s(\d{4})\s',mname)
                    if year:
                        year = year[0]
                    else:
                        year=''
                else:
                    name=mname
                    year=''
                
                meta = grab.get_meta('tvshow',name,None,None,year,overlay=6)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
                print "Tv Mode: %s"%name
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                  'plot': meta['plot'],'title': mname,'cover_url': meta['cover_url'],
                  'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                      'backdrop_url': meta['backdrop_url'],'status': meta['status']}
                if infoLabels['cover_url']=='':
                        infoLabels['cover_url']=art+'/vidicon.png'
        else:
                infoLabels = {'title': mname,'cover_url': art+'/vidicon.png','backdrop_url': ''}
        return infoLabels

def GETMETAEpi(mname,data):
        if selfAddon.getSetting("meta-view") == "true":
                match=re.compile('(.+?)xoxc(.+?)xoxc(.+?)xoxc(.+?)xoxc').findall(data)
                for showname, sea, epi, epiname in match:
                        showname= showname.replace('-','').replace('-2012','').replace('acute;','').replace('Comedy Central Roast','Comedy Central Roasts')
                        showname= showname.replace('Doctor Who  2005','Doctor Who').replace(' (US)','(US)').replace(' (UK)','(UK)').replace(' (AU)','(AU)').replace('%','').replace(' [COLOR red]Recently Updated[/COLOR]','').replace('.','').replace('M.D.','').replace('<span class="updated">Updated!</span>','')
                        print showname+' '+sea+' '+epi+' '+epiname
                meta = grab.get_episode_meta(str(showname),None, int(sea), int(epi),episode_title=str(epiname), overlay='6')
                print "Episode Mode: Name %s Season %s - Episode %s"%(str(epiname),str(sea),str(epi))
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                      'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                      'poster': meta['poster'],'episode': meta['episode'],'backdrop_url': meta['backdrop_url']}
                
        else:
                infoLabels = {'title': mname,'cover_url': '','backdrop_url': ''}       
        
        return infoLabels

def GETMETAEpiT(mname,thumb,desc):
        if selfAddon.getSetting("meta-view") == "true":
                mname  = mname.replace('[COLOR purple]','').replace('[COLOR green]','').replace('[COLOR yellow]','').replace('[COLOR aqua]','').replace('[COLOR blue]','').replace('[COLOR red]','').replace('[/COLOR]','')
                mname  = mname.replace('New Episode','').replace('Main Event','').replace('New Episodes','')
                mname=mname+' MU'
                r = re.findall('(.+?)\ss(\d+)e(\d+)\s',mname,re.I)
                if r:
                    for name,sea,epi in r:
                        year=''
                        name=name.replace(' US','').replace(' (US)','').replace(' UK',' (UK)').replace(' AU','').replace(' and',' &').replace(' 2013','').replace(' 2011','').replace(' 2012','').replace(' 2010','')
                        if re.findall('twisted',name,re.I):
                            year='2013'
                        if re.findall('the newsroom',name,re.I):
                            year='2012'
                        metaq = grab.get_meta('tvshow',name,None,None,year)
                        imdb=metaq['imdb_id']
                        tit=metaq['title']
                        year=metaq['year']
                        epiname=''

                f = re.findall('(.+?)\sseason\s(\d+)\sepisode\s(\d+)\s',mname,re.I)
                if f:
                    for name,sea,epi in f:
                        year=''
                        name=name.replace(' US','').replace(' (US)','').replace(' (us)','').replace(' (uk Series)','').replace(' (UK)','').replace(' UK',' (UK)').replace(' AU','').replace(' AND',' &').replace(' And',' &').replace(' and',' &').replace(' 2013','').replace(' 2011','').replace(' 2012','').replace(' 2010','')
                        if re.findall('twisted',name,re.I):
                            year='2013'
                        if re.findall('the newsroom',name,re.I):
                            year='2012'
                        metaq = grab.get_meta('tvshow',name,None,None,year)
                        imdb=metaq['imdb_id']
                        tit=metaq['title']
                        year=metaq['year']
                        epiname=''
                        
                if len(r)==0 and len(f)==0:
                    metaq=''
                    name=mname
                    epiname=''
                    sea=0
                    epi=0
                    imdb=''
                    tit=''
                    year=''
                meta = grab.get_episode_meta(str(name),imdb, int(sea), int(epi))
                print "Episode Mode: Name %s Season %s - Episode %s"%(str(name),str(sea),str(epi))
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'premiered':meta['premiered'],
                      'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],'episode': meta['episode'],
                              'season': meta['season'],'backdrop_url': meta['backdrop_url']}

                if infoLabels['cover_url']=='':
                        if metaq!='':
                            thumb=metaq['cover_url']
                            infoLabels['cover_url']=thumb
                           
                if infoLabels['backdrop_url']=='':
                        fan=Dir+'fanart.jpg'
                        infoLabels['backdrop_url']=fan
                if infoLabels['cover_url']=='':
                    if thumb=='':
                        thumb=art+'/vidicon.png'
                        infoLabels['cover_url']=thumb
                    else:
                        infoLabels['cover_url']=thumb
                infoLabels['imdb_id']=imdb
                if meta['overlay'] == 7:
                   infoLabels['playcount'] = 1
                else:
                   infoLabels['playcount'] = 0
                
                infoLabels['showtitle']=tit
                infoLabels['year']=year
                   
        else:
                fan=Dir+'fanart.jpg'
                infoLabels = {'title': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': '','plot': desc,'genre': '','imdb_id': ''}       
        
        return infoLabels
############################################################################### Playback resume/ mark as watched #################################################################################

def WatchedCallback():
        addon.log('Video completely watched.')
        videotype='movies'
        grab.change_watched(videotype, name, iconimage, season='', episode='', year='', watched=7)
        xbmc.executebuiltin("XBMC.Container.Refresh")

def WatchedCallbackwithParams(video_type, title, imdb_id, season, episode, year):
    print "worked"
    grab.change_watched(video_type, title, imdb_id, season=season, episode=episode, year=year, watched=7)
    xbmc.executebuiltin("XBMC.Container.Refresh")

def ChangeWatched(imdb_id, videoType, name, season, episode, year='', watched='', refresh=False):
        grab.change_watched(videoType, name, imdb_id, season=season, episode=episode, year=year, watched=watched)
        xbmc.executebuiltin("XBMC.Container.Refresh")

def refresh_movie(vidtitle,imdb, year=''):

    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()
    vidtitle = vidtitle.decode("ascii", "ignore")
    vidtitle = re.sub("\d+", "", vidtitle)
    vidtitle=vidtitle.replace('  ','')
    search_meta = grab.search_movies(vidtitle)
    
    if search_meta:
        movie_list = []
        for movie in search_meta:
            movie_list.append(movie['title'] + ' (' + str(movie['year']) + ')')
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose', movie_list)
        
        if index > -1:
            new_imdb_id = search_meta[index]['imdb_id']
            new_tmdb_id = search_meta[index]['tmdb_id']
            year=search_meta[index]['year']

            meta=grab.update_meta('movie', vidtitle, imdb, '',new_imdb_id,'',year)
            


            xbmc.executebuiltin("Container.Refresh")
    else:
        msg = ['No matches found']
        addon.show_ok_dialog(msg, 'Refresh Results')

def episode_refresh(vidname, imdb, season_num, episode_num):
    grab.update_episode_meta(vidname, imdb, season_num, episode_num)
    xbmc.executebuiltin("XBMC.Container.Refresh")
################################################################################Trailers#######################################################################
def trailer(tmdbid):
    if tmdbid == '':
        xbmc.executebuiltin("XBMC.Notification(Sorry!,No Trailer Available For This Movie,3000)")
    else:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading Trailer,1500)")
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
        request= 'http://api.themoviedb.org/3/movie/' + tmdbid + '/trailers?api_key=d5da2b7895972fffa2774ff23f40a92f'
        txheaders= {'Accept': 'application/json','User-Agent':user_agent}
        req = urllib2.Request(request,None,txheaders)
        response=urllib2.urlopen(req).read()
        if re.search('"size":"HD"',response):
            quality=re.compile('"size":"HD","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        elif re.search('"size":"HQ"',response):
            quality=re.compile('"size":"HQ","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        elif re.search('"size":"Standard"',response):
            quality=re.compile('"size":"Standard","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,No Trailer Available For This Movie,3000)")

def TRAILERSEARCH(url, name, imdb):
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Getting Trailers Result,2000)")
    name = re.split(':\s\[',name)
    search      = name[0]
    infoLabels = grab._cache_lookup_by_name('movie', search.strip(), year='')
    print infoLabels
    res_name    = []
    res_url     = []
    res_name.append('[COLOR red][B]Cancel[/B][/COLOR]')
    
    site = ' site:http://www.youtube.com '
    results = SearchGoogle(search+' official trailer', site)
    for res in results:
        if res.url.encode('utf8').startswith('http://www.youtube.com/watch'):
            res_name.append(res.title.encode('utf8'))
            res_url.append(res.url.encode('utf8'))
    results = SearchGoogle(search[:(len(search)-7)]+' official trailer', site)
    
    for res in results:
        if res.url.encode('utf8').startswith('http://www.youtube.com/watch') and res.url.encode('utf8') not in res_url:
            res_name.append(res.title.encode('utf8'))
            res_url.append(res.url.encode('utf8'))
            
    dialog = xbmcgui.Dialog()
    ret = dialog.select(search + ' trailer search',res_name)

    if ret == 0:
        return
    elif ret >= 1:
        trailer_url = res_url[ret - 0]
        try:
            xbmc.executebuiltin(
                "PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=%s)" 
                % str(trailer_url)[str(trailer_url).rfind("v=")+2:] )
            if re.findall('Darwin iOS',PLATFORM):
                grab.update_trailer('movie', imdb, trailer_url)
                xbmc.executebuiltin("XBMC.Container.Refresh")

        except:
            return    

def SearchGoogle(search, site):
    gs = GoogleSearch(''+search+' '+site)
    gs.results_per_page = 25
    gs.page = 0
    try:
        results = gs.get_results()
    except Exception, e:
        print '***** Error: %s' % e
        return None
    return results
############################################################################### Resolvers ############################################################################################
def resolve_veehd(url):
        name = "veeHD"
        cookie_file = os.path.join(datapath, '%s.cookies' % name)
        user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        try:
            loginurl = 'http://veehd.com/login'
            ref = 'http://veehd.com/'
            submit = 'Login'        
            terms = 'on'
            remember_me = 'on'
            data = {'ref': ref, 'uname': '', 'pword': '', 'submit': submit, 'terms': terms, 'remember_me': remember_me}
            html = net(user_agent).http_POST(loginurl, data).content
            net().save_cookies(cookie_file)
            headers = {}
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'}
            net().set_cookies(cookie_file)
            print 'MashUp VeeHD - Requesting GET URL: %s' % url
            html = net().http_GET(url, headers).content
            fragment = re.findall('playeriframe".+?attr.+?src : "(.+?)"', html)
            frag = 'http://%s%s'%('veehd.com',fragment[1])
            net().set_cookies(cookie_file)
            html = net().http_GET(frag, headers).content
            r = re.search('"video/divx" src="(.+?)"', html)
            if r:
                stream_url = r.group(1)
            if not r:
                message = name + '- 1st attempt at finding the stream_url failed probably an Mp4, finding Mp4'
                addon.log_debug(message)
                a = re.search('"url":"(.+?)"', html)
                if a:
                    r=urllib.unquote(a.group(1))
                    if r:
                        stream_url = r
                    else:
                        raise Exception ('File Not Found or removed')
                if not a:
                    a = re.findall('href="(.+?)">', html)
                    stream_url = a[1]
            return stream_url
        except Exception, e:
            print '**** MashUp VeeHD Error occured: %s' % e
            addon.show_small_popup('[B][COLOR green]MashUP: VeeHD Resolver[/COLOR][/B]','Error, Check XBMC.log for Details',
                                   5000, error_logo)
            return

        
def resolve_billionuploads(url):

    try:
            #########
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving BillionUploads Link...')       
            dialog.update(0)
        
            print 'MashUp BillionUploads - Requesting GET URL: %s' % url
            html = net.http_GET(url).content
               
            #Check page for any error msgs
            if re.search('This server is in maintenance mode', html):
                print '***** BillionUploads - Site reported maintenance mode'
                raise Exception('File is currently unavailable on the host')

            #Set POST data values
            op = 'download2'
            rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
            postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            method_free = re.search('<input type="hidden" name="method_free" value="(.*?)">', html).group(1)
            down_direct = re.search('<input type="hidden" name="down_direct" value="(.+?)">', html).group(1)
        
            #Captcha
            captchaimg = re.search('<img src="(http://BillionUploads.com/captchas/.+?)"', html)
        
            dialog.close()
        
            #If Captcha image exists
            if captchaimg:
                #Grab Image and display it
                img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()
            
                #Small wait to let user see image
                time.sleep(3)
            
                #Prompt keyboard for user input
                kb = xbmc.Keyboard('', 'Type the letters in the image', False)
                kb.doModal()
                capcode = kb.getText()
            
                #Check input
                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '':
                        capcode = kb.getText()
                    elif userInput == '':
                        Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                        return None
                else:
                    return None
                wdlg.close()
            
                data = {'op': op, 'rand': rand, 'id': postid, 'referer': url, 'method_free': method_free, 'down_direct': down_direct, 'code': capcode}

            else:
                data = {'op': op, 'rand': rand, 'id': postid, 'referer': url, 'method_free': method_free, 'down_direct': down_direct}

            #They need to wait for the link to activate in order to get the proper 2nd page
            dialog.close()
            common.addon.show_countdown(3, 'Please Wait', 'Resolving')
               
            dialog.create('Resolving', 'Resolving MashUp BillionUploads Link...') 
            dialog.update(50)
        
            print 'MashUp BillionUploads - Requesting POST URL: %s DATA: %s' % (url, data)
            html = net.http_POST(url, data).content
            dialog.update(100)
            link = re.search('&product_download_url=(.+?)"', html).group(1)
            link = link + "|referer=" + url
            return link

    except Exception, e:
        print '**** MashUp BillionUploads Error occured: %s' % e
        raise
    finally:
        dialog.close()

def resolve_180upload(url):

    try:
        datapath = addon.get_profile()
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving 180Upload Link...')
        dialog.update(0)
        
        puzzle_img = os.path.join(datapath, "180_puzzle.png")
        
        print 'MashUp 180Upload - Requesting GET URL: %s' % url
        html = net.http_GET(url).content

        dialog.update(50)
                
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            raise Exception('Unable to resolve 180Upload Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net.http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           xbmc.sleep(3000)

           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving MashUp 180Upload Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'MashUp 180Upload - Requesting POST URL: %s' % url
        html = net.http_POST(url, data).content
        dialog.update(100)
        
        link = re.search('<a href="(.+?)" onclick="thanks\(\)">Download now!</a>', html)
        if link:
            print 'MashUp 180Upload Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            raise Exception('Unable to resolve 180Upload Link')

    except Exception, e:
        print '**** MashUp 180Upload Error occured: %s' % e
        raise
    finally:
        dialog.close()
        
def resolve_videto(url):
    error_logo = art+'/bigx.png'
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    from resources.libs import jsunpack
    try:
        html = net(user_agent).http_GET(url).content
        addon.log_error('MashUP: Resolve Vidto - Requesting GET URL: '+url)
        r = re.findall(r'<font class="err">File was removed</font>',html,re.I)
        if r:
            addon.log_error('MashUP: Resolve Vidto - File Was Removed')
            addon.show_small_popup('[B][COLOR green]MashUP: Vidto Resolver[/COLOR][/B]','No Such File Or The File Has Been Removed',
                                   5000, error_logo)
            return
        if not r:
            r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                           ,html,re.M|re.DOTALL)
            if r:
                unpacked = jsunpack.unpack(r[0])#this is where it will error, not sure if resources,libs added to os path
                r = re.findall(r'label:"\d+p",file:"(.+?)"}',unpacked)
            if not r:
                r = re.findall('type="hidden" name="(.+?)" value="(.+?)">',html)
                post_data = {}
                for name, value in r:
                    post_data[name] = value
                post_data['usr_login'] = ''
                post_data['referer'] = url
                addon.show_countdown(7, 'Please Wait', 'Resolving')
                html = net(user_agent).http_POST(url,post_data).content
                r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                               ,html,re.M|re.DOTALL)
                if r:
                    unpacked = jsunpack.unpack(r[0])
                    r = re.findall(r'label:"\d+p",file:"(.+?)"}',unpacked)
                if not r:
                    r = re.findall(r"var file_link = '(.+?)';",html)
        return r[0]
    except Exception, e:
        print 'MashUP: Resolve Vidto Error - '+str(e)
        addon.show_small_popup('[B][COLOR green]MashUP: Vidto Resolver[/COLOR][/B]','Error, Check XBMC.log for Details',
                               5000, error_logo)
        return
############################################################################### Download Code ###########################################################################################
downloadPath = selfAddon.getSetting('download-folder')
DownloadLog=os.path.join(datapath,'Downloads')
try:
    os.makedirs(DownloadLog)
except:
    pass
DownloadFile=os.path.join(DownloadLog,'DownloadLog') 

class StopDownloading(Exception): 
        def __init__(self, value): 
            self.value = value 
        def __str__(self): 
            return repr(self.value)
def GetUrliW(url):
        link=OPENURL(url)
        link=unescapes(link)
        match=re.compile('class=frame src="(.+?)"').findall(link)
        link=match[0]
        return link

def geturl(murl):
        link=OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<a class="myButton" href="(.+?)">Click Here to Play</a>').findall(link)
        if len(match)==0:
                match=re.compile('<a class="myButton" href="(.+?)">Click Here to Play Part1</a><a class="myButton" href="(.+?)">Click Here to Play Part2</a>').findall(link)
                return match[0]
        else:
                return match[0]

def Download_Source(name,url):
    originalName=name
    match=re.compile('watchseries.lt').findall(url)
    if match:
        name=name.replace('/','').replace('.','')
        name=name.replace('[DVD]','').replace('[TS]','').replace('[TC]','').replace('[CAM]','').replace('[SCREENER]','').replace('[COLOR blue]','').replace('[COLOR red]','').replace('[/COLOR]','').replace('[COLOR]','')
        name=name.replace(' : Gorillavid','').replace(' : Divxstage','').replace(' : Movshare','').replace(' : Sharesix','').replace(' : Movpod','').replace(' : Daclips','').replace(' : Videoweed','')
        name=name.replace(' : Played','').replace(' : MovDivx','').replace(' : Movreel','').replace(' : BillionUploads','').replace(' : Putlocker','').replace(' : Sockshare','').replace(' : Nowvideo','').replace(' : 180upload','').replace(' : Filenuke','').replace(' : Flashx','').replace(' : Novamov','').replace(' : Uploadc','').replace(' : Xvidstage','').replace(' : Zooupload','').replace(' : Zalaa','').replace(' : Vidxden','').replace(' : Vidbux','')
        name=name.replace(' 720p BRRip','').replace(' 720p HDRip','').replace(' 720p WEBRip','').replace(' 720p BluRay','')
        name=name.replace('  Part:1','').replace('  Part:2','').replace('  Part:3','').replace('  Part:4','')
        match=re.compile('(.+?)xocx(.+?)xocx').findall(url)
        for hurl, durl in match:
            url=geturl('http://watchseries.lt'+hurl)
    match2=re.compile('iwatchonline').findall(url)
    if match2:
        name=name.split('[COLOR red]')[0]
        name=name.replace('/','').replace('.','')
        url=GetUrliW(url)
    
    name=name.split(' [')[0]
    name=name.split('[')[0]
    name=name.split(' /')[0]
    name=name.split('/')[0]
    if re.findall('billionuploads',url):
        try:
            stream_url =main.resolve_billionuploads(url)
            print "Using Built in BillionUpload Resolver"
            stream_url=stream_url.split('referer')[0]
            stream_url=stream_url.replace('|','')
        except:
            media = urlresolver.HostedMediaFile(url)
            source = media
            stream_url = source.resolve()
            stream_url=stream_url.split('referer')[0]
            stream_url=stream_url.replace('|','')
    elif re.findall('180upload',url):
        try:
            stream_url =main.resolve_180upload(url)
        except:
            media = urlresolver.HostedMediaFile(url)
            source = media
            stream_url = source.resolve()
    else:
        media = urlresolver.HostedMediaFile(url)
        source = media
        if source:
            stream_url = source.resolve()
        else:
            stream_url=url
        
    if stream_url:
            print stream_url
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,2000)")
            if os.path.exists(downloadPath):
                match1=re.compile("flv").findall(stream_url)
                if len(match1)>0:
                    name=name+'.flv'
                match2=re.compile("mkv").findall(stream_url)
                if len(match2)>0:
                    name=name+'.mkv'
                match3=re.compile("mp4").findall(stream_url)
                if len(match3)>0:
                    name=name+'.mp4'
                match4=re.compile("avi").findall(stream_url)
                if len(match4)>0:
                    name=name+'.avi'
                mypath=os.path.join(downloadPath,name)
                if os.path.isfile(mypath) is True:
                    xbmc.executebuiltin("XBMC.Notification(Download Alert!,The video you are trying to download already exists!,8000)")
                else:
                    DownloadInBack=selfAddon.getSetting('download-in-background')
                    if DownloadInBack == 'true':
                        QuietDownload(stream_url,mypath,originalName,name)
                    else:
                        Download(stream_url,mypath,originalName,name)
            
            else:
                xbmc.executebuiltin("XBMC.Notification(Download Alert!,You have not set the download folder,8000)")
                return False
                
    else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Not Found,6000)")
            stream_url = False


def GetNoobroom():
        link=OPENURL('http://www.noobroom.com')
        match=re.compile('value="(.+?)">').findall(link)
        return match[0]            
def Noobroom(page_url):
    import re
    import urllib2
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36', 'Cookie':'place=1; save=1'}

    user = selfAddon.getSetting('username')
    passw = selfAddon.getSetting('password')
    url=GetNoobroom()+'/login2.php'
    log_in = net().http_POST(url,{'email':user,'password':passw}).content
    html = net().http_GET(page_url).content
    media_id = re.compile('"file": "(.+?)"').findall(html)[0]
    fork_url = re.compile('"streamer": "(.+?)"').findall(html)[0] + '&start=0&file=' + media_id
    #print fork_url

    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):    
        def http_error_302(self, req, fp, code, msg, headers):
            self.video_url = headers['Location']
            #print self.video_url
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302

    myhr = MyHTTPRedirectHandler()

    opener = urllib2.build_opener(myhr)
    urllib2.install_opener(opener)

    req = urllib2.Request(fork_url)
    for k, v in headers.items():
                req.add_header(k, v)
    try:            
        response = urllib2.urlopen(req)
    except:
        pass

    return myhr.video_url    

def Download_SourceB(name,url):#starplay/noobroom
    originalName=name
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")

    stream_url= Noobroom(url)
    name=name.split(' [')[0]
    name=name.replace('/','').replace('.','')

    if stream_url:
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,2000)")
            if os.path.exists(downloadPath):
                match1=re.compile("flv").findall(stream_url)
                if len(match1)>0:
                    name=name+'.flv'
                match2=re.compile("mkv").findall(stream_url)
                if len(match2)>0:
                    name=name+'.mkv'
                match3=re.compile("mp4").findall(stream_url)
                if len(match3)>0:
                    name=name+'.mp4'
                match4=re.compile("avi").findall(stream_url)
                if len(match4)>0:
                    name=name+'.avi'
                mypath=os.path.join(downloadPath,name)
                if os.path.isfile(mypath) is True:
                    xbmc.executebuiltin("XBMC.Notification(Download Alert!,The video you are trying to download already exists!,8000)")
                else:
                    DownloadInBack=selfAddon.getSetting('download-in-background')
                    if DownloadInBack == 'true':
                        QuietDownload(stream_url,mypath,originalName,name)
                    else:
                        Download(stream_url,mypath,originalName,name)
            
            else:
                xbmc.executebuiltin("XBMC.Notification(Download Alert!,You have not set the download folder,8000)")
                return False
                
    else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Not Found,6000)")
            stream_url = False

def Download(url, dest,originalName, displayname=False):
         
        if displayname == False:
            displayname=url
        delete_incomplete = selfAddon.getSetting('delete-incomplete-downloads')
        dp = xbmcgui.DialogProgress()
        dp.create('Downloading:    '+displayname)
        start_time = time.time() 
        try: 
            urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))
            open(DownloadFile,'a').write('{name="%s",destination="%s"}'%(originalName,dest))
            
        except:
            if delete_incomplete == 'true':
                #delete partially downloaded file if setting says to.
                while os.path.exists(dest): 
                    try: 
                        os.remove(dest) 
                        break 
                    except: 
                        pass 
            #only handle StopDownloading (from cancel), ContentTooShort (from urlretrieve), and OS (from the race condition); let other exceptions bubble 
            if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): 
                return False 
            else: 
                raise 
            return False
        return True

def QuietDownload(url, dest,originalName, videoname):
    #quote parameters passed to download script     
    q_url = urllib.quote_plus(url)
    q_dest = urllib.quote_plus(dest)
    q_vidname = urllib.quote_plus(videoname)
    q_vidOname = urllib.quote_plus(originalName)
    
    #Create possible values for notification
    notifyValues = [2, 5, 10, 20, 25, 50, 100]

    # get notify value from settings
    NotifyPercent=int(selfAddon.getSetting('notify-percent'))
    
    script = os.path.join( mashpath, 'resources', 'libs', "DownloadInBackground.py" )
    xbmc.executebuiltin( "RunScript(%s, %s, %s, %s, %s, %s)" % ( script, q_url, q_dest, q_vidname,q_vidOname, str(notifyValues[NotifyPercent]) ) )
    return True

 
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            # print ( 
                # percent, 
                # numblocks, 
                # blocksize, 
                # filesize, 
                # currently_downloaded, 
                # kbps_speed, 
                # eta, 
                # ) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s ' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs, e)
            #print percent, mbs, e 
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 
            raise StopDownloading('Stopped Downloading')


def jDownloader(murl):
    match2=re.compile('iwatchonline').findall(murl)
    if match2:
        murl=GetUrliW(murl)
    match=re.compile('watchseries.lt').findall(murl)
    if match:
        match=re.compile('(.+?)xocx(.+?)xocx').findall(murl)
        for hurl, durl in match:
            murl=geturl('http://watchseries.lt'+hurl)
    print "Downloading "+murl+" via jDownlaoder"
    cmd = 'plugin://plugin.program.jdownloader/?action=addlink&url='+murl
    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % cmd)

################################################################################ Message ##########################################################################################################

def Message():
    help = SHOWMessage()
    help.doModal()
    main.GA("None","Mash2k3Info")
    del help


class SHOWMessage(xbmcgui.Window):
    def __init__(self):
        self.addControl(xbmcgui.ControlImage(0,0,1280,720,art+'/infoposter.png'))
    def onAction(self, action):
        if action == 92 or action == 10:
            xbmc.Player().stop()
            self.close()

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()
    
################################################################################ Google Analytics ##########################################################################################################


def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(selfAddon.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    selfAddon.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = selfAddon.getSetting('visitor_ga')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'   =========================='
        try:
            repo = os.path.join(repopath, 'addon.xml')
            repofile = open(repo, 'r').read()
            repov=re.compile('name="All Addons by Mash2k3" version="(.+?)" provider-name="Mash2k3').findall(repofile)
            if repov:
                RepoVer = repov[0]
                
        except:
            RepoVer='Repo Not Intalled'
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = selfAddon.getSetting('visitor_ga')
        for build, PLATFORM in match:
            if re.search('12.0',build,re.IGNORECASE): 
                build="Frodo" 
            if re.search('11.0',build,re.IGNORECASE): 
                build="Eden" 
            if re.search('13.0',build,re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            print "Repo Ver. "+RepoVer
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+"MashUp v"+VERSION+"/ Repo v"+RepoVer+"*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+"MashUp v"+VERSION+"/ Repo v"+RepoVer+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================"

 
checkGA()

################################################################################ Types of Directories ##########################################################################################################

def addDirT(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='DIR'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,plot,type)]
        script1=Dir+'/resources/scripts/addFavsTv.py'
        script2=Dir+'/resources/scripts/delFavsTv.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 

def addPlayT(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='PLAY'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,plot,type)]
        script1=Dir+'/resources/scripts/addFavsTv.py'
        script2=Dir+'/resources/scripts/delFavsTv.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok 

def addDirTE(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        infoLabels =GETMETAEpiT(name,iconimage,'')
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        if selfAddon.getSetting("meta-view") != "true":
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        type='DIR'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,str(img),str(plot),type)]
        script1=Dir+'/resources/scripts/addFavsTE.py'
        script2=Dir+'/resources/scripts/delFavsTE.py'
        
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='episode'
                cname=infoLabels['title']               
                sea=infoLabels['season']
                epi=infoLabels['episode']
                imdb_id=infoLabels['imdb_id']
                if imdb_id != '':
                    Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=779&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type, imdb_id,sea,epi)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=780&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type,imdb_id,sea,epi)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 


def addPlayTE(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        mname=name
        if re.findall('sceper',url):
            mname=name.split('&')[0]
        infoLabels =GETMETAEpiT(mname,iconimage,plot)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        if selfAddon.getSetting("meta-view") != "true":
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        type='PLAY'
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,str(img),str(plot),type)]
        script1=Dir+'/resources/scripts/addFavsTE.py'
        script2=Dir+'/resources/scripts/delFavsTE.py'
        
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='episode'
                cname=infoLabels['title']
                sea=infoLabels['season']
                epi=infoLabels['episode']
                imdb_id=infoLabels['imdb_id']
                if imdb_id != '':
                    Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=779&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type, imdb_id,sea,epi)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=780&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type,imdb_id,sea,epi)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDirM(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        infoLabels =GETMETAT(name,genre,fanart,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                tmdbid=infoLabels['tmdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        if selfAddon.getSetting("meta-view") != "true":
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        type='DIR'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,str(plot),type)]
        script1=Dir+'/resources/scripts/addFavsM.py'
        script2=Dir+'/resources/scripts/delFavsM.py'
        
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=infoLabels['title']
                Commands.append(('Play Trailer','XBMC.RunPlugin(%s?mode=782&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],cname,url,imdb)))
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 


def addPlayM(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        infoLabels =GETMETAT(name,genre,fanart,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                tmdbid=infoLabels['tmdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        if selfAddon.getSetting("meta-view") != "true":
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        type='PLAY'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,str(plot),type)]
        script1=Dir+'/resources/scripts/addFavsM.py'
        script2=Dir+'/resources/scripts/delFavsM.py'
        
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=infoLabels['title']
                Commands.append(('Play Trailer','XBMC.RunPlugin(%s?mode=782&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],cname,url,imdb)))
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
    
def addDirMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='DIR'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,str(plot),type)]
        script1=Dir+'/resources/scripts/addFavsMs.py'
        script2=Dir+'/resources/scripts/delFavsMs.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 

def addPlayMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='PLAY'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,plot,type)]
        script1=Dir+'/resources/scripts/addFavsMs.py'
        script2=Dir+'/resources/scripts/delFavsMs.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDirL(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='DIR'
        
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,str(plot),type)]
        script1=Dir+'/resources/scripts/addFavsL.py'
        script2=Dir+'/resources/scripts/delFavsL.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 

def addPlayL(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='PLAY'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,plot,type)]
        script1=Dir+'/resources/scripts/addFavsL.py'
        script2=Dir+'/resources/scripts/delFavsL.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addPlayc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems=[]
        if iconimage==None:
            iconimage=''
        if plot==None:
            plot=''
        if fanart==None:
            fanart=''
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
    
def addDirb(name,url,mode,iconimage,fanart):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirHome(name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('[COLOR green]Switch[/COLOR]Up', 'XBMC.RunPlugin(%s?mode=783&name=%s&url=%s)' % (sys.argv[0],'SwitchUp','switchup')))
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(name,url,mode,iconimage,plot):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&plot="+str(plot)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirFIX(name,url,mode,iconimage,location,path):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&location="+urllib.quote_plus(location)+"&path="+urllib.quote_plus(path)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDown(name,url,mode,iconimage,fan):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        link=OPENURL(url)
        match=re.compile("Javascript:location.?href=.+?'(.+?)\'").findall(link)
        if len(match)>0:
            for url in match:
                sysurl = urllib.quote_plus(url)
        else:
            sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        contextMenuItems.append(('Direct Download', 'XBMC.RunPlugin(%s?mode=190&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        contextMenuItems.append(('Download with jDownloader', 'XBMC.RunPlugin(%s?mode=776&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fan)
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDown2(name,url,mode,iconimage,fan):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        contextMenuItems.append(('Direct Download', 'XBMC.RunPlugin(%s?mode=190&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        contextMenuItems.append(('Download with jDownloader', 'XBMC.RunPlugin(%s?mode=776&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fan)
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDown3(name,url,mode,iconimage,fanart):#starplay only
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        infoLabels =GETMETAT(name,'','',iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                tmdbid=infoLabels['tmdb_id']
                plot=infoLabels['plot']
                name=infoLabels['title']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        if selfAddon.getSetting("meta-view") != "true":
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'

            plot='Sorry description not available'
            plot=plot.replace(",",'.')
        name=name.replace(",",'')
        sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        
        type='PLAY'
        args=[(url,name,mode,iconimage,plot,type)]
        script1=Dir+'/resources/scripts/addFavsM.py'
        script2=Dir+'/resources/scripts/delFavsM.py'
        
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")"),
                  ('Direct Download', 'XBMC.RunPlugin(%s?mode=212&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl))]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=infoLabels['title']
                Commands.append(('Play Trailer','XBMC.RunPlugin(%s?mode=782&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],cname,url,imdb)))
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDown4(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        Commands=[]
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        if re.findall('(.+?)\ss(\d+)e(\d+)\s',name,re.I):
            infoLabels =GETMETAEpiT(name,iconimage,plot)
            video_type='episode'
            sea=infoLabels['season']
            epi=infoLabels['episode']
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            script1=Dir+'/resources/scripts/addFavsTE.py'
            script2=Dir+'/resources/scripts/delFavsTE.py'
        elif re.findall('Season(.+?)Episode([^<]+)',name,re.I):
            infoLabels =GETMETAEpiT(name,iconimage,plot)
            video_type='episode'
            sea=infoLabels['season']
            epi=infoLabels['episode']
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            script1=Dir+'/resources/scripts/addFavsTE.py'
            script2=Dir+'/resources/scripts/delFavsTE.py'
        else:
            infoLabels =GETMETAT(name,genre,fanart,iconimage)
            video_type='movie'
            tmdbid=infoLabels['tmdb_id']
            xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
            script1=Dir+'/resources/scripts/addFavsM.py'
            script2=Dir+'/resources/scripts/delFavsM.py'
        if selfAddon.getSetting("meta-view") == "true":
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        if selfAddon.getSetting("meta-view") != "true":
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        type='PLAY'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,str(plot),type)]
        if '</sublink>' not in url:
            Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")"),
                  ('Direct Download', 'XBMC.RunPlugin(%s?mode=190&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)),
                  ('Download with jDownloader', 'XBMC.RunPlugin(%s?mode=776&name=%s&url=%s)' % (sys.argv[0], sysname, url))]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=infoLabels['title']
                Commands.append(('Play Trailer','XBMC.RunPlugin(%s?mode=782&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],cname,url,imdb)))
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        if '</sublink>' in url:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addInfo(name,url,mode,iconimage,gen,year):
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        name=name.replace('()','')
        infoLabels = GETMETAT(name,gen,year,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                tmdbid=infoLabels['tmdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        args=[(url,name)]
        script1=Dir+'/resources/scripts/addFavs.py'
        script2=Dir+'/resources/scripts/delFavs.py'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=infoLabels['title']
                Commands.append(('Play Trailer','XBMC.RunPlugin(%s?mode=782&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],cname,url,imdb)))
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addDirIWO(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        infoLabels =GETMETAT(name,genre,fanart,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                tmdbid=infoLabels['tmdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        if selfAddon.getSetting("meta-view") != "true":
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        type='DIR'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",".").replace('"','')
        name=name.replace(",",'')
        iconimage=iconimage.replace(",",".")
        args=[(url,name,mode,iconimage,str(plot),type)]
        script1=Dir+'/resources/scripts/addFavsIWO.py'
        script2=Dir+'/resources/scripts/delFavsIWO.py'
        
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's","XBMC.RunScript(" + script1 + ", " + str(args) + ")"),
              ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's","XBMC.RunScript(" + script2 + ", " + str(args) + ")")]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=infoLabels['title']
                Commands.append(('Play Trailer','XBMC.RunPlugin(%s?mode=782&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],cname,url,imdb)))
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 
def addInfo2(name,url,mode,iconimage,plot):
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        infoLabels = GETMETAShow(name)
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.setInfo( type="Video", infoLabels=infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addDLog(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        if re.findall('(.+?)\ss(\d+)e(\d+)\s',name,re.I):
            infoLabels =GETMETAEpiT(name,iconimage,plot)
            video_type='episode'
            sea=infoLabels['season']
            epi=infoLabels['episode']
        elif re.findall('Season(.+?)Episode([^<]+)',name,re.I):
            infoLabels =GETMETAEpiT(name,iconimage,plot)
            video_type='episode'
            sea=infoLabels['season']
            epi=infoLabels['episode']
        else:
            infoLabels =GETMETAT(name,genre,fanart,iconimage)
            video_type='movie'
            tmdbid=infoLabels['tmdb_id']
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        if selfAddon.getSetting("meta-view") != "true":
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        type='PLAY'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        Commands=[("[B][COLOR red]Remove[/COLOR][/B]",'XBMC.RunPlugin(%s?mode=243&name=%s&url=%s)'% (sys.argv[0],name,url))]
        if selfAddon.getSetting("meta-view") == "true":
                
                imdb=infoLabels['imdb_id']
                cname=infoLabels['title']
                Commands.append(('Play Trailer','XBMC.RunPlugin(%s?mode=782&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],cname,url,imdb)))
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok    

def addSpecial(name,url,mode,iconimage):
    liz=xbmcgui.ListItem(name,iconImage="",thumbnailImage = iconimage)
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)

def addSearchDir(name,url, mode,iconimage):
    #thumbnail = 'DefaultPlaylist.png'
    u         = sys.argv[0]+"?url="+urllib.quote_plus(url) + "?mode=" + str(mode)        
    liz       = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty('fanart_image', Dir+'fanart.jpg')
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)
