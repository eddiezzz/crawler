from urllib2 import Request, urlopen

 
def getHtml(url):
    req = Request(url)
    req.add_header('Accept-Encoding', 'utf-8')
    req.add_header('User-agent', 'Mozilla/5.0')
    res = urlopen(req).read()
    return res

url="https://mp.weixin.qq.com/s?timestamp=1540894499&src=3&ver=1&signature=go4WJuBkXAzUUtCNQOl1HltB*UPKeKMN5rs3JlXLkGCK5qBGN8*kknbLWGUns1rs7GTfMRe17*AAE6XVkPTypiaHPbu55T1Mb1FXDA75C8RfY8WpGXpSIZNIvle-oRJB*qpDUmUI-Qu4jTbxgBcqc8m5LGelrznOnRFhqwH3AbM="
body=getHtml(url)

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(body)
for s in soup('script'):
    s.extract()
print soup.__str__()
