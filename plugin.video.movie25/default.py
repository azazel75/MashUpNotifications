#-*- coding: utf-8 -*-
import urllib,urllib2,re,cookielib,string, urlparse
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urlresolver,os,time
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net
from metahandler import metahandlers
import datetime,time
from resources.libs import main, movie25


#Mash Up - by Mash2k3 2012.

Mainurl ='http://www.movie25.com/movies/'
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
grab = metahandlers.MetaData(preparezip = False)
addon = Addon(addon_id)
art = main.art
from universal import watchhistory
wh = watchhistory.WatchHistory('plugin.video.movie25')



################################################################################ Source Imports ##########################################################################################################

from resources.libs import youtube, youplaylist, downloadedcontent

from resources.libs.documentaries import vice, documentary, watchdocumentary, documentarywire

from resources.libs.sports import wildtv, golfchannel,  fitnessblender, skysports, tsn, espn, foxsoccer, outdoorch, mmafighting, bodybuilding

from resources.libs.kids import disneyjr, wbkids

from resources.libs.adventure import discovery, airaces, nationalgeo

from resources.libs.plugins import seriesgate, sominaltvfilms, dubzonline, globalbc, btvguide, watchseries, sceper, extramina, fma, iwatchonline, animefreak

from resources.libs.live import livestation, hadynz, oneeightone, vipplaylist, naviplaylists, ilive, castalba, desistreams, musicstreams, countries,tubtub, customchannel

from resources.libs.movies_tv import oneclickwatch, movieplaylist, mkvmovies, pencurimovie, backuptv, rlsmix, newmyvideolinks, dailyflix, oneclickmoviez, starplay, movie1k

from resources.libs.international import  einthusan, cinevip


################################################################################ Directories ##########################################################################################################
updatepath=os.path.join(main.datapath,'Update')
try:
    os.makedirs(updatepath)
except:
    pass
UpdateFile=os.path.join(updatepath,'updatetracker')


def AtoZ():
        main.addDir('0-9','http://www.movie25.com/movies/0-9/',1,art+'/09.png')
        for i in string.ascii_uppercase:
                main.addDir(i,'http://www.movie25.com/movies/'+i.lower()+'/',1,art+'/'+i.lower()+'.png')
        main.GA("None","Movie25-A-Z")   
def MAIN():
        mashup=132
        notified=os.path.join(main.datapath,str(mashup))
        if not os.path.exists(notified):
            open(notified,'w').write('version="%s",'%mashup)
            dir = addon.get_path()
            chlg = os.path.join(dir, 'changelog.txt')
            TextBoxes("[B][COLOR red]MashUp Changelog[/B][/COLOR]",chlg)
            mashup=mashup-1
            notified=os.path.join(main.datapath,str(mashup))
            if  os.path.exists(notified):
                os.remove(notified)
        if selfAddon.getSetting("switchup") == "false":
                main.addDirHome('Search','http://www.movie25.com/',420,art+'/search2.png')
                main.addDirHome("All Fav's",'http://www.movie25.com/',639,art+'/favsu.png')
                main.addDirHome('A-Z','http://www.movie25.com/',6,art+'/AZ2.png')
                main.addDirHome('New Releases','http://www.movie25.com/movies/new-releases/',1,art+'/new2.png')
                main.addDirHome('Latest Added','http://www.movie25.com/movies/latest-added/',1,art+'/latest2.png')
                main.addDirHome('Featured Movies','http://www.movie25.com/movies/featured-movies/',1,art+'/feat2.png')
                main.addDirHome('Most Viewed','http://www.movie25.com/movies/most-viewed/',1,art+'/view2.png')
                main.addDirHome('Most Voted','http://www.movie25.com/movies/most-voted/',1,art+'/vote2.png')
                main.addDirHome('HD Releases','http://www.movie25.com/movies/latest-hd-movies/',1,art+'/dvd2hd.png')
                main.addDirHome('Genre','http://www.movie25.com/',2,art+'/genre2.png')
                main.addDirHome('By Year','http://www.movie25.com/',7,art+'/year2.png')
        else:
                main.addDirHome('Search','http://www.iwatchonline.to',644,art+'/search+.png')
                main.addDirHome("All Fav's",'http://www.movie25.com/',639,art+'/gfavsu.png')
                main.addDirHome('A-Z','http://www.iwatchonline.to',595,art+'/AZ+.png')
                main.addDirHome('Upcoming','http://www.iwatchonline.to/main/content_more/movies/?sort=upcoming&start=0',587,art+'/new+.png')
                main.addDirHome('Latest Added','http://www.iwatchonline.to/main/content_more/movies/?sort=latest&start=0',587,art+'/latest+.png')
                main.addDirHome('Featured Movies','http://www.iwatchonline.to/main/content_more/movies/?sort=featured&start=0',587,art+'/feat+.png')
                main.addDirHome('Popular','http://www.iwatchonline.to/main/content_more/movies/?sort=popular&start=0',587,art+'/view+.png')
                main.addDirHome('Latest DVD Movies','http://www.iwatchonline.to/main/content_more/movies/?quality=dvd&start=0',587,art+'/dvd+.png')
                main.addDirHome('Latest HD Movies','http://www.iwatchonline.to/main/content_more/movies/?quality=hd&start=0',587,art+'/dvd2+.png')
                main.addDirHome('Genre','http://www.iwatchonline.to',596,art+'/genre+.png')
                main.addDirHome('By Year','year',652,art+'/year+.png')
        main.addDirHome('Watch History','history',222,art+'/whistory.png')
        main.addDirHome('HD Movies','http://oneclickwatch.org/category/movies/',33,art+'/hd2.png')
        main.addDirHome('3D Movies','3D',223,art+'/3d.png')
        main.addDirHome('International','http://www.movie25.com/',36,art+'/intl.png')
        main.addDirHome('TV Latest','http://www.movie25.com/',27,art+'/tv2.png')
        main.addDirHome('Live Streams','http://www.movie25.com/',115,art+'/live.png')
        main.addDirHome('Built in Plugins','http://www.movie25.com/',500,art+'/plugins.png')
        main.addDirHome('[COLOR green]VIP[/COLOR]laylists','http://www.movie25.com/',234,art+'/moviepl.png')
        main.addDirHome('Sports','http://www.movie25.com/',43,art+'/sportsec2.png')
        main.addDirHome('Adventure','http://www.movie25.com/',63,art+'/adv2.png')
        main.addDirHome('Kids Zone','http://www.movie25.com/',76,art+'/kidzone2.png')
        main.addDirHome('Documentaries','http://www.movie25.com/',85,art+'/docsec2.png')
        main.addPlayc('Resolver Settings','http://www.movie25.com/',99,art+'/resset.png','','','','','')
        main.addDirHome('Fixes','http://www.movie25.com/',784,art+'/fixes.png')
        main.addPlayc('Need Help?','http://www.movie25.com/',100,art+'/xbmchub.png','','','','','')
        main.addLink('@mashupxbmc','',art+'/twittermash.png')
        main.addPlayc('Hub Maintenance','http://www.movie25.com/',156,art+'/hubmain.png','','','','','')
        main.addDirHome("MashUp How To's",'PLvNKtQkKaqg-PVXvlP7sYcfiEoaC56v3W',205,art+'/howto.png')
        

        main.CheckVersion()#Checks If Plugin Version is up to date
 
        

        #Announcement Notifier from xml file
        
        try:
                link=main.OPENURL('https://github.com/mash2k3/MashUpNotifications/raw/master/Notifier.xml')
        except:
                link='nill'

        r = re.findall(r'ANNOUNCEMENTWINDOW ="ON"',link)
        if r:
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('<item><new>(.+?)</new><message1>.+?</message1><message2>.+?</message2><message3>.+?</message3><ANNOUNCEMENT>(.+?)</ANNOUNCEMENT><old>(.+?)</old></item>').findall(link)
                if len(match)>0:
                        for new,anounce,old in match:
                                continue
                        if new != ' ':
                                notified=os.path.join(main.datapath,str(new))
                                if not os.path.exists(notified):
                                        open(notified,'w').write('version="%s",'%new)
                                        TextBoxes("[B][COLOR red]MashUp Announcements[/B][/COLOR]",anounce)
                                if old != ' ':
                                        notified=os.path.join(main.datapath,str(old))
                                        if  os.path.exists(notified):
                                                os.remove(notified)
                        else:
                                print 'No Messages'
    
                else:
                    print 'Github Link Down'
                
        
        else:
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('<item><new>(.+?)</new><message1>(.+?)</message1><message2>(.+?)</message2><message3>(.+?)</message3><ANNOUNCEMENT>.+?</ANNOUNCEMENT><old>(.+?)</old></item>').findall(link)
                if len(match)>0:
                        for new,mes1,mes2,mes3,old in match:
                                continue
                        if new != ' ':
                                notified=os.path.join(main.datapath,str(new))
                                if not os.path.exists(notified):
                                        open(notified,'w').write('version="%s",'%new)
                                        dialog = xbmcgui.Dialog()
                                        ok=dialog.ok('[B]Important Announcement![/B]', str(mes1) ,str(mes2),str(mes3))
                                if old != ' ':
                                        notified=os.path.join(main.datapath,str(old))
                                        if  os.path.exists(notified):
                                                os.remove(notified)
                        else:
                                print 'No Messages'
    
                else:
                    print 'Github Link Down'
        main.VIEWSB()


