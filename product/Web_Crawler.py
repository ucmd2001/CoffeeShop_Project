
import urllib.request as req
import bs4

# url ="https://www.ptt.cc/bbs/movie/index.html"
#建立一個Request物件,附加 Request.headers 的資訊
def crawler(url="https://www.ptt.cc/bbs/movie/index.html"):
    request = req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }) #Header代表一般使用者的使用環境
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8") 

    #解析原始碼,取得每篇文章的標題
    root = bs4.BeautifulSoup(data, "html.parser")
    titles=root.find_all("div",class_="title") #尋找class = "title"的div標籤
    array =[]
    for title in titles:
        if title.a != None: #如果有標題含有a 標籤(沒有被刪除)
            element =title.a.string
            array.append(element)       
    # for result_str in array:
    #     result_str = "".join(array)
    # # print(result_str)
    return array
    # return result_str
    