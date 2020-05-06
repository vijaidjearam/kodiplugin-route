def resolve_vidorgnet(url):
	if "vidorg.net" in url:
	                    url = url.replace('\/','/')
	                    url = url.split(',')
	                    url = url[0]+url[3]+'/index-v1-a1.m3u8'
	                    if url:
	                        return url