def CheckForUpdate():
        try:
                link2=main.OPENURL('https://github.com/mash2k3/MashUpFixes/raw/master/Fixes.xml')
        except:
                link2='nill'
        link2=link2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<date>(.+?)</date>').findall(link2)
        if len(match)>0:
                date=match[0]
                date=date.replace('/','')
                if not os.path.exists(UpdateFile):
                    open(UpdateFile,'w').write('date="%s"'%(date))
                else:
                    update=re.compile('date="(.+?)"').findall(open(UpdateFile,'r').read())
                    oldDate=update[0]
                    if int(date)>int(oldDate):
                        dialog = xbmcgui.Dialog()
                        ret = dialog.yesno('MashUp Update', 'There is a new fix update available.','Will you like to update now?', 'It is recommended that you update.','No', 'Yes')
                        if ret==True:
                                cmd = 'plugin://plugin.video.movie25/?url=http://www.movie25.com/&mode=784&name=Fixes'
                                xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)
                                open(UpdateFile,'w').write('date="%s"'%(date))
                        else:
                                open(UpdateFile,'w').write('date="%s"'%(date))
                                
                return

        
def GENRE(url):
        main.addDir('Action','http://www.movie25.com/movies/action/',1,art+'/act.png')
        main.addDir('Adventure','http://www.movie25.com/movies/adventure/',1,art+'/adv.png')
        main.addDir('Animation','http://www.movie25.com/movies/animation/',1,art+'/ani.png')
        main.addDir('Biography','http://www.movie25.com/movies/biography/',1,art+'/bio.png')
        main.addDir('Comedy','http://www.movie25.com/movies/comedy/',1,art+'/com.png')
        main.addDir('Crime','http://www.movie25.com/movies/crime/',1,art+'/cri.png')
        main.addDir('Documentary','http://www.movie25.com/movies/documentary/',1,art+'/doc.png')
        main.addDir('Drama','http://www.movie25.com/movies/drama/',1,art+'/dra.png')
        main.addDir('Family','http://www.movie25.com/movies/family/',1,art+'/fam.png')
        main.addDir('Fantasy','http://www.movie25.com/movies/fantasy/',1,art+'/fant.png')
        main.addDir('History','http://www.movie25.com/movies/history/',1,art+'/his.png')
        main.addDir('Horror','http://www.movie25.com/movies/horror/',1,art+'/hor.png')
        main.addDir('Music','http://www.movie25.com/movies/music/',1,art+'/mus.png')
        main.addDir('Musical','http://www.movie25.com/movies/musical/',1,art+'/mucl.png')
        main.addDir('Mystery','http://www.movie25.com/movies/mystery/',1,art+'/mys.png')
        main.addDir('Romance','http://www.movie25.com/movies/romance/',1,art+'/rom.png')
        main.addDir('Sci-Fi','http://www.movie25.com/movies/sci-fi/',1,art+'/sci.png')
        main.addDir('Short','http://www.movie25.com/movies/short/',1,art+'/sho.png')
        main.addDir('Sport','http://www.movie25.com/movies/sport/',1,art+'/sport.png')
        main.addDir('Thriller','http://www.movie25.com/movies/thriller/',1,art+'/thr.png')
        main.addDir('War','http://www.movie25.com/movies/war/',1,art+'/war.png')
        main.addDir('Western','http://www.movie25.com/movies/western/',1,art+'/west.png')
        main.GA("None","Movie25-Genre")
        main.VIEWSB()
        
def YEAR():
        main.addDir('2013','http://www.movie25.com/search.php?year=2013/',8,art+'/year.png')
        main.addDir('2012','http://www.movie25.com/search.php?year=2012/',8,art+'/2012.png')
        main.addDir('2011','http://www.movie25.com/search.php?year=2011/',8,art+'/2011.png')
        main.addDir('2010','http://www.movie25.com/search.php?year=2010/',8,art+'/2010.png')
        main.addDir('2009','http://www.movie25.com/search.php?year=2009/',8,art+'/2009.png')
        main.addDir('2008','http://www.movie25.com/search.php?year=2008/',8,art+'/2008.png')
        main.addDir('2007','http://www.movie25.com/search.php?year=2007/',8,art+'/2007.png')
        main.addDir('2006','http://www.movie25.com/search.php?year=2006/',8,art+'/2006.png')
        main.addDir('2005','http://www.movie25.com/search.php?year=2005/',8,art+'/2005.png')
        main.addDir('2004','http://www.movie25.com/search.php?year=2004/',8,art+'/2004.png')
        main.addDir('2003','http://www.movie25.com/search.php?year=2003/',8,art+'/2003.png')
        main.addDir('Enter Year','http://www.movie25.com',23,art+'/enteryear.png')
        main.GA("None","Movie25-Year")
        main.VIEWSB()

def GlobalFav():
        main.addLink("[COLOR red]MashUp Fav's can also be favorited under XBMC favorites[/COLOR]",'','')
        main.addDir("Downloaded Content",'MashUp',241,art+'/downloadlog.png')
        main.addDir("Movie25 Fav's",'http://www.movie25.com/',10,art+'/fav2.png')
        main.addDir("iWatchOnline Fav's",'http://www.movie25.com/',655,art+'/fav2+.png')
        main.addDir("Movie Fav's",'http://www.movie25.com/',641,art+'/fav.png')
        main.addDir("TV Show Fav's",'http://www.movie25.com/',640,art+'/fav.png')
        main.addDir("TV Episode Fav's",'http://www.movie25.com/',651,art+'/fav.png')
        main.addDir("Live Fav's",'http://www.movie25.com/',648,art+'/fav.png')
        main.addDir("Misc. Fav's",'http://www.movie25.com/',650,art+'/fav.png')



    
def TV():
        mashup='metadata'
        notified=os.path.join(main.datapath,str(mashup))
        if not os.path.exists(notified):
            open(notified,'w').write('type="%s",'%mashup)
            dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
            chlg = os.path.join(dir, 'metadata.txt')
            TextBoxes("[B][COLOR red]Important Announcement![/B][/COLOR]",chlg)
        main.addDir('Latest Episodes (Newmyvideolinks) True HD[COLOR red] DC[/COLOR]','TV',34,art+'/tvb.png')
        main.addDir('Latest Episodes (Rlsmix)[COLOR red](Debrid Only)[/COLOR] True HD[COLOR red] DC[/COLOR]','TV',61,art+'/tvb.png')
        main.addDir('Latest Episodes (Sceper)[COLOR red](Debrid Only)[/COLOR] True HD','http://sceper.ws/home/category/tv-shows',545,art+'/tvb.png')
        main.addDir('Latest Episodes (Watchseries)','http://watchseries.lt/tvschedule/-1',573,art+'/tvb.png')
        main.addDir('Latest Episodes (iWatchonline)','http://www.iwatchonline.to/tv-schedule',592,art+'/tvb.png')
        main.addDir('Latest Episodes (Movie1k)','movintv',30,art+'/tvb.png')
        main.addDir('Latest Episodes (Oneclickwatch)','http://oneclickwatch.org',32,art+'/tvb.png')
        main.addDir('Latest Episodes (Seriesgate)','http://seriesgate.tv/latestepisodes/',602,art+'/tvb.png')
        main.addDir('Latest Episodes (BTV Guide)','todays',555,art+'/tvb.png')
        main.addLink('[COLOR red]Back Up Sources[/COLOR]','','')
        main.addDir('Latest 150 Episodes (ChannelCut)','http://www.channelcut.me/last-150',546,art+'/tvb.png')
        main.addDir('Latest 100 Episodes (Tv4stream)','http://www.tv4stream.info/last-100-links/',546,art+'/tvb.png')
        main.GA("None","TV-Latest")


def ThreeDsec():
        mashup='metadata'
        notified=os.path.join(main.datapath,str(mashup))
        if not os.path.exists(notified):
            open(notified,'w').write('type="%s",'%mashup)
            dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
            chlg = os.path.join(dir, 'metadata.txt')
            TextBoxes("[B][COLOR red]Important Announcement![/B][/COLOR]",chlg)
        main.addDir('3D Movies (Newmyvideolinks) True HD[COLOR red] DC[/COLOR]','3D',34,art+'/3d.png')
        main.addDir('3D Movies (MkvMovies) True HD','http://mkvmovies.gamezonewap.info/search/label/3D',224,art+'/3d.png')


