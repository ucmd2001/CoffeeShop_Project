import urllib.request as req
import bs4

#建立一個Request物件,附加 Request.headers 的資訊
def stock_crawler(url="https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZG_AB.djhtm"):
    request = req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }) #Header代表一般使用者的使用環境
    with req.urlopen(request) as response:
        data=response.read().decode("Big5")
    # 解析原始碼,取得每篇文章的標題
    root = bs4.BeautifulSoup(data, "html.parser")
    titles=root.find_all("td",class_="t3t1") #尋找class = "t3t1"的td標籤
    array = []
    for title in titles:
        if title.a != None:
            element =title.a.string
            array.append(element)
    return array

