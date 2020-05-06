import urllib2,re,xbmc
def resolve_embedtamilgun(url):
    if "embed1.tamildbox" in url:
        #xbmc.log("---------------------------------------embed1-tamildbox-----------------------------------------------------------")
        if "https" in url:
            url = url.replace("https","http")
        elif "http" in url:
            url = url
        else:
            url = 'http:'+url
        proxy_handler = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_handler)
        req = urllib2.Request(url)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        r = opener.open(req)
        html1 = r.read()
        movieurl= re.compile("domainStream = '(.*?)'").findall(html1)
        xbmc.log("---------------------------------------embed1-tamildbox - movie-url-----------------------------------------------------------")
        xbmc.log(str(movieurl))
        if movieurl:
            for tempurl in movieurl:
                if tempurl:
                    xbmc.log("---------------------------------------embed1-tamildbox - temp-url-----------------------------------------------------------")
                    xbmc.log(tempurl)
                    return tempurl
        elif "domainStream = domainStream.replace('.tamildbox.tips', '.tamilgun.tv')" in html1:
            url = url.replace('hls_vast', 'hls')
            url = url.replace('.tamildbox.tips', '.tamilgun.tv')
            url = url + '/playlist.m3u8'
            #xbmc.log(url)
            return url
    return None