def TVAll():
        mashup='metadata'
        notified=os.path.join(main.datapath,str(mashup))
        if not os.path.exists(notified):
            open(notified,'w').write('type="%s",'%mashup)
            dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
            chlg = os.path.join(dir, 'metadata.txt')
            TextBoxes("[B][COLOR red]Important Announcement![/B][/COLOR]",chlg)
        #main.addDir('Watch-Free Series','TV',501,art+'/wfs/wsf.png')
        main.addDir('Watchseries.it[COLOR red] DC[/COLOR]','TV',572,art+'/wfs/watchseries.png')
        main.addDir('BTV Guide','TV',551,art+'/wfs/btvguide.png')
        main.addDir('Series Gate','TV',601,art+'/wfs/sg.png')
        main.addDir('iWatchOnline [COLOR red] DC[/COLOR]','TV',584,art+'/iwatchonline.png')
        main.addDir('TV-Release [COLOR red](Works Best With Debrid)[/COLOR]','tvr',1000,art+'/tvrelease.png')
        main.addDir('Sceper [COLOR red](Debrid Only)[/COLOR]','TV',539,art+'/wfs/sceper.png')
        main.addDir('SominalTvFilms','TV',619,art+'/wfs/sominal.png')
        main.addDir('Extramina','TV',530,art+'/wfs/extramina.png')
        main.addDir('FMA','TV',567,art+'/wfs/fma.png')
        main.addDir('dubzonline','TV',613,art+'/wfs/dubzonline.png')
        main.addDir('AnimeFreak TV','TV',625,art+'/animefreak.png')
        main.addDir('Global BC','gbc',165,art+'/globalbc.png')
        main.GA("None","Plugin")

def HD():
        mashup='metadata'
        notified=os.path.join(main.datapath,str(mashup))
        if not os.path.exists(notified):
            open(notified,'w').write('type="%s",'%mashup)
            dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
            chlg = os.path.join(dir, 'metadata.txt')
            TextBoxes("[B][COLOR red]Important Announcement![/B][/COLOR]",chlg)
            
        main.addDir('Latest HD Movies (Newmyvideolinks) True HD[COLOR red] DC[/COLOR]','http://newmyvideolinks.com',34,art+'/hd2.png')
        main.addDir('Latest HD Movies (Dailyfix) True HD','HD',53,art+'/hd2.png')
        main.addDir('Latest HD Movies (Starplay/[COLOR green]Noobroom7[/COLOR]) Direct MP4 True HD[COLOR red] DC[/COLOR]','http://noobroom7.com/latest.php',57,art+'/hd2.png')
        main.addDir('Latest HD Movies (Pencurimovie) Direct MP4 True HD','http://www.pencurimovie.com/feeds/posts/default?max-results=1000',215,art+'/hd2.png')
        main.addDir('Latest HD Movies (Oneclickmovies)[COLOR red](Debrid Only)[/COLOR] True HD[COLOR red] DC[/COLOR]','www.scnsrc.me',55,art+'/hd2.png')
        main.addDir('Latest HD Movies (Sceper)[COLOR red](Debrid Only)[/COLOR] True HD','http://sceper.ws/category/movies/movies-bluray-rip',541,art+'/hd2.png')
        main.addDir('Latest HD Movies (Oneclickwatch)','http://oneclickwatch.org/category/movies/',25,art+'/hd2.png')
        #main.addLink('[COLOR red]Back Up Sources[/COLOR]','','')
        main.GA("None","HD")
def INT():
        mashup='metadata'
        notified=os.path.join(main.datapath,str(mashup))
        if not os.path.exists(notified):
            open(notified,'w').write('type="%s",'%mashup)
            dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
            chlg = os.path.join(dir, 'metadata.txt')
            TextBoxes("[B][COLOR red]Important Announcement![/B][/COLOR]",chlg)
        main.addDir('Latest Indian Subtitled Movies (einthusan)','http://www.einthusan.com',37,art+'/intl.png')
        main.addDir('Latest Hindi/Tamil/Telugu & more (sominaltv)','TV',619,art+'/intl.png')
        main.addDir('Latest Indian Movies (Movie1k)','movin',30,art+'/intl.png')
        main.addDir('Latest Indian Dubbed Movies (Movie1k)','movindub',30,art+'/intl.png')
        main.addDir('Latest Spanish Dubbed & Subtitled(ESP) Movies (cinevip)','http://www.cinevip.org/',66,art+'/intl.png')
        main.addDir("XcTech's Bollywood Playlist",'PLvNKtQkKaqg8IPssr3WG4-YkOEAe8TQ0j',205,art+'/intl.png')
        main.GA("None","INT")

def SPORTS():
        main.addDir('ESPN','http:/espn.com',44,art+'/espn.png')
        main.addDir('TSN','http:/tsn.com',95,art+'/tsn.png')
        main.addDir('SkySports.com','www1.skysports.com',172,art+'/skysports.png')
        main.addDir('Fox Soccer  [COLOR red](US ONLY)[/COLOR]','http:/tsn.com',124,art+'/foxsoc.png')
        main.addDir('All MMA','mma',537,art+'/mma.png')
        main.addDir('Outdoor Channel','http://outdoorchannel.com/',50,art+'/OC.png')
        main.addDir('Wild TV','https://www.wildtv.ca/shows',92,art+'/wildtv.png')
        main.addDir('Workouts','https://www.wildtv.ca/shows',194,art+'/workout.png')
        main.addDir('The Golf Channel','golf',217,art+'/golfchannel.png')
        main.GA("None","Sports")

def MMA():
        main.addDir('UFC','ufc',59,art+'/ufc.png')
        main.addDir('Bellator','BellatorMMA',47,art+'/bellator.png')
        main.addDir('MMA Fighting.com','http://www.mmafighting.com/videos',113,art+'/mmafig.png')

def WorkoutMenu():
        main.addDir('Fitness Blender[COLOR red](Full Workouts)[/COLOR]','fb',198,art+'/fitnessblender.png')
        main.addDir('Insanity','http://watchseries.lt/serie/INSANITY_-_The_Asylum',578,art+'/insanity.png')
        main.addDir('P90X','http://watchseries.lt/serie/p90x',578,art+'/p90x.png')
        main.addDir('Body Building[COLOR red](Instructional Only)[/COLOR]','bb',195,art+'/bodybuilding.png')
        

def UFC():
        main.addDir('UFC.com','ufc',47,art+'/ufc.png')
        main.addDir('UFC(Movie25)','ufc',60,art+'/ufc.png')
        main.addDir('UFC(Newmyvideolinks)','ufc',103,art+'/ufc.png')
        main.GA("None","UFC")

def ADVENTURE():
        main.addDir('Discovery Channel','http://dsc.discovery.com/videos',631,art+'/disco.png')
        main.addDir('National Geographic','ng',70,art+'/natgeo.png')
        main.addDir('Military Channel','http://military.discovery.com/videos',80,art+'/milcha.png')
        main.addDir('Science Channel','http://science.discovery.com/videos',81,art+'/scicha.png')
        main.addDir('Velocity Channel','http://velocity.discovery.com/videos',82,art+'/velo.png')
        main.addDir('Animal Planet','http://animal.discovery.com/videos',83,art+'/anip.png')
        main.GA("None","Adventure")
        


def KIDZone(murl):
        main.addDir('Disney Jr.','djk',107,art+'/disjr.png')
        main.addDir('National Geographic Kids','ngk',71,art+'/ngk.png')
        main.addDir('WB Kids','wbk',77,art+'/wb.png')
        main.addDir('Youtube Kids','wbk',84,art+'/youkids.png')
        main.GA("None","KidZone")
        main.VIEWSB()
    
