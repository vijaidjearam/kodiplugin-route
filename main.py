#https://github.com/tamland/kodi-plugin-routing
import routing
from xbmcgui import ListItem, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
import urllib2,urllib,re,requests
import resolveurl as urlresolver
from lib import chromevideo, embedtamilgun, vidorgnet


def getdatacontent_dict(url,reg):
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    req = urllib2.Request(url)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    r = opener.open(req)
    html = r.read()
    r = re.compile(reg)
    data = [m.groupdict() for m in r.finditer(html)]
    return data
def getdatacontent(url,reg):
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    req = urllib2.Request(url)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    r = opener.open(req)
    html = r.read()
    data = re.compile(reg).findall(html)
    return data


plugin = routing.Plugin()
@plugin.route('/')
def index():
    # addDirectoryItem(plugin.handle, plugin.url_for(show_category,"https://6movierulz.com/category/tamil-movie/"), ListItem("Category One"), True)
    # addDirectoryItem(plugin.handle, plugin.url_for(show_category, "two"), ListItem("Category Two"), True)
    # addDirectoryItem(plugin.handle, plugin.url_for(show_directory, "/dir/two"), ListItem("Directory Two"), True)
    url = "http://movierulz.com"
    r = requests.get(url,verify=False) 
    movierulzurl = r.url
    url = movierulzurl+"/category/tamil-movie/"
    get_site_content_regex ='<a href=\"(?P<pageurl>.*?)\"\stitle=\"(?P<title>.*?)\">\s*<img width=\"\d+\" height=\"\d+\" src=\"(?P<poster>.*?)\"'
    get_stream_url_regex = '<p><strong>(?P<streamtitle>.*?)<\/strong><br \/>\s+<a href=\"(?P<streamurl>.*?)\"'
    get_nav_data_regex = '<a href=\"(?P<navlink>.*?)\">&larr;(\s|)Older Entries'
    get_site_content_regex = urllib.quote_plus(get_site_content_regex)
    get_stream_url_regex = urllib.quote_plus(get_stream_url_regex)
    get_nav_data_regex = urllib.quote_plus(get_nav_data_regex)
    addDirectoryItem(plugin.handle, plugin.url_for(getsitecontent,url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex), ListItem("movierulz-Tamil"), True)
    url = movierulzurl+"/bollywood-movie-free/"
    addDirectoryItem(plugin.handle, plugin.url_for(getsitecontent,url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex), ListItem("movierulz-Hindi"), True)
    url = movierulzurl+"/category/telugu-movies-2020/"
    addDirectoryItem(plugin.handle, plugin.url_for(getsitecontent,url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex), ListItem("movierulz-Telugu"), True)
    url = "https://www.tubetamil.com"
    get_site_content_regex='<div class="thumb">\s+<a\shref=\"(?P<pageurl>.*?)\"\s+title=\"(?P<title>.*?)\">\s+<img\ssrc=\"(?P<poster>.*?)\"'
    get_nav_data_regex = '<li class="next"><a\shref=\"(?P<navlink>.*?)\"'
    get_stream_url_regex = '<iframe\swidth=\"(.*?)\"\s+height=\"(.*?)\"\s+src=\"(?P<streamurl>.*?)\?'
    get_site_content_regex = urllib.quote_plus(get_site_content_regex)
    get_stream_url_regex = urllib.quote_plus(get_stream_url_regex)
    get_nav_data_regex = urllib.quote_plus(get_nav_data_regex)
    addDirectoryItem(plugin.handle, plugin.url_for(getsitecontent,url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex), ListItem("Tubetamil"), True)
    url= "http://tamilgun.com"
    r = requests.get(url,verify=False) 
    url = r.url
    tamilgunurl = url.replace('/tamil/','')
    url = tamilgunurl +'/categories/new-movies-a/'
    get_site_content_regex = '<img src=\" (?P<poster>.*?) \" alt=\"(?P<title>.*?)\" \/>\s+<div class=\"rocky-effect\">\s+<a href=\"(?P<pageurl>.*?)\"\s>'
    get_nav_data_regex = '<a class="next page-numbers" href="(?P<navlink>.*?)">'
    get_stream_url_regex = '<(iframe|IFRAME)\s(src|SRC)=\"(?P<streamurl>.*?)\"|onclick=\"window\.open\(\'(?P<streamurl1>.*?)\'|sources:\s+\[{\"file\":\"(?P<streamurl2>.*?)\"}\]'
    get_site_content_regex = urllib.quote_plus(get_site_content_regex)
    get_stream_url_regex = urllib.quote_plus(get_stream_url_regex)
    get_nav_data_regex = urllib.quote_plus(get_nav_data_regex)
    addDirectoryItem(plugin.handle, plugin.url_for(getsitecontent,url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex), ListItem("Tamilgun-NewMovies"), True)
    url = tamilgunurl +'/categories/hd-movies/'
    get_site_content_regex = '<img src=\" (?P<poster>.*?) \" alt=\"(?P<title>.*?)\" \/>\s+<div class=\"rocky-effect\">\s+<a href=\"(?P<pageurl>.*?)\"\s>'
    get_nav_data_regex = '<a class="next page-numbers" href="(?P<navlink>.*?)">'
    get_stream_url_regex = '<(iframe|IFRAME)\s(src|SRC)=\"(?P<streamurl>.*?)\"|onclick=\"window\.open\(\'(?P<streamurl1>.*?)\'|sources:\s+\[{\"file\":\"(?P<streamurl2>.*?)\"}\]'
    get_site_content_regex = urllib.quote_plus(get_site_content_regex)
    get_stream_url_regex = urllib.quote_plus(get_stream_url_regex)
    get_nav_data_regex = urllib.quote_plus(get_nav_data_regex)
    addDirectoryItem(plugin.handle, plugin.url_for(getsitecontent,url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex), ListItem("Tamilgun-HDMovies"), True)
    endOfDirectory(plugin.handle)


