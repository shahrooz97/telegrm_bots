from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
import random




proxies = [] # Will contain proxies [ip, port]

# proxies from sslproxy site
def proxies_():
    ua = UserAgent() # From here we generate a random user agent
    active_proxies = []
    # Retrieve latest proxies
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')
    
    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
            })

    for n in range(40):
        req = Request('http://icanhazip.com')
        req.set_proxy(proxies[n]['ip']+ ':' +proxies[n]['port'], 'http')
        try:
          my_ip = urlopen(req).read().decode('utf8')
          #print('Proxy ' + proxies[n]['ip'] + ':' + proxies[n]['port'] + ' deleted.')
          active_proxies.append(str(
              proxies[n]['ip'])+":"+str(proxies[n]['port'])
)

        except:
          pass
          #active_proxies.append(str(proxies[n]['ip']+':'+str(proxies[n]['port'])+' connection Error'))
    return active_proxies 


def get_proxies_f():
    url = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = []
    match = soup.find('tbody')
    for item in match.contents:
        result.append('{}:{}\ncountry: {}\nanonymity: {}\nhttps: {}'.format(item.contents[0].text, item.contents[1].text, item.contents[3].text, item.contents[4].text, item.contents[6].text))

    return result[:40]




#
#    url_for_test = 'https://httpbin.org/ip'
#    for i in range(1,11):
#        proxy = next(proxy_pool)
#        try:
#            resp = requests.get(url_for_test, proxies={'http':proxy, 'https':proxy})
#            if resp.json().status_code==200:
#                result.append(proxy)
#        except:
#            pass
#    return result



#if __name__=='__main__':
#    proxies_()

#print(proxies) 
