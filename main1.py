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

plugin = routing.Plugin()
@plugin.route('/')
def index():
    # addDirectoryItem(plugin.handle, plugin.url_for(show_category,"https://6movierulz.com/category/tamil-movie/"), ListItem("Category One"), True)
    # addDirectoryItem(plugin.handle, plugin.url_for(show_category, "two"), ListItem("Category Two"), True)
    get_site_content_regex =r'<a href=\"(?P<pageurl>.*?)\"\stitle=\"(?P<title>.*?)\">\s*<img width=\"\d+\" height=\"\d+\" src=\"(?P<poster>.*?)\"'
    get_site_content_regex = get_site_content_regex.replace('?','questionmark')
    #get_site_content_regex = get_site_content_regex.replace('\\','backslash')
    url = "https://6movierulz.com/category/tamil-movie/"+'get_site_content_regex'+get_site_content_regex
    addDirectoryItem(plugin.handle, plugin.url_for(getsitecontent,url), ListItem("movierulz"), True)
    # addDirectoryItem(plugin.handle, plugin.url_for(show_directory, "/dir/two"), ListItem("Directory Two"), True)
    endOfDirectory(plugin.handle)

@plugin.route('/category/<category_id>')
def show_category(category_id):
    addDirectoryItem(plugin.handle, "", ListItem("Hello category"+category_id))
    endOfDirectory(plugin.handle)

@plugin.route('/movierulz/<path:url>')
def getsitecontent(url):
    xbmc.log('-------------------------------------------------------entering-get-site-content url-------------------------')
    mainurl,regex = url.split('get_site_content_regex')
    xbmc.log(mainurl)
    regex = regex.replace('questionmark','?')
    regex = regex.replace('/','\\')
    regex = regex[1:]
    xbmc.log(regex)
    #get_site_content_regex = '<a href=\"(?P<pageurl>.*?)\"\stitle=\"(?P<title>.*?)\">\s*<img width=\"\d+\" height=\"\d+\" src=\"(?P<poster>.*?)\"'
    data = getdatacontent(mainurl,regex)
    for item in data:
        #addDirectoryItem(plugin.handle,"", ListItem(item['title'],item['poster'],item['poster']))
        addDirectoryItem(plugin.handle,plugin.url_for(liststreamurl,item['pageurl']), ListItem(item['title'],item['poster'],item['poster']),True)
    endOfDirectory(plugin.handle)

@plugin.route('/liststreamurl/<path:url>')
def liststreamurl(url):
    xbmc.log('-------------------------------------------------------entering-list-stream-url-------------------------')
    xbmc.log(url)
    get_stream_url_regex = '<p><strong>(?P<streamtitle>.*?)<\/strong><br \/>\s+<a href=\"(?P<streamurl>.*?)\"'
    data = getdatacontent(url,get_stream_url_regex)
    for item in data:
        addDirectoryItem(plugin.handle,plugin.url_for(resolvelink,item['streamurl']), ListItem(item['streamtitle']),True)
    endOfDirectory(plugin.handle)

@plugin.route('/resolvelink/<path:url>')
def resolvelink(url):
    xbmc.log('-------------------------------------------------------entering-resolve-link-------------------------')
    xbmc.log(url)
    try:
        movieurl = urlresolver.HostedMediaFile(url)
        movieurl = movieurl.resolve()
        xbmc.log('-------------------------------------------------------movie url link-------------------------')
        #addDirectoryItem(plugin.handle,movieurl, ListItem('click to play the link'))
        xbmc.log(movieurl)
        # movieurl = movieurl.split('|')
        # movieurl = movieurl[0]
        # xbmc.log(movieurl)
        play_item = ListItem('click to play the link')
        play_item.setInfo( type="Video", infoLabels=None)
        play_item.setProperty('IsPlayable', 'true')
        #addDir('','',movieurl,"Click to play the link","","")
        addDirectoryItem(plugin.handle,url=movieurl,listitem=play_item,isFolder=False)
        #setResolvedUrl(int(sys.argv[1]),True,xbmcgui.ListItem(path=movieurl))
        #addDirectoryItem(plugin.handle,plugin.url_for(playvideo,movieurl), ListItem('click link'))
            #addDirectoryItem(plugin.handle,url=movieurl,ListItem=play_item,False)
    except:
        Dialog().ok('XBMC', 'Unable to locate video')
    endOfDirectory(plugin.handle)


if __name__ == '__main__':
    plugin.run()