from bs4 import BeautifulSoup #网页解析获取数据
import re
import urllib.request,urllib.error #指定url，获取网页数据
import numpy as np
import xlwt


def main():
    baseurl="https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist=getData(baseurl)
    # 3.保存数据
    #savepath="./" #.当前文件夹 /当前位置 \\文件系统反 r表示不转义，使用真实字符
    savepath="豆瓣电影Top250.xls"
    saveData(datalist,savepath) #保存数据

    # askURL("https://movie.douban.com/top250?start=0")

findLink=re.compile(r'<a href="(.*?)">') #compile创建正则表达式对象，表示规则（字符串的模式）
findImgSrc=re.compile(r'img.*src="(.*?)"',re.S) #re.S让换行符包含在字符中
findTitle=re.compile(r'span class="title">(.*?)</span>')
findRating=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
findJudge=re.compile(r'<span>(\d*)人评价</span>')
findInQ=re.compile(r'<span class="inq">(.*?)</span>')
findBD=re.compile(r'<p class="">(.*?)</p>',re.S)

#1.爬取网页
def getData(baseurl):
    datalist=[]
    for i in range(0,10): #调用获取页面信息函数10次
        url=baseurl+str(i*25)
        html=askURL(url) #保存获取到的网页源码
        # 2.逐一解析数据
        soup=BeautifulSoup(html,"html.parser") #html解析器
        for item in soup.find_all('div',class_="item"): #查找符合要求的字符串，形成列表 下划线是为了避免与python语言的关键字class冲突
            #print(item) #查看电影item全部信息
            data=[] #保存一部电影所有信息
            item=str(item)
            # print(item)
            # break #停止

            #获取影片详情链接
            Link=re.findall(findLink,item)[0] #re库用来通过正则表达式查找指定的字符串
            data.append(Link)

            ImgSrc = re.findall(findImgSrc,item)[0]
            data.append(ImgSrc)

            Title = re.findall(findTitle,item) #片名可能有多个
            if(len(Title)==2):
                ctitle=Title[0] #添加中文名
                data.append(ctitle)
                otitle=Title[1].replace("/","") #去掉无关符号
                data.append(otitle) #添加英文名
            else:
                data.append(Title[0])
                data.append(' ') #留空

            Rating = re.findall(findRating,item)[0]
            data.append(Rating)

            Judge = re.findall(findJudge,item)[0]
            data.append(Judge)

            InQ = re.findall(findInQ,item)
            if len(InQ)!=0:
                InQ=InQ[0].replace('。','')
                data.append(InQ)
            else:
                data.append(" ")

            BD = re.findall(findBD,item)[0]
            BD=re.sub('<br(\s+)/>(\s+)',' ',BD) #去掉<br/>
            BD=re.sub('/',' ',BD)
            data.append(BD.strip()) #去掉前后空格

            datalist.append(data)

    x=np.array(datalist)
    print(x.shape)
    return datalist

#得到指定一个URL的网页内容
def askURL(url):
    head={ #模拟浏览器头部信息，向服务器发布消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 75.0.3770.100 Safari / 537.36"
    } #用户代理告诉服务器是什么类型机器浏览器（本质告诉浏览器能接受什么样的信息）
    #head['U']
    request=urllib.request.Request(url,headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request) #发出请求，返回response
        html=response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

#3.保存数据
def saveData(datalist,savepath):
    print("save...")

    book = xlwt.Workbook(encoding='utf-8',style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)
    col=('电影详情链接','图片链接','影片中文名','影片外文名','评分','评价数','概况','相关信息') #元组
    for i in range(0, 8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,250):
        print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save(savepath)

if __name__=="__main__":
    main()
    print("爬取完毕！")
