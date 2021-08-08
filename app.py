from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    SourceUser,
)

# crawler
# from cambridgeDictionary import (main, checkInput)
import main
import checkInput
import json

app = Flask(__name__)

line_bot_api = LineBotApi(
    ''
)
handler = WebhookHandler('')


@app.route("/")
def home():
    testStr = ""

    return testStr + ' home OK'


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return 'OK'


# 處理訊息


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    '''
    是數字整數
        正整數
        負整數
            
    是小數 或 字串
        是小數
        是字串
            是中文
            是單字
                是功能
                不是功能
            是句子

    '''

    try:
        #輸入為數字整數
        textNum = int(text)
        print("Input is an integer number. Number = ", textNum)
        if textNum <= 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Number should be greater than 0!"))
        else:
            try:  #搜尋example
                try:
                    #搜尋字典頁面
                    pageURL = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/"
                    with open("dataBase.json", mode="r") as file:
                        data = json.load(file)
                        url = data["url"]
                        pageURL += url
                    main.getData(pageURL)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text="Your input: " + event.message.text + "\n\n" +
                            "Result(example): \n" + main.getExample(textNum)))
                except:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="Error! url is null."))
            except:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text=
                        "Error! Can't Find The Example With Assigned Number."))
    except:
        #輸入不是數字整數
        try:
            #輸入是小數
            val = float(user_input)
            print("Input is a float number, not an integer number.\n Number =",
                  val)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=
                    "Input is a float number, not an integer number.\n Number = "
                    + user_input))
        except:
            #輸入是字串
            if checkInput.IsChinese(text) == True:  #是中文
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="This is Chinese, not English."))
            #檢查是單字還是句子
            elif checkInput.IsSentence(text) == False:  #是單字
                if checkInput.IsFunction(text):  #是功能
                    funcName = checkInput.GetFunctionName(text)
                    if funcName == 'profile':  #取得功能名稱
                        if isinstance(event.source, SourceUser):
                            profile = line_bot_api.get_profile(
                                event.source.user_id)
                            line_bot_api.reply_message(event.reply_token, [
                                TextSendMessage(text='Display name: ' +
                                                profile.display_name),
                                TextSendMessage(text='Status message: ' +
                                                str(profile.status_message))
                            ])
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(
                                    text=
                                    "Bot can't use profile API without user ID"
                                ))
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="Can't find the function."))
                else:
                    #輸入
                    # pageURL = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crisis"
                    pageURL = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/" + text
                    #url 寫入 .json檔
                    with open("dataBase.json", mode="r") as file:
                        data = json.load(file)
                        data["url"] = text
                    with open("dataBase.json", mode="w") as file:
                        json.dump(data, file)

                    main.getData(pageURL)  #搜尋字典頁面
                    isFinded = main.getIsPageFound()  #根據回傳內容判斷輸入文字是否找得到對應的字典頁面

                    if isFinded == True:
                        try:
                            #傳送搜尋結果
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(
                                    text="Your input: " + event.message.text +
                                    ", 搜尋結果: \n" + main.getTitle() +
                                    "\n單字意思: \n" + main.getDefinitionAll()))

                        except:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(
                                    text="Error! Can't Find The Definition."))
                    else:
                        #找不到單字
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(
                                text=
                                "Page not found. Please enter the correct word."
                            ))
            else:  #echo bot
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Your input: \n" +
                                    event.message.text))


if __name__ == "__main__":
    app.run()
