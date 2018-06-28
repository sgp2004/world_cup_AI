# coding=utf-8
import urllib.parse
import sys
import urllib.request
import gzip
from bs4 import BeautifulSoup

# params  CategoryId=808 CategoryType=SiteHome ItemListActionName=PostList PageIndex=3 ParentCategoryId=0 TotalPostCount=4000
def getHtml(url,values):
    user_agent='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    headers = {'User-Agent':user_agent}
    data = urllib.parse.urlencode(values)
    print(url+'?'+data)
    response_result = urllib.request.urlopen(url+'?'+data).read()
    print(type(response_result))
    #压缩过的数据，一般不需要unzip 视具体网页决定
    html = gzip.decompress(response_result)
    html = html.decode('gbk')
    #html = response_result.decode('utf-8')
    return html
#return ""

#获取数据
def requestOdds(index):
    print('请求数据')
    url = 'http://odds.500.com/index_jczq_2018-06-'+index+".shtml#!league=%5B352%2C452%5D"
    value= {
            }
    result = getHtml(url,value)
    return result
def has_class_but_no_id(tag):
    return tag.has_attr('tr') and not tag.has_attr('id')


'''
一场比赛的基本信息：比赛id，比赛类型，哪一轮，时间，主客场，胜平负赔率，返还率，主赢信心指数
'''
class Game:
    def __str__(self):
        # return '%s,%s,%s,%s,%s,%s,%s,%s,%s' %(self.race,self.turn,self.time,self.host,self.guest,self.rate_w,self.rate_tie,self.rate_lose,self.rate_back)
        return '%s VS %s,%s,%s,%s' %(self.host,self.guest,self.rate_w,self.rate_tie,self.rate_lose)

'''
球队的基本信息：
球队名、足联排名、杯赛排名、近期战绩（胜率）、进球、失球、
'''
class Team:
    pass

'''
投注信息： 比赛id，主胜概率、平局概率、负概率、主胜成交量、平局成交量、负成交量、主胜庄家盈利、平局庄家盈利、主负庄家盈利
'''
class Trade:
    pass

'''
百家欧赔 即时赔率（胜平负）即时概率（胜平负）返还率
'''
class Odds:
    pass


if __name__ == '__main__':
    print("start parse")
    text = requestOdds(sys.argv[1])
    soup = BeautifulSoup(text, 'html.parser')
    items = soup.find_all('tr', attrs={'': ''}, limit=1000)
    for item in items:
        #print(item)
        tds = item.find_all('td')
        games = []
        if len(tds)>=15 and tds[1].string=='世界杯':
            game = Game()
            game.race = tds[1].string
            game.turn = tds[2].string
            game.time = tds[3].string
            game.host = tds[4].string
            game.guest = tds[6].string
            game.rate_w = tds[11].string
            game.rate_tie = tds[12].string
            game.rate_lose = tds[13].string
            game.rate_back= tds[14].string
            games.append(game)
        if len(games)>0:
            i = 1
            for game in games:
                print(game,",6."+sys.argv[1]+"."+str(i))
                i=i+1


