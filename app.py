
#解決DNS連線問題
# import dns.resolver
# dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
# dns.resolver.default_resolver.nameservers=['8.8.8.8']
# 以防有人大量濫用爬蟲，import time
from ssl import _create_default_https_context
import time
# #引用JWT金鑰
# import jwt
# import time

#連線mongoDB
import pymongo
# client = pymongo.MongoClient("mongodb+srv://gigi:gigi@cluster0.4sn8p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.member_info

#連線member_info 資料庫
#確認是否正常連線資料庫
print("資料庫連線建立成功")

#初始化 Flask 伺服器、設定登入逾時時間
from datetime import timedelta 
from flask import *
app=Flask(__name__,static_folder="static",static_url_path="/")
app.secret_key="any string but secret"
app.config["PERMANENT_SESSION_LIFETIME"]= timedelta(minutes=30)
#session_lifetime 30分鐘自動登出

#處理路由
#首頁
@app.route("/")
def index():
    return render_template("index.html")

#會員系統頁
@app.route("/member_system")
def member():
    # 假如他沒登入，導向會員系統頁，已經登入情況下會導向會員資料頁面
    if "id" in session:
        personal_email = session["email"]
        personal_nickname = session["nickname"]
        cups = session["cups"]
        return render_template("personal_info.html",p_email=personal_email,p_nickname=personal_nickname,p_cups = cups)
    else:
        return render_template("member_system.html")

#註冊頁
@app.route("/signup",methods=["POST"])
def signup():
    #從前端接收資料 暱稱,emailm,密碼,確認密碼
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    password_confrim = request.form["password_confrim"]
    #連結資料庫，處理資料，和資料庫user集合互動 
    collection = db.user
    #檢查users集合是否有相同Email的文件資料
    result=collection.find_one({
        "email":email
    })
    if result != None:
        return redirect("/error?msg=信箱已被註冊")
    #把資料放進資料庫，完成註冊
    collection.insert_one({
        "email":email,
        "nickname":nickname,
        "password":password,
        "password_confrim":password_confrim
    })
    return redirect("/member_system") #導回會員頁

#登入頁面
@app.route("/signin",methods=["POST"])
def signin():
    email = request.form["email"]
    password = request.form["password"]
#和資料庫 user集合互動
    collection = db.user
#檢查信箱密碼是否正確:搜尋user集合是否有符合條件之資料
#用{$and:[]} 搜尋
    result = collection.find_one({
    "$and":[
        {"email":email},
        {"password":password}
        ]
    })
    #找不到對應資料，導向至錯誤畫面
    if result == None:
        return redirect("/error?msg=帳號或密碼輸入錯誤，請重新輸入")
    #登入成功，在session紀錄會員資訊，導向會員畫面
    session["nickname"]=result["nickname"]
    session["email"]=result["email"]
    session["id"]=str(result["_id"])
    session["password"]=result["password"]
    session["cups"] = result["cups"]
    return redirect("/personal_info")

#登出畫面
@app.route("/signout")
def signout():
    del session["id"]
    return redirect("/")

#個人資料頁
@app.route("/personal_info")
def personal_info(): 
    # 假設他沒有登入，id沒在session內部，引導至會員系統頁面
    if "id" in session:
        email = session["email"]
        collection = db.user
        result = collection.find_one({"email":email})
        personal_email = result["email"]
        personal_nickname = result["nickname"]
        session["cups"] = result["cups"]
        return render_template("personal_info.html",p_email=personal_email,p_nickname=personal_nickname,p_cups=session["cups"])

#更新密碼頁
@app.route("/pwchange")
def pwchange():
    return render_template("pwchange.html")

#儲值20杯
@app.route("/cupspuls20",methods=["GET"])
def cupspuls20():
    cups = session["cups"]
    collection = db.user
    result = collection.find_one({"cups":cups})
    if result != None:
        collection.update_one({"cups":cups},{'$inc': {'cups': 20}})
    return redirect("/personal_info")

#兌換一杯
@app.route("/cupsminusone")
def cupsminusone():
    cups = session["cups"]
    collection = db.user
    result = collection.find_one({"cups":cups})
    if result != None:
        collection.update_one({"cups":cups},{'$inc': {'cups': -1}})

    return redirect("/personal_info")

#更新密碼成功頁
@app.route("/pwchanged",methods=["POST"])
def pwchanged():
    #從前端接收資料
    password = request.form["password"]
    password_new = request.form["password_new"]
    email=session["email"]
    #連結資料庫，處理資料，和資料庫user集合互動 
    collection = db.user
    #檢查users集合是否有相同password的文件資料
    result=collection.find_one({
        "password":password
    })
    #假如密碼不正確，回傳密碼不正確error
    if result == None:
        return redirect("/error?msg=密碼不正確，請重新輸入")
    elif result == password:
        return redirect("/error?msg=密碼和之前相同，請重新輸入")
    else :
    #把資料放進資料庫，完成更新
        collection.update_one({
            "email":email
        },{"$set":{"password":password_new}
        })

    return redirect("/member_system") #回會員首頁

#錯誤頁
#/error?msg=錯誤訊息
@app.route("/error")
def error():
    messsage= request.args.get("msg","發生錯誤請聯繫客服")

    return render_template("error.html",message=messsage)

# 處理404錯誤
@app.errorhandler(404)
def not_found_error(error):
    message=request.args.get("msg","發生錯誤請重新輸入")
    return render_template('error.html',message=message), 404

# 處理500錯誤
@app.errorhandler(500)
def internal_error(error):
    message=request.args.get("msg","發生錯誤請重新輸入")
    return render_template('error.html',message=message), 500

if __name__ == "__main__":
    app.run(debug=True)
