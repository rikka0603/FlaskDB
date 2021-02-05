# Rikka
# Time:2020

from bs4 import BeautifulSoup        #网页解析
import re                            #正则表达式，进行文字匹配
import urllib.request,urllib.error   #制定URL,获取网页数据
import xlwt                          #进行excel操作
import sqlite3                       #进行SQLITE数据库操作



def main():

    baseurl = "https://movie.douban.com/top250?start="

    #1.爬取网页

    datalist = getData(baseurl)

    #savepath = ".\\豆瓣电影Top250.xls"
    # saveData(datalist,savepath)
    dbpath = "movie.db"
    saveData2(datalist,dbpath)
    #2.解析数据
    #3.保存数据


#影片详情规则
findLink = re.compile(r'<a href="(.*?)">')  #创建正则表达式对象，表示规则

findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)   #re.S 让换行符包含在字符中

findTitle = re.compile(r'<span class="title">(.*?)</span>')

findAverage = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')

findPeople = re.compile(r'<span>(\d*)人评价</span>')

fidInq = re.compile(r'<span class="inq">(.*?)</span>')

findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


#爬取网页
def getData(baseurl):

    datalist = []
    for i in range(0,10):    #调用获取页面信息函数10次
        url = baseurl+str(i*25)
        html = askURL(url)        #保存获取的网页源码
        #逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            #print(item)  #测试:一部电影的item信息
            data = []   #保存一部电影的所有信息
            item = str(item)
            #获取影片详情链接
            link = re.findall(findLink,item)[0]   #re库用来通过正则表达式查找指定字符串
            data.append(link)

            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)

            titles = re.findall(findTitle,item)
            if(len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')   #留空

            rating = re.findall(findAverage,item)[0]
            data.append(rating)

            num = re.findall(findPeople,item)[0]
            data.append(num)

            inq = re.findall(fidInq,item)
            if len(inq)!= 0:
                inq = inq[0].replace("0","")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd,item)[0]
            bd = re.sub('...<br(\s+)?/>(\s+)?'," ",bd)   #去掉换行
            data.append(bd.strip())   #去掉前后的空哥

            datalist.append(data)   #把处理的电影信息放在datalist
    #print(datalist)
    return datalist

#得到指定一个URL的网页内容
def askURL(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }     #用户代理，告诉豆瓣服务器，告诉我们是什么类型的机器、浏览器
    request = urllib.request.Request(url,headers=head)   #发送请求
    html = ""
    try:
        response = urllib.request.urlopen(request)  #获取响应
        html = response.read().decode("utf-8") #获取网页内容
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def saveData(datalist,savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('豆瓣电影top250')  # 创建工作表1
    col = ("电影详情链接","图片链接","影片中文名","影片外文名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])  #列名
    for i in range(0,250):
        print("第%d条"%i)
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save('db2503.xls')


def saveData2(datalist,dbpath):

    init_db(dbpath)

    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
                insert into movie250(
                info_link,pic_link,cname,ename,score,rated,instruction,info)
                values (%s)'''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()



def init_db(dbpath):
    #创建数据表
    sql ='''
        create table movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instruction text,
        info text
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
    init_db("movietest.db")
    print("爬取完毕！")