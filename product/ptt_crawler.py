import urllib.request as req
import bs4

def ptt_crawler(url="https://www.ptt.cc/bbs/Gossiping/index.html"): #函式化,包裝起來
    #建立一個Request物件,附加 Request.headers 的資訊
    request = req.Request(url,headers={
        "cookie":"over18=1", #over18 = 1,不會再次詢問
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    #解析原始碼,取得每篇文章的標題
    root = bs4.BeautifulSoup(data, "html.parser")
    titles=root.find_all("div",class_="title")#尋找class = "title"的div標籤
    array=[]
    for title in titles:
        if title.a != None: #如果有標題含有a 標籤(沒有被刪除)
            element = title.a.string
            array.append(element)
            
    return array

    # #抓上一頁的連結
    # nextLink = root.find("a",string="‹ 上頁")
    # return nextLink["href"] #丟回函式外

# #主程序:抓取多個頁面的標題
# pageURL ="https://www.ptt.cc/bbs/Gossiping/index.html"
# count = 0 #設定要抓幾頁
# while count<5: #當count<5,繼續抓下一頁
#     pageURL ="https://www.ptt.cc"+getData(pageURL) 
#     #pageURL ="/bbs/Gossiping/index39381.html"補前面的https網址給他
#     count+=1
# print(pageURL)