def LiveStreams():
        #Announcement Notifier from xml file
        try:
                link=main.OPENURL('https://github.com/mash2k3/MashUpNotifications/raw/master/NotifierLive.xml')
        except:
                link='nill'

        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<item><new>(.+?)</new><message1>(.+?)</message1><message2>(.+?)</message2><message3>(.+?)</message3><old>(.+?)</old></item>').findall(link)
        if len(match)>0:
                for new,mes1,mes2,mes3,old in match:
                        continue
                if new != ' ':
                        notified=os.path.join(main.datapath,str(new))
                        if not os.path.exists(notified):
                                open(notified,'w').write('version="%s",'%new)
                                dialog = xbmcgui.Dialog()
                                ok=dialog.ok('[B]Live Section Announcement![/B]', str(mes1) ,str(mes2),str(mes3))
                        if old != ' ':
                                notified=os.path.join(main.datapath,str(old))
                                if  os.path.exists(notified):
                                        os.remove(notified)
                else:
                        print 'No Messages'
    
        else:
            print 'Github Link Down'
        main.addDir('Livestation News','http://mobile.livestation.com/',116,art+'/livestation.png')
        main.addDir('iLive Streams','ilive',119,art+'/ilive.png')
        #main.addDir('Desi Streams','desi',129,art+'/desistream.png')
        main.addDir('Castalba Streams','castalgba',122,art+'/castalba.png')
        main.addDir('Misc. Music Streams','music',127,art+'/miscmusic.png')
        #main.addDir('Playlists','navi',138,art+'/random.png')
        main.addDir('By Country','navi',143,art+'/countrysec.png')
        main.addDir('Arabic Streams','navi',231,art+'/arabicstream.png')
        try:
                link=main.OPENURL('https://github.com/mash2k3/MashUpNotifications/raw/master/LiveDirectory(mash2k3Only).xml')
        except:
                link=main.OPENURL('https://mash2k3-repository.googlecode.com/svn/trunk/LiveDirectory%28mash2k3Only%29.xml')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('type=playlistname=Sorted by user-assigned order','').replace('name=Sorted [COLOR=FF00FF00]by user-assigned order[/COLOR]','').replace('name=Live Tv Channels Twothumb','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode>').findall(link)
        for name,url,thumb,mode in match:
                if re.findall('http',thumb):
                    thumbs=thumb
                else:
                    thumbs=art+'/'+thumb+'.png'
                main.addDir(name,url,int(mode),thumbs)
        main.addDir('Live TV','https://github.com/mash2k3/MashUpStreams/raw/master/playlists/generallivetv.xml',149,art+'/livetv.png')
        main.addDir('UK TV','https://github.com/mash2k3/MashUpStreams/raw/master/playlists/liveuktv.xml',141,art+'/uktv.png')
        if selfAddon.getSetting("customchannel") == "true":
                main.addDir('My XML Channels','nills',238,art+'/xml.png')
        main.addDir('TubTub.com','http://tubtub.com/',185,art+'/tubtub.png')
        main.addDir('181.FM Radio Streams','nills',191,art+'/181fm.png')
        
        main.GA("None","Live")

def DOCS():
        main.addDir('Vice','http://www.vice.com/shows',104,art+'/vice.png')
        main.addDir('Documentary Heaven','doc1',86,art+'/dh.png')
        main.addDir('Watch Documentary','doc1',159,art+'/watchdoc.png')
        main.addDir('Documentary Wire','doc1',226,art+'/docwire.png')
        main.addDir('Top Documentary Films','doc2',86,art+'/topdoc.png')
        main.addDir('Documentary Log','doc3',86,art+'/doclog.png')
        main.addDir('Documentaries (Movie25)','http://www.movie25.com/movies/documentary/',1,art+'/doc.png')
        main.GA("None","Documentary")


def PlaylistDir():
        try:
                link=main.OPENURL('https://github.com/mash2k3/MashUpNotifications/raw/master/MoviePlaylist_Dir.xml')
        except:
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Movie Playlist Down,5000,"")")
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode>').findall(link)
        for name,url,thumb,mode in match:
                if re.findall('http',thumb):
                    thumbs=thumb
                else:
                    thumbs=art+'/'+thumb+'.png'
                main.addDir(name,url,int(mode),thumbs)
        main.GA("None","MoviePL")

def FIXES():
        main.addLink('[COLOR red]Apply fix only if your current one is broken[/COLOR]','','')
        try:
                link=main.OPENURL('https://github.com/mash2k3/MashUpFixes/raw/master/Fixes.xml')
        except:
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Repo is Down,5000,"")")
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<item><name>([^<]+)</name.+?filename>([^<]+)</filename.+?location>([^<]+)</location.+?path>([^<]+)</path.+?thumbnail>([^<]+)</thumbnail></item>').findall(link)
        for name,filename,location,path,thumb in match:
                main.addDirFIX(name,filename,785,art+'/'+thumb+'.png',location,path)

def FIXDOWN(name,filename,location,path):
    main.GA("Fixes",name+"-Fix")
    url = 'https://dl.dropboxusercontent.com/u/35068738/FIXES'+filename
    print "#############  Downloading from "+ url+"  #####################"
    path = xbmc.translatePath(os.path.join(str(location),str(path)))
    lib=os.path.join(path, str(filename))
    DownloaderClass(url,lib)
    dialog = xbmcgui.Dialog()
    name  = name.split('[COLOR red]')[0]
    dialog.ok("MashUp", "Thats It All Done", "[COLOR blue]Now "+name+" should be Fixed[/COLOR]")
        
################################################################################ XBMCHUB Repo & Hub Maintenance Installer ##########################################################################################################


hubpath = xbmc.translatePath(os.path.join('special://home/addons', ''))
maintenance=os.path.join(hubpath, 'plugin.video.hubmaintenance')



def DownloaderClass(url,dest):
        dp = xbmcgui.DialogProgress()
        dp.create("MashUp","Downloading & Copying File",'')
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
        try:
            percent = min((numblocks*blocksize*100)/filesize, 100)
            dp.update(percent)
        except:
            percent = 100
            dp.update(percent)
        if (dp.iscanceled()): 
            print "DOWNLOAD CANCELLED" # need to get this part working
            return False
        dp.close()
        del dp
def HubMain():
            ok=True
            cmd = 'plugin://plugin.video.hubmaintenance/'
            xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)
            return ok
hubrepo = xbmc.translatePath(os.path.join('special://home/addons', 'repository.xbmchub'))
try:  
    if not os.path.exists(hubrepo): 
        url = 'http://xbmc-hub-repo.googlecode.com/svn/addons/repository.xbmchub/repository.xbmchub-1.0.1.zip'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, 'repository.xbmchub-1.0.1.zip')
        DownloaderClass(url,lib)
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
        time.sleep(2)
        xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
except:
    pass

repopath = xbmc.translatePath(os.path.join('special://home/addons', 'repository.mash2k3'))
try: 
    if not os.path.exists(repopath):
        url = 'https://bitbucket.org/mash2k3/mash2k3-repository/src/a3be11dd1482e4b08fcc3905b9150971117e7955/zips/repository.mash2k3/repository.mash2k3-1.5.zip?at=master'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, 'repository.mash2k3-1.5.zip')
        DownloaderClass(url,lib)
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
        time.sleep(2)
        xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
except:
    pass
################################################################################ XBMCHUB POPUP ##########################################################################################################


