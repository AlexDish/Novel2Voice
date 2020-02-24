import requests
import bs4
import re

URL_BASE = 'https://www.biqumo.com/8_8521/'
FIRST_HTML = '4936412.html'
# FIRST_HTML = '7332922.html'
ARTICLE_ID = '8_8521'
TXT_PATH = 'Articles'

def getOnePage(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        return None

def parseAction(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    page_id, title, article_data = parseArticle(soup)
    saveTxt(page_id, title, article_data)
    next_link = parseNextLink(soup)
    if next_link:
        return URL_BASE + next_link
    else:
        return None
    pass
   
def parseArticle(soup):
    article_datas = soup.select('#content')
    if len(article_datas)>0:
        article_data, page_id = parseUselessTag(article_datas[0])
        # print(article_data)
        return page_id, soup.title.text, article_data
        # saveTxt(page_id, soup.title.text, article_data)
    return None
    pass

def parseUselessTag(article_data):
    ret = re.sub('<br/>', '\n', str(article_data))
    ret = re.sub('<div.*?>', '', ret)
    ret = re.sub('</div>', '', ret)
    ret = re.sub('<script>.*?>', '', ret)
    page_id = re.findall('(\w+)\.html', ret)[0]
    ret = re.sub('https://.*?\w.*\s+.+com', '', ret)
    return ret, page_id

def saveTxt(page_id, title, article_data):
    title = title.replace('_庆余年_穿越小说_笔趣阁', '')
    title = re.sub('[/,\\\\, :, *, ?, ", <, >, |]', '', title)
    with open('./'+TXT_PATH+'/'+page_id+'_'+title+'.txt', 'w', encoding='utf-8') as f:
        f.write(article_data)

def parseNextLink(soup):
    lis = soup.find_all('li')
    for li in lis:
        if '下一章' == li.a.text:
            link = li.a['href']
            try:
                ar_id = re.findall('/(\w*)/', link)[0]
            except Exception:
                ar_id = None
            try:
                page_id_html = re.findall('/(\w*.html)', link)[0]
            except Exception:
                page_id_html = None
            print(ar_id, ',', page_id_html)
            if ar_id == ARTICLE_ID:
                return page_id_html
            else:
                return None
    return None
    pass

def main():
    text = getOnePage(URL_BASE + FIRST_HTML)
    while True:
        if text:
            ret = parseAction(text)
        if ret:
            text = getOnePage(ret)
        else:
            break

if __name__ == '__main__':
    main()
    # input("")
    
    