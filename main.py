#https://github.com/tamland/kodi-plugin-routing
import routing
from xbmcgui import ListItem, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl
import urllib2,urllib,re,requests
import resolveurl as urlresolver

def getdatacontent(url,reg):
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    req = urllib2.Request(url)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    r = opener.open(req)
    html = r.read()
    r = re.compile(reg)
    data = [m.groupdict() for m in r.finditer(html)]
    return data
def getnavcontent(url,reg):
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
    url = "https://6movierulz.com/category/tamil-movie/"
    get_site_content_regex ='<a href=\"(?P<pageurl>.*?)\"\stitle=\"(?P<title>.*?)\">\s*<img width=\"\d+\" height=\"\d+\" src=\"(?P<poster>.*?)\"'
    get_stream_url_regex = '<p><strong>(?P<streamtitle>.*?)<\/strong><br \/>\s+<a href=\"(?P<streamurl>.*?)\"'
    get_nav_data_regex = '<a href=\"(?P<navlink>.*?)\">&larr;(\s|)Older Entries'
    get_site_content_regex = urllib.quote_plus(get_site_content_regex)
    get_stream_url_regex = urllib.quote_plus(get_stream_url_regex)
    get_nav_data_regex = urllib.quote_plus(get_nav_data_regex)
    addDirectoryItem(plugin.handle, plugin.url_for(getsitecontent,url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex), ListItem("movierulz"), True)
    endOfDirectory(plugin.handle)


@plugin.route('/getsitecontent/<path:url>/<get_site_content_regex>/<get_nav_data_regex>/<get_stream_url_regex>')
def getsitecontent(url,get_site_content_regex,get_nav_data_regex,get_stream_url_regex):
    get_site_content_regex = urllib.unquote_plus(get_site_content_regex)
    get_nav_data_regex = urllib.unquote_plus(get_nav_data_regex)
    data = getdatacontent(url,get_site_content_regex)
    nav = getdatacontent(url,get_nav_data_regex)
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
    data = getdatacontent(url,get_stream_url_regex)
    for item in data:
        addDirectoryItem(plugin.handle,plugin.url_for(resolvelink,item['streamurl']), ListItem(item['streamtitle']),True)
    endOfDirectory(plugin.handle)

@plugin.route('/resolvelink/<path:url>')
def resolvelink(url):
    try:
        movieurl = urlresolver.HostedMediaFile(url)
        movieurl = movieurl.resolve()
        play_item = ListItem('click to play the link')
        play_item.setInfo( type="Video", infoLabels=None)
        play_item.setProperty('IsPlayable', 'true')
        addDirectoryItem(plugin.handle,url=movieurl,listitem=play_item,isFolder=False)
    except:
        Dialog().ok('XBMC', 'Unable to locate video')
    endOfDirectory(plugin.handle)


if __name__ == '__main__':
    plugin.run()