@plugin.route('/getsitecontent/<path:url>/<get_site_content_regex>/<get_nav_data_regex>/<get_stream_url_regex>')
def getsitecontent(url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex):
    get_site_content_regex = urllib.unquote_plus(get_site_content_regex)
    get_nav_data_regex = urllib.unquote_plus(get_nav_data_regex)
    data = getdatacontent_dict(url,get_site_content_regex)
    nav = getdatacontent_dict(url,get_nav_data_regex)
    for item in data:
        addDirectoryItem(plugin.handle,plugin.url_for(liststreamurl,item['pageurl'],get_stream_url_regex), ListItem(item['title'],item['poster'],item['poster']),True)
    if nav:
        get_site_content_regex = urllib.quote_plus(get_site_content_regex)
        get_nav_data_regex = urllib.quote_plus(get_nav_data_regex)
        nav = nav[0]
        if nav['navlink']:
            nav = nav['navlink']
            addDirectoryItem(plugin.handle,plugin.url_for(getsitecontent,nav,get_site_content_regex,get_nav_data_regex,get_stream_url_regex),ListItem("[B]Next Page...[/B]"),True)
    endOfDirectory(plugin.handle)

@plugin.route('/liststreamurl/<path:url>/<get_stream_url_regex>')
def liststreamurl(url,get_stream_url_regex):
    get_stream_url_regex = urllib.unquote_plus(get_stream_url_regex)
    data = getdatacontent_dict(url,get_stream_url_regex)
    xbmc.log(str(data))
    blacklists = ['goblogportal']
    for item in data:
        xbmc.log(str(item))
        for key, value in item.items():

            if 'streamurl'in key:
                if value:
                    for blacklist in blacklists:
                        if blacklist in value:
                            pass
                        else:
                            streamurl = urllib.quote_plus(value)
                            title = value.split('/')
                            title = title[2]+'-Link'
                            addDirectoryItem(plugin.handle,plugin.url_for(resolvelink,streamurl), ListItem(title),True)
    endOfDirectory(plugin.handle)

@plugin.route('/resolvelink/<url>')
def resolvelink(url):
    url = urllib.unquote_plus(url)
    play_item = ListItem('click to play the link')
    play_item.setInfo( type="Video", infoLabels=None)
    play_item.setProperty('IsPlayable', 'true')
    if 'youtube' in url:
        url = url.split('/')
        youtube_video_id = url[-1]
        url = 'plugin://plugin.video.youtube/play/?video_id='+youtube_video_id
        addDirectoryItem(plugin.handle,url=url,listitem=play_item,isFolder=False)
    elif 'etcscrs' in url:
        data = getdatacontent_dict(url,'<iframe\swidth=\"(.*?)\"\sheight=\"(.*?)\"\s+src=\"(?P<mixdroplink>.*?)\"')
        for item in data:
            if item['mixdroplink']:
                if 'mixdrop' in item['mixdroplink']:
                    url = 'https:'+item['mixdroplink']
                    try:
                        movieurl = urlresolver.HostedMediaFile(url)
                        movieurl = movieurl.resolve()
                        addDirectoryItem(plugin.handle,url=movieurl,listitem=play_item,isFolder=False)
                    except:
                        Dialog().ok('XBMC', 'Unable to locate video')
    elif 'chrome.video' in url:
        movieurl = resolve_chromevideo(url)
        try:
            addDirectoryItem(plugin.handle,url=movieurl,listitem=play_item,isFolder=False)
        except:
            Dialog().ok('XBMC', 'Unable to locate video')
    elif "embed1.tamildbox" in url:
        movieurl = embedtamilgun.resolve_embedtamilgun(url)
        try:
            if movieurl:
                addDirectoryItem(plugin.handle,url=movieurl,listitem=play_item,isFolder=False)
            else:
                Dialog().ok('XBMC', 'Unable to locate video')
        except:
            Dialog().ok('XBMC', 'Unable to locate video')
    elif 'vidorg' in url:
        movieurl = vidorgnet.resolve_vidorgnet(url)
        try:
            addDirectoryItem(plugin.handle,url=movieurl,listitem=play_item,isFolder=False)
        except:
            Dialog().ok('XBMC', 'Unable to locate video')

    else:
        try:
            movieurl = urlresolver.HostedMediaFile(url)
            movieurl = movieurl.resolve()
            addDirectoryItem(plugin.handle,url=movieurl,listitem=play_item,isFolder=False)
        except:
            Dialog().ok('XBMC', 'Unable to locate video')
    endOfDirectory(plugin.handle)


if __name__ == '__main__':
    plugin.run()