class HUB( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/xbmchub.mp3'%selfAddon.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()
        if controlID == 7:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()
        
def pop():
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUB('hub1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    if xbmc.getCondVisibility('system.platform.android'):
        popup = HUB('hub1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    else:
        popup = HUB('hub.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    popup.doModal()
    del popup

################################################################################ Favorites Function##############################################################################################################
def ListglobalFavIWO():
        favpath=os.path.join(main.datapath,'Favourites')
        tvfav=os.path.join(favpath,'Movies')
        FavFile=os.path.join(tvfav,'IWOFav')
        if os.path.exists(FavFile):
                Favs=re.compile('url="(.+?)",name="(.+?)",mode="(.+?)",thumb="(.+?)",plot="(.+?)",type="(.+?)"').findall(open(FavFile,'r').read())
                for url,name,mode,thumb,plot,type in Favs:
                        if type=='PLAY':
                                main.addPlayM(name,url,int(mode),thumb,plot,'','','','')
                        if type=='DIR':
                                main.addDirM(name,url,int(mode),thumb,plot,'','','','')
                
        else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR green]Mash Up[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
        main.GA("None","IWO-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()

def ListglobalFavT():
        favpath=os.path.join(main.datapath,'Favourites')
        tvfav=os.path.join(favpath,'TV')
        FavFile=os.path.join(tvfav,'TVFav')
        if os.path.exists(FavFile):
                Favs=re.compile('url="(.+?)",name="(.+?)",mode="(.+?)",thumb="(.+?)",plot="(.+?)",type="(.+?)"').findall(open(FavFile,'r').read())
                for url,name,mode,thumb,plot,type in Favs:
                        if type=='PLAY':
                                main.addPlayT(name,url,int(mode),thumb,plot,'','','','')
                        if type=='DIR':
                                main.addDirT(name,url,int(mode),thumb,plot,'','','','')
                
        else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR green]Mash Up[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
        main.GA("None","TV-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        
def ListglobalFavTE():
        favpath=os.path.join(main.datapath,'Favourites')
        tvfav=os.path.join(favpath,'TV')
        FavFile=os.path.join(tvfav,'TVEpiFav')
        if os.path.exists(FavFile):
                Favs=re.compile('url="(.+?)",name="(.+?)",mode="(.+?)",thumb="(.+?)",plot="(.+?)",type="(.+?)"').findall(open(FavFile,'r').read())
                for url,name,mode,thumb,plot,type in Favs:
                        if type=='PLAY':
                                main.addPlayTE(name,url,int(mode),thumb,plot,'','','','')
                        if type=='DIR':
                                main.addDirTE(name,url,int(mode),thumb,plot,'','','','')
                
        else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR green]Mash Up[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
        main.GA("None","TVEPI-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavM():
        favpath=os.path.join(main.datapath,'Favourites')
        tvfav=os.path.join(favpath,'Movies')
        FavFile=os.path.join(tvfav,'OtherFav')
        if os.path.exists(FavFile):
                Favs=re.compile('url="(.+?)",name="(.+?)",mode="(.+?)",thumb="(.+?)",plot="(.+?)",type="(.+?)"').findall(open(FavFile,'r').read())
                for url,name,mode,thumb,plot,type in Favs:
                        if type=='PLAY':
                                main.addPlayM(name,url,int(mode),thumb,plot,'','','','')
                        if type=='DIR':
                                main.addDirM(name,url,int(mode),thumb,plot,'','','','')
                
        else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR green]Mash Up[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
        main.GA("None","Movie-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavMs():
        favpath=os.path.join(main.datapath,'Favourites')
        tvfav=os.path.join(favpath,'Misc')
        FavFile=os.path.join(tvfav,'MiscFav')
        if os.path.exists(FavFile):
                Favs=re.compile('url="(.+?)",name="(.+?)",mode="(.+?)",thumb="(.+?)",plot="(.+?)",type="(.+?)"').findall(open(FavFile,'r').read())
                for url,name,mode,thumb,plot,type in Favs:
                        if type=='PLAY':
                                main.addPlayMs(name,url,int(mode),thumb,plot,'','','','')
                        if type=='DIR':
                                main.addDirMs(name,url,int(mode),thumb,plot,'','','','')
                
        else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR green]Mash Up[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
        main.GA("None","Misc-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavL():
        favpath=os.path.join(main.datapath,'Favourites')
        tvfav=os.path.join(favpath,'Live')
        FavFile=os.path.join(tvfav,'LiveFav')
        if os.path.exists(FavFile):
                Favs=re.compile('url="(.+?)",name="(.+?)",mode="(.+?)",thumb="(.+?)",plot="(.+?)",type="(.+?)"').findall(open(FavFile,'r').read())
                for url,name,mode,thumb,plot,type in Favs:
                        if type=='PLAY':
                                main.addPlayL(name,url,int(mode),thumb,plot,'','','','')
                        if type=='DIR':
                                main.addDirL(name,url,int(mode),thumb,plot,'','','','')
                
        else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR green]Mash Up[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
        main.GA("None","Live-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    
################################################################################ Histroy ##########################################################################################################

def History():
    main.GA("None","WatchHistory")
    if selfAddon.getSetting("whistory") == "true":
        history_items = wh.get_my_watch_history()
        for item in history_items:
                item_title = item['title']
                item_url = item['url']
                item_image = item['image_url']
                item_fanart = item['fanart_url']
                item_infolabels = item['infolabels']
                item_isfolder = item['isfolder']
                if item_image =='':
                    item_image= art+'/noimage.png'
                main.addLink(item_title,item_url,item_image)
    else:
        dialog = xbmcgui.Dialog()
        ok=dialog.ok('[B]MashUp History[/B]', 'Watch history is disabled' ,'To enable go to addon settings','and enable Watch History')
        history_items = wh.get_my_watch_history()
        for item in history_items:
                item_title = item['title']
                item_url = item['url']
                item_image = item['image_url']
                item_fanart = item['fanart_url']
                item_infolabels = item['infolabels']
                item_isfolder = item['isfolder']
                main.addLink(item_title,item_url,item_image)
    
        


    
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
################################################################################ Modes ##########################################################################################################


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None
title=None
season=None
episode=None
location=None
path=None


try:
        name=urllib.unquote_plus(params["name"])
except:
        pass

try:
        
        url=urllib.unquote_plus(params["url"])
        
except:
        pass

try:
        mode=int(params["mode"])
except:
        pass

try:
        iconimage=urllib.unquote_plus(params["iconimage"])
        iconimage = iconimage.replace(' ','%20')
except:
        pass
try:
        plot=urllib.unquote_plus(params["plot"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
        fanart = fanart.replace(' ','%20')
except:
        pass

try:
        genre=urllib.unquote_plus(params["genre"])
except:
        pass

try:
        title=urllib.unquote_plus(params["title"])
except:
        pass
try:
        episode=int(params["episode"])
except:
        pass
try:
        season=int(params["season"])
except:
        pass
try:
        location=urllib.unquote_plus(params["location"])
except:
        pass
try:
        path=urllib.unquote_plus(params["path"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
        print ""
        MAIN()
        CheckForUpdate()
                
       
elif mode==1:
        print ""+url
        movie25.LISTMOVIES(url)
        
elif mode==2:
        print ""+url
        GENRE(url)

elif mode==4:
        print ""+url
        movie25.SEARCH(url)
        
elif mode==420:
        print ""+url
        movie25.Searchhistory()

elif mode==3:
        print ""+url
        movie25.VIDEOLINKS(name,url)

elif mode==5:
        print ""+url
        movie25.PLAY(name,url)

elif mode==171:
        print ""+url
        movie25.PLAYB(name,url)
elif mode==6:
        AtoZ()

elif mode==7:
        YEAR()

elif mode==23:
        movie25.ENTYEAR()
        
elif mode==8:
        print ""+url
        movie25.YEARB(url)

elif mode==9:
        print ""+url
        movie25.NEXTPAGE(url)
        
elif mode==10:
        movie25.FAVS()

elif mode==11:
        print ""+url
        movie25.PUTLINKS(name,url)

elif mode==12:
        print ""+url
        movie25.OELINKS(name,url)

elif mode==13:
        print ""+url
        movie25.FNLINKS(name,url)

elif mode==14:
        print ""+url
        movie25.VIDLINKS(name,url)

elif mode==15:
        print ""+url
        movie25.FLALINKS(name,url)

elif mode==16:
        print ""+url
        movie25.NOVLINKS(name,url)

elif mode==17:
        print ""+url
        movie25.UPLINKS(name,url)

elif mode==18:
        print ""+url
        movie25.XVLINKS(name,url)

elif mode==19:
        print ""+url
        movie25.ZOOLINKS(name,url)

elif mode==20:
        print ""+url
        movie25.ZALINKS(name,url)

elif mode==21:
        print ""+url
        movie25.VIDXLINKS(name,url)

elif mode==22:
        print ""+url
        movie25.SOCKLINKS(name,url)

elif mode==24:
        print ""+url
        movie25.NOWLINKS(name,url)

elif mode==25:
        print ""+url
        oneclickwatch.LISTSP(url)

elif mode==26:
        print ""+url
        oneclickwatch.LINKSP(name,url)
        
elif mode==27:
        print ""+url
        TV()

elif mode==28:
        print ""+url
        iwatchonline.LISTTV(url)
        
elif mode==29:
        print ""+url
        iwatchonline.VIDEOLINKST(name,url)

elif mode==30:
        print ""+url
        movie1k.LISTTV2(url)

elif mode==31:
        print ""+url
        movie1k.VIDEOLINKST2(name,url,iconimage)
        
elif mode==32:
        print ""+url
        oneclickwatch.LISTTV3(url)

elif mode==33:
        print ""+url
        HD()

elif mode==34:
        print ""+url
        newmyvideolinks.LISTSP2(url)

elif mode==35:
        print ""+url
        newmyvideolinks.LINKSP2(name,url)

elif mode==36:
        print ""+url
        INT()

elif mode==37:
        print ""+url
        einthusan.LISTINT(name,url)

elif mode==38:
        print ""+url
        einthusan.LINKINT(name,url)

######39-42 available
        
elif mode==43:
        print ""+url
        SPORTS()

elif mode==44:
        print ""+url
        espn.ESPN()
        
elif mode==45:
        print ""+url
        espn.ESPNList(url)

elif mode==46:
        print ""+url
        espn.ESPNLink(name,url,iconimage,plot)

elif mode==47:
        print ""+url
        youtube.YOUList(name,url)
        
elif mode==48:
        print ""+url
        youtube.YOULink(name,url,iconimage)

elif mode==50:
        print ""+url
        outdoorch.OC()
        
elif mode==51:
        print ""+url
        outdoorch.OCList(url)

elif mode==52:
        print ""+url
        outdoorch.OCLink(name,url,iconimage)

elif mode==53:
        print ""+url
        dailyflix.LISTSP3(url)

elif mode==54:
        print ""+url
        dailyflix.LINKSP3(name,url)

elif mode==55:
        print ""+url
        oneclickmoviez.LISTSP4(url)

elif mode==56:
        print ""+url
        oneclickmoviez.LINKSP4(name,url)

elif mode==57:
        print ""+url
        starplay.LISTSP5(url)

elif mode==58:
        print ""+url
        starplay.LINKSP5(name,url)
        
elif mode==59:
        print ""+url
        UFC()
        
elif mode==60:
        print ""+url
        movie25.UFCMOVIE25()

elif mode==61:
        print ""+url
        rlsmix.LISTTV4(url)

elif mode==62:
        print ""+url
        rlsmix.LINKTV4(name,url)

elif mode==63:
        print ""+url
        ADVENTURE()
        
elif mode==631:
        print ""+url
        discovery.DISC(url)

elif mode==64:
        print ""+url
        discovery.LISTDISC(name,url)

elif mode==65:
        print ""+url
        discovery.LINKDISC(name,url)

elif mode==66:
        print ""+url
        cinevip.LISTINT3(url)

elif mode==67:
        print ""+url
        cinevip.LINKINT3(name,url,iconimage)

elif mode==68:
        print ""+url
        useme(url)

elif mode==69:
        print ""+url
        useMe(name,url)

elif mode==70:
        print ""+url
        nationalgeo.NG()

elif mode==71:
        print ""+url
        nationalgeo.NGDir(url)

elif mode==72:
        print ""+url
        nationalgeo.LISTNG(url)

elif mode==73:
        print ""+url
        nationalgeo.LISTNG2(url)

elif mode==74:
        print ""+url
        nationalgeo.LINKNG(name,url)

elif mode==75:
        print ""+url
        nationalgeo.LINKNG2(name,url)

elif mode==76:
        print ""+url
        KIDZone(url)
        
elif mode==77:
        print ""+url
        wbkids.WB()
        
elif mode==78:
        print ""+url
        wbkids.LISTWB(url)

elif mode==79:
        print ""+url
        wbkids.LINKWB(name,url)

elif mode==80:
        print ""+url
        discovery.MILIT(url)
        
elif mode==81:
        print ""+url
        discovery.SCI(url)

elif mode==82:
        print ""+url
        discovery.VELO(url)

elif mode==83:
        print ""+url
        discovery.ANIP(url)

elif mode==84:
        print ""+url
        youtube.YOUKIDS()

elif mode==85:
        print ""+url
        DOCS()        

elif mode==86:
        print ""+url
        documentary.LISTDOC(url)
        
elif mode==87:
        print ""+url
        documentary.LISTDOC2(url)

elif mode==88:
        print ""+url
        documentary.LINKDOC(name,url,iconimage)
        
elif mode==89:
        print ""+url
        documentary.LISTDOCPOP(url)

elif mode==90:
        print ""+url
        airaces.LISTAA()

elif mode==91:
        print ""+url
        airaces.PLAYAA(name,url,iconimage)

elif mode==92:
        print ""+url
        wildtv.WILDTV(url)        

elif mode==93:
        print ""+url
        wildtv.LISTWT(url)
        
elif mode==94:
        print ""+url
        wildtv.LINKWT(name,url)

elif mode==95:
        print ""+url
        tsn.TSNDIR()

elif mode==96:
        print ""+url
        tsn.TSNDIRLIST(url)        

elif mode==97:
        print ""+url
        tsn.TSNLIST(url)
        
elif mode==98:
        print ""+url
        tsn.TSNLINK(name,url,iconimage)
        
elif mode==99:
        urlresolver.display_settings()
        
elif mode==100:
        pop()
        
elif mode==101:
        newmyvideolinks.SEARCHNEW(name,url)

elif mode==102:
        newmyvideolinks.SearchhistoryNEW(url)
        
elif mode==103:
        newmyvideolinks.UFCNEW()
        
elif mode==104:
        vice.Vice(url)
        
elif mode==105:
        vice.ViceList(url)

elif mode==106:        
        vice.ViceLink(name,url,iconimage)        

elif mode==107:
        disneyjr.DISJR()
        
elif mode==108:
        disneyjr.DISJRList(url)

elif mode==109:
        disneyjr.DISJRList2(url)
        
elif mode==110:        
        disneyjr.DISJRLink(name,url,iconimage)       
        
elif mode==111:
        StrikeFList(url)

elif mode==112:        
        StrikeFLink(name,url)   

elif mode==113:
        mmafighting.MMAFList(url)

elif mode==114:        
        mmafighting.MMAFLink(name,url,iconimage)   
elif mode==115:
        LiveStreams()
elif mode==116:
        livestation.LivestationList(url)
elif mode==117:
        livestation.LivestationLink(name,url,iconimage)
elif mode==118:
        livestation.LivestationLink2(name,url,iconimage)

elif mode==119:
        ilive.iLive()
elif mode==120:
        ilive.iLiveList(url)
elif mode==121:
        ilive.iLiveLink(name,url,iconimage)

elif mode==122:
        castalba.CastalbaList(url)
elif mode==123:
        castalba.CastalbaLink(name,url,iconimage)

elif mode==124:
        foxsoccer.FOXSOC()
elif mode==125:
        foxsoccer.FOXSOCList(url)
elif mode==126:
        foxsoccer.FOXSOCLink(name,url)

elif mode==127:
        musicstreams.MUSICSTREAMS()
elif mode==128:
        main.Clearhistory(url)

elif mode==129:
        desistreams.DESISTREAMS()
elif mode==130:
        desistreams.DESISTREAMSList(url)
elif mode==131:
        desistreams.DESISTREAMSLink(name,url)
        
elif mode==132:
        movie1k.SearchhistoryMovie1k()
elif mode==133:
        movie1k.SEARCHMovie1k(url)
elif mode==134:
        oneclickwatch.PLAYOCW(name,url)

elif mode==135:
        oneclickwatch.VIDEOLINKST3(name,url)

elif mode==136:
        rlsmix.SearchhistoryRlsmix()

elif mode==137:
        rlsmix.SEARCHRlsmix(url)


elif mode==138:
       naviplaylists.playlists()

elif mode==139:
        naviplaylists.playlistList(name,url)

elif mode==140:
        naviplaylists.playlistList2(name,url)

elif mode==141:
        naviplaylists.playlistList3(name,url)

elif mode==142:
        naviplaylists.playlistList4(name,url)

elif mode==149:
        naviplaylists.playlistList5(name,url)
        
elif mode==158:
        naviplaylists.playlistList6(name,url)

elif mode==168:
        naviplaylists.playlistList7(name,url)

elif mode==143:
        countries.COUNTRIES()

elif mode==144:
        countries.COUNTRIESList(name,url)

elif mode==204:
        countries.COUNTRIESLink(name,url,iconimage)


elif mode==145:
        print ""+url
        movie25.MOVSHLINKS(name,url)

elif mode==146:
        print ""+url
        movie25.DIVXSLINKS(name,url)

elif mode==147:
        print ""+url
        movie25.SSIXLINKS(name,url)

elif mode==148:
        print ""+url
        movie25.GORLINKS(name,url)

elif mode==150:
        print ""+url
        movie25.MOVPLINKS(name,url)

elif mode==151:
        print ""+url
        movie25.DACLINKS(name,url)

elif mode==152:
        print ""+url
        movie25.VWEEDLINKS(name,url)

elif mode==153:
        print ""+url
        movie25.MOVDLINKS(name,url)

elif mode==154:
        print ""+url
        movie25.MOVRLINKS(name,url)

elif mode==155:
        print ""+url
        movie25.BUPLOADSLINKS(name,url)

elif mode==156:
        print ""+url
        HubMain()

elif mode==157:
        print ""+url
        movie25.PLAYEDLINKS(name,url)

elif mode==159:
        print ""+url
        watchdocumentary.WATCHDOC()

elif mode==160:
        print ""+url
        watchdocumentary.WATCHDOCList(url)

elif mode==161:
        print ""+url
        watchdocumentary.WATCHDOCLink(name,url,iconimage)

elif mode==162:
        print ""+url
        watchdocumentary.CATEGORIES()

elif mode==163:
        print ""+url
        watchdocumentary.WATCHDOCList2(url)

elif mode==164:
        print ""+url
        watchdocumentary.WATCHDOCSearch()

elif mode==165:
        print ""+url
        globalbc.GLOBALBC()

elif mode==166:
        print ""+url
        globalbc.GLOBALBCList(url)

elif mode==167:
        print ""+url
        globalbc.GLOBALBCLink(name,url)

elif mode==169:
        print ""+url
        globalbc.GLOBALBCList2(url)

elif mode==170:
        print ""+url
        globalbc.GLOBALBCSearch()

#171 taken



elif mode==172:
        print ""+url
        skysports.SKYSPORTS()

elif mode==173:
        print ""+url
        skysports.SKYSPORTSList(url)

elif mode==174:
        print ""+url
        skysports.SKYSPORTSLink(name,url)

elif mode==175:
        print ""+url
        skysports.SKYSPORTSTV(url)

elif mode==176:
        print ""+url
        skysports.SKYSPORTSList2(url)
        
elif mode==177:
        dialog = xbmcgui.Dialog()
        dialog.ok("Mash Up", "Sorry this video requires a SkySports Suscription.","Will add this feature in later Version.","Enjoy the rest of the videos ;).")

elif mode==178:
        print ""+url
        skysports.SKYSPORTSCAT()

elif mode==179:
        print ""+url
        skysports.SKYSPORTSCAT2(url)

elif mode==180:
        print ""+url
        skysports.SKYSPORTSTEAMS(url)

elif mode==181:
        print ""+url
        vipplaylist.VIPplaylists(url)

elif mode==182:
        print ""+url
        vipplaylist.VIPList(name,url)

elif mode==183:
        print ""+url
        vipplaylist.VIPLink(name,url,iconimage)


elif mode==184:
        print ""+url
        musicstreams.MUSICSTREAMSLink(name,url,iconimage)


elif mode==185:
        print ""+url
        tubtub.TubTubMAIN(url)

elif mode==186:
        print ""+url
        tubtub.TubTubLink(name,url)

elif mode==187:
        print ""+url
        arabic.ArabicMAIN(url)

elif mode==188:
        print ""+url
        arabic.ArabicLink(name,url)

elif mode==189:
        print ""+url
        arabic.ArabicList(url)

elif mode==190:
        print ""+url
        main.Download_Source(name,url)


elif mode==191:
        print ""+url
        oneeightone.MAINFM()

elif mode==192:
        print ""+url
        oneeightone.LISTFM(name,url)

elif mode==193:
        print ""+url
        oneeightone.LINKFM(name,url)

elif mode==194:
        print ""+url
        WorkoutMenu()

elif mode==195:
        print ""+url
        bodybuilding.MAINBB()

elif mode==196:
        print ""+url
        bodybuilding.LISTBB(url)

elif mode==197:
        print ""+url
        bodybuilding.LINKBB(name,url,iconimage)

elif mode==198:
        print ""+url
        fitnessblender.MAINFB()

elif mode==199:
        print ""+url
        fitnessblender.BODYFB()

elif mode==200:
        print ""+url
        fitnessblender.DIFFFB()

elif mode==201:
        print ""+url
        fitnessblender.TRAINFB()

elif mode==202:
        print ""+url
        fitnessblender.LISTBF(url)

elif mode==203:
        print ""+url
        fitnessblender.LINKBB(name,url,iconimage)

elif mode==205:
        print ""+url
        youplaylist.YOUList(name,url)

elif mode==206:
        print ""+url
        youplaylist.YOULink(name,url,iconimage)

elif mode==207:
        print ""+url
        movie25.GotoPage(url)

elif mode==208:
        print ""+url
        movie25.GotoPageB(url)

elif mode==209:
        print ""+url
        newmyvideolinks.LINKSP2B(name,url)
        
elif mode==210:
        print ""+url
        rlsmix.LINKTV4B(name,url)

elif mode==211:
        print ""+url
        oneclickmoviez.LINKSP4B(name,url)

elif mode==212:
        print ""+url
        main.Download_SourceB(name,url)
        
elif mode == 213 or mode == 214:
        if xbmc.Player().isPlayingAudio():
                info   = xbmc.Player().getMusicInfoTag()
                artist = info.getTitle().split(' - ')[0]
                track  = info.getTitle()
                track  = track.split(' (')[0]
                print track
                artist=artist.replace('f/','ft ')
                cmd = '%s?mode=%s&name=%s&artist=%s' % ('plugin://plugin.audio.xbmchubmusic/', str(mode), track, artist)
                xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)



elif mode==215:
        print ""+url
        pencurimovie.LIST(url)


elif mode==216:
        print ""+url
        pencurimovie.LINK(name,url,iconimage)


elif mode==217:
        golfchannel.MAIN()
        
elif mode==218:
        print ""+url
        golfchannel.LIST(url)

elif mode==219:
        print ""+url
        golfchannel.LIST2(name,url,iconimage,plot)


elif mode==220:
        print ""+url
        golfchannel.LINK(name,url,iconimage)

elif mode==221:
        print ""+url
        golfchannel.LIST3(url)


elif mode==222:
        print ""+url
        History()

elif mode==223:
        print ""+url
        ThreeDsec()

elif mode==224:
        print ""+url
        mkvmovies.LIST(url)

elif mode==225:
        print ""+url
        mkvmovies.LINK(name,url,iconimage)


elif mode==226:
        documentarywire.MAIN()
        
elif mode==227:
        print ""+url
        documentarywire.LIST(url)

elif mode==228:
        print ""+url
        documentarywire.LINK(name,url,iconimage,plot)

elif mode==229:
        print ""+url
        documentarywire.SEARCH(url)

elif mode==230:
        print ""+url
        documentarywire.CATLIST(url)


elif mode==231:
        print ""+url
        hadynz.MAIN()

elif mode==232:
        print ""+url
        hadynz.LINK(name,url,iconimage)

elif mode==233:
        print ""+url
        


elif mode==234:
        print ""+url
        PlaylistDir()


elif mode==235:
        print ""+url
        movieplaylist.Mplaylists(url)

elif mode==236:
        print ""+url
        movieplaylist.MList(name,url)

elif mode==237:
        print ""+url
        movieplaylist.MLink(name,url,iconimage)


elif mode==238:
        print ""+url
        customchannel.MAIN()

elif mode==239:
        print ""+url
        customchannel.LIST(name,url)

elif mode==240:
        print ""+url
        customchannel.LINK(name,url,iconimage)

elif mode==241:
        print ""+url
        downloadedcontent.LIST()

elif mode==242:
        print ""+url
        downloadedcontent.LINK(name,url)

elif mode==243:
        print ""+url
        downloadedcontent.REMOVE(name,url)
######################################################################################################
        ######################################################################################
        ######################################################################################
        ######################################################################################

        
elif mode==500:
        TVAll()        

elif mode==530:
        extramina.MAINEXTRA()

elif mode==531:
        print ""+url
        extramina.LISTEXgenre(url)

elif mode==532:
        print ""+url
        extramina.LISTEXrecent(url)


elif mode==533:
        print ""+url
        extramina.GENREEXTRA(url)

elif mode==534:
        print ""+url
        extramina.SEARCHEXTRA(url)
        
elif mode==535:
        print ""+url
        extramina.SearchhistoryEXTRA()

elif mode==536:
        print ""+url
        extramina.VIDEOLINKSEXTRA(name,url,iconimage,plot)
                
elif mode==538:
        print ""+url
        extramina.AtoZEXTRA()

elif mode==537:
        print ""+url
        MMA()        

elif mode==539:
        sceper.MAINSCEPER()
        
elif mode==540:
        sceper.MORTSCEPER(url)

elif mode==541:
        print ""+url
        sceper.LISTSCEPER(name,url)
        
elif mode==545:
        print ""+url
        sceper.LISTSCEPER2(name,url)

elif mode==542:
        print ""+url
        sceper.SEARCHSCEPER(url)
        
elif mode==543:
        print ""+url
        sceper.SearchhistorySCEPER()

elif mode==544:
        print ""+url
        sceper.VIDEOLINKSSCEPER(name,url,iconimage)

elif mode==546:
        print ""+url
        backuptv.CHANNELCList(url)

elif mode==547:
        print ""+url
        backuptv.CHANNELCLink(name,url)

elif mode==548:
        print ""+url
        newmyvideolinks.LISTEtowns(url)

elif mode==549:
        newmyvideolinks.SEARCHEtowns(url)

elif mode==550:
        newmyvideolinks.SearchhistoryEtowns(url)

elif mode==551:
        btvguide.MAINBTV()

elif mode==552:
        print ""+url
        btvguide.LISTShowsBTV(url)

elif mode==553:
        print ""+url
        btvguide.LISTSeasonBTV(name,url,iconimage)

elif mode==554:
        print ""+url
        btvguide.LISTEpilistBTV(name,url)

elif mode==555:
        print ""+url
        btvguide.LISTPopBTV(url)

elif mode==556:
        print ""+url
        btvguide.GENREBTV(url)

elif mode==557:
        print ""+url
        btvguide.SEARCHBTV(url)
        
elif mode==558:
        print ""+url
        btvguide.SearchhistoryBTV()

elif mode==559:
        print ""+url
        btvguide.VIDEOLINKSBTV(name,url)     
        
elif mode==560:
        print ""+url
        btvguide.AtoZBTV()
        
elif mode==561:
        print ""+url
        btvguide.AllShowsBTV(url)
elif mode==562:
        print ""+url
        btvguide.LISTPOPShowsBTV(url)

elif mode==563:
        print ""+url
        btvguide.PLAYBTV(name,url)
elif mode==564:
        print ""+url
        btvguide.LISTNEWShowsBTV(url)
elif mode==565:
        print ""+url
        btvguide.LISTNEWEpiBTV(url)

elif mode==566:
        print ""+url
        btvguide.DECADEBTV(url)
        

elif mode==567:
        print ""+url
        fma.MAINFMA()

elif mode==568:
        print ""+url
        fma.LISTFMA(url)
        
elif mode==569:
        print ""+url
        fma.LINKFMA(name,url,iconimage,plot)
        
elif mode==570:
        print ""+url
        fma.AtoZFMA()
        
elif mode==571:
        print ""+url
        fma.GENREFMA(url)

elif mode==646:
        print ""+url
        fma.SearchhistoryM()
        
elif mode==647:
        print ""+url
        fma.SEARCHM(url)

elif mode==572:
        print ""+url
        watchseries.MAINWATCHS()

elif mode==573:
        print ""+url
        watchseries.LISTWATCHS(url)

elif mode==574:
        print ""+url
        watchseries.LINKWATCHS(name,url)

elif mode==575:
        print ""+url
        watchseries.LISTHOST(name,url)

elif mode==576:
        print ""+url
        watchseries.LISTSHOWWATCHS(url)

elif mode==577:
        print ""+url
        watchseries.AtoZWATCHS()
        
elif mode==578:
        print ""+url
        watchseries.LISTWATCHSEASON(name, url)

elif mode==579:
        print ""+url
        watchseries.LISTWATCHEPISODE(name, url)
        
elif mode==580:
        print ""+url
        watchseries.POPULARWATCHS(url)

elif mode==581:
        print ""+url
        watchseries.SearchhistoryWS()
        
elif mode==582:
        print ""+url
        watchseries.SEARCHWS(url)

elif mode==583:
        print ""+url
        watchseries.GENREWATCHS()

elif mode==584:
        print ""+url
        iwatchonline.iWatchMAIN()

elif mode==642:
        print ""+url
        iwatchonline.SearchhistoryTV()
        
elif mode==643:
        print ""+url
        iwatchonline.SEARCHTV(url)

elif mode==644:
        print ""+url
        iwatchonline.SearchhistoryM()
        
elif mode==645:
        print ""+url
        iwatchonline.SEARCHM(url)

elif mode==585:
        print ""+url
        iwatchonline.iWatchTV()

elif mode==586:
        print ""+url
        iwatchonline.iWatchMOVIES()

elif mode==587:
        print ""+url
        iwatchonline.iWatchLISTMOVIES(url)

elif mode==588:
        print ""+url
        iwatchonline.iWatchLINK(name,url)

elif mode==589:
        print ""+url
        iwatchonline.iWatchLISTSHOWS(url)

elif mode==590:
        print ""+url
        iwatchonline.iWatchSeason(name,url,iconimage)

elif mode==591:
        print ""+url
        iwatchonline.iWatchEpisode(name,url)

elif mode==592:
        print ""+url
        iwatchonline.iWatchToday(url)

elif mode==593:
        print ""+url
        iwatchonline.AtoZiWATCHtv()

elif mode==594:
        print ""+url
        iwatchonline.iWatchGenreTV()

elif mode==595:
        print ""+url
        iwatchonline.AtoZiWATCHm()

elif mode==596:
        print ""+url
        iwatchonline.iWatchGenreM()
      

elif mode==601:
        seriesgate.MAINSG()
        
elif mode==602:
        print ""+url
        seriesgate.LISTEpiSG(url)

elif mode==603:
        print ""+url
        seriesgate.LISTShowsSG(url)

elif mode==604:
        print ""+url
        seriesgate.LISTSeasonSG(name,url,iconimage)

elif mode==605:
        print ""+url
        seriesgate.LISTEpilistSG(name,url)

elif mode==606:
        print ""+url
        seriesgate.LISTPopSG(url)

elif mode==607:
        print ""+url
        seriesgate.GENRESG(url)

elif mode==608:
        print ""+url
        seriesgate.SEARCHSG(url)
        
elif mode==612:
        print ""+url
        seriesgate.SearchhistorySG()

elif mode==609:
        print ""+url
        seriesgate.VIDEOLINKSSG(name,url,iconimage)
       
elif mode==610:
        print ""+url
        seriesgate.AtoZSG()
        
elif mode==611:
        print ""+url
        seriesgate.AllShows(url)


elif mode==613:
        dubzonline.MAINdz()
        
elif mode==614:
        print ""+url
        dubzonline.AtoZdz()

elif mode==615:
        print ""+url
        dubzonline.AZLIST(name,url)

elif mode==616:
        print ""+url
        dubzonline.EPILIST(url)

elif mode==617:
        print ""+url
        dubzonline.LINK(name,url)

elif mode==618:
        print ""+url
        dubzonline.latestLIST(url)


elif mode==619:
        sominaltvfilms.MAIN()
        
elif mode==620:
        print ""+url
        sominaltvfilms.LIST(name,url)

elif mode==621:
        print ""+url
        sominaltvfilms.LINK(name,url,iconimage,fanart,plot)

elif mode==622:
        print ""+url
        sominaltvfilms.LINK2(name,url,iconimage,plot)

elif mode==623:
        print ""+url
        sominaltvfilms.AtoZ(url)
        
elif mode==624:
        print ""+url
        sominaltvfilms.SEARCH()

elif mode==625:
        animefreak.MAIN()
        
elif mode==626:
        print ""+url
        animefreak.LIST(name,url)

elif mode==627:
        print ""+url
        animefreak.LINK(name,url,iconimage,plot)

elif mode==628:
        print ""+url
        animefreak.AtoZ()

elif mode==629:
        print ""+url
        animefreak.AZLIST(name,url)

elif mode==630:
        print ""+url
        animefreak.LIST2(name,url,iconimage,plot)
        
elif mode==632:
        print ""+url
        animefreak.LATESTE(name,url)

elif mode==633:
        print ""+url
        animefreak.LATESTA(name,url)

elif mode==634:
        print ""+url
        animefreak.GENRE(url)
        
elif mode==635:
        print ""+url
        animefreak.GENRELIST(url)

elif mode==636:
        print ""+url
        animefreak.LATESTA(name,url)

elif mode==637:
        print ""+url
        animefreak.LISTPOP(url)

elif mode==638:
        print ""+url
        animefreak.SEARCH()

elif mode==639:
        print ""+url
        GlobalFav()

elif mode==640:
        print ""+url
        ListglobalFavT()

elif mode==641:
        print ""+url
        ListglobalFavM()

#642-47 taken

elif mode==648:
        print ""+url
        ListglobalFavL()

elif mode==649:
        print ""+url
        iwatchonline.iWatchLINKB(name,url)
elif mode==650:
        print ""+url
        ListglobalFavMs()
elif mode==651:
        print ""+url
        ListglobalFavTE()
elif mode==652:
        iwatchonline.iWatchYearM()
elif mode==653:
        iwatchonline.ENTYEAR()
elif mode==654:
        iwatchonline.GotoPage(url)

elif mode==655:
        print ""+url
        ListglobalFavIWO()

elif mode == 776:
        main.jDownloader(url)        
elif mode == 777:
        main.ChangeWatched(iconimage, url, name, '', '')

elif mode == 778:
        main.refresh_movie(name,iconimage)
        
elif mode == 779:
        main.ChangeWatched(iconimage, url, name, season, episode)
elif mode == 780:
        main.episode_refresh(name, iconimage, season, episode)
elif mode == 781:
        main.trailer(url)
elif mode == 782:
        main.TRAILERSEARCH(url, name, iconimage)
elif mode == 783:
        main.SwitchUp()
elif mode == 784:
        print ""+url
        FIXES()
elif mode == 785:
        print ""+url
        FIXDOWN(name,url,location,path)
        
elif mode == 1000:
    from resources.libs.plugins import tvrelease
    tvrelease.MAINMENU()
elif mode == 1001:
    from resources.libs.plugins import tvrelease
    tvrelease.INDEX(url)
elif mode == 1002:
    from resources.libs.plugins import tvrelease
    tvrelease.GOTOP(url)
elif mode == 1003:
    from resources.libs.plugins import tvrelease
    tvrelease.LISTHOSTERS(name,url)
elif mode == 1004:
    urlresolver.display_settings()
elif mode == 1005:
    from resources.libs.plugins import tvrelease
    tvrelease.PLAYMEDIA(name,url)
elif mode == 1006:
    from resources.libs.plugins import tvrelease
    tvrelease.SEARCH(url)
elif mode == 1007:
    from resources.libs.plugins import tvrelease
    tvrelease.TVPACKS(url)
    
    
    

elif mode == 2000:
    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
