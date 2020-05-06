def resolve_chromevideo(url):    
    if "chromecast.video" in url:
        if "https" in url:
            url = url 
        elif "http" in url:
            url = url.replace("http","https")
        else:
            url = 'https:'+url
        
        headers = {
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ta-IN;q=0.8,ta;q=0.7,fr-FR;q=0.6,fr;q=0.5',
        }

        response = requests.get(url, headers=headers)
        html1 = response.content
        movieurl = re.compile('sources:\s+\[\"(.*?)\",\"(.*?)\"\]').findall(html1)
        movieurl = movieurl[0]
        
        if movieurl[0]:
            headers = {
                'Connection': 'keep-alive',
                'Origin': 'https://chromecast.video',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
                'DNT': '1',
                'Accept': '*/*',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Referer': url,
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,ta-IN;q=0.8,ta;q=0.7,fr-FR;q=0.6,fr;q=0.5',
            }
            response = requests.get(movieurl[0], headers=headers)
            temp = response.content
            movieurl = re.compile('https:\/\/(.*?)index-v1-a1.m3u8').findall(temp)
            if movieurl[-1]:
                movieurl = 'https://'+movieurl[-1]+'index-v1-a1.m3u8'
                return movieurl