# -*- coding: latin-1 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui
from operator import itemgetter
pluginhandle = int(sys.argv[1])

def CATEGORIES():
        addDir('Action','http://videokatalog.msn.de/movies/teaser/katalog/3/6/3',1,'')
        addDir('Comedy','http://videokatalog.msn.de/movies/teaser/katalog/3/6/5',1,'')
        addDir('Drama','http://videokatalog.msn.de/movies/teaser/katalog/3/6/6',1,'')
        addDir('Sci-Fi','http://videokatalog.msn.de/movies/teaser/katalog/3/6/7',1,'')
        addDir('Thriller','http://videokatalog.msn.de/movies/teaser/katalog/3/6/8',1,'')
        addDir('Western','http://videokatalog.msn.de/movies/teaser/katalog/3/6/9',1,'')
        addDir('Kids','http://videokatalog.msn.de/movies/teaser/katalog/3/6/10',1,'')

                       
def INDEX(url):#1
        req = urllib2.Request(url)
#        print url
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        movies=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" target=".+?"><img src="(.+?)" alt="(.+?)" title=".+?" /></a>').findall(movies)
	match_sorted=sorted(match, key=itemgetter(2))
        for url,thumb,name in match_sorted:
		name = name.replace("&#039;","'")
		name = name.replace("&amp;","&")
		addLink(name,url,2,'http://videokatalog.msn.de'+thumb)

def VIDEOLINKS(url,name):#2
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link_video=response.read()
        response.close()
	#print match
#        match=re.compile("formatCode: (.+?), url: '(.+?)'").findall(link_video)
        match=re.compile("formatCode: .+?, url: '(.+?)'").findall(link_video)
	#{formatCode: 1002, url: 'http\x3a\x2f\x2fcontent5.catalog.video.msn.com\x2fe2\x2fds\x2fde-de\x2fDEDE_Videovalis\x2fDEDE_Videovalis_Thriller\x2fa7dc35a1-bc31-4de5-8768-431b30353cc0.mp4'}

        #formatCode: 1002, url: 'http\x3a\x2f\x2fcontent4.catalog.video.msn.com\x2fe2\x2fds\x2fde-de\x2fDEDE_Videovalis\x2fDEDE_Videovalis_SciFi\x2f5d05254d-67aa-447e-a9e4-da8e4e6eae42.mp4
#        for formatcode,url in match:
#		urla = url.replace("\\x3a",":")
#		urlb = urla.replace("\\x2f","/")
#                addLink('Play '+formatcode,urlb,'')
	url = match[-1].replace("\\x3a",":")
	url = url.replace("\\x2f","/")
        item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

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




#def addLink(name,url,iconimage):
#        ok=True
#        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
#        liz.setInfo( type="Video", infoLabels={ "Title": name } )
#        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
#        return ok

def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

              
params=get_params()
url=None
name=None
mode=None
total=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        total=str(params["total"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)

elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
