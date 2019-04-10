import requests,re
from lxml import etree
from pyquery import PyQuery as pq
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
def crawl_goubanjia():
        start_url = 'http://www.goubanjia.com/'
        result = requests.get(start_url,headers=headers)
        print(result.status_code)
        if result:
            doc = pq(result.text)
            items = doc("td.ip").items()
            for item in items:
                item.find('p').remove()
                print(re.sub('\n','', item.text()),'\n')
                print(item.text().replace('\n',''))
# crawl_goubanjia()
# text = '<td class="ip"><p style="display: none;">7</p><span>7</span><p style="display: none;">8</p><span>8</span><span style="display:inline-block;"/><span style="display:inline-block;">.2</span><p style="display: none;">6.</p><span>6.</span><span style="display:inline-block;">1</span><div style="display:inline-block;">6</div><p style="display: none;">5.</p><span>5.</span><span style="display:inline-block;">5</span><div style="display:inline-block;">4</div>:<span class="port ECGCEI">8260</span></td>&#13;'
# text1 = re.sub('<.*?style="display: none;".*?>','',text)
# doc = pq(text1)
# item = doc.text()
# item1 = re.sub('\n','',item)
# print(item1)
a, b = 2, 2