#ref: [[Python教學]Request和BeautifulSoup爬蟲教學，初學者也可以馬上學會！](https://zx2515296964.medium.com/python-%E6%95%99%E5%AD%B8-%E7%B0%A1%E5%96%AE%E5%B9%BE%E6%AD%A5%E9%A9%9F-%E8%AE%93%E4%BD%A0%E8%BC%95%E9%AC%86%E7%88%AC%E8%9F%B2-928a816051c1)
#ref: [[第 16 天] 網頁解析](https://ithelp.ithome.com.tw/articles/10186119)
#ref: 暫停一下再爬: https://zx2515296964.medium.com/python-%E6%95%99%E5%AD%B8-%E7%B0%A1%E5%96%AE%E5%B9%BE%E6%AD%A5%E9%A9%9F-%E8%AE%93%E4%BD%A0%E8%BC%95%E9%AC%86%E7%88%AC%E8%9F%B2-928a816051c1

# TODO: python list index -1 why exampleList[-1][count][0] can run???

import urllib.request as req
import re
import bs4
import numpy as np

#variable
definitionList = []  # 建立一個空的 list 來放定義
exampleList = []  # 建立一個空的 list 來放範例
titleStr = ""  #標題字串
isPageFound = False  # 有找到單字頁面

# data (to restore url)
import json


def getData(url):
    # reset variable
    itemNum = 0
    global definitionList  # = [[]]  # 建立一個空的 list 來放定義
    global exampleList  # = [[]]  # 建立一個空的 list 來放範例
    global titleStr  # = ""
    global isPageFound

    definitionList = []  # 建立一個空的 list 來放定義
    exampleList = []  # 建立一個空的 list 來放定義
    titleStr = ""
    isPageFound = False

    request = req.Request(
        url,
        headers={
            "cookie":
            "over18=1",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
        })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "html.parser")

    # title
    titles = root.find_all("div", class_="di-title")
    for title in titles:
        try:
            titleStr = title.span.string
        except:
            titleStr = "None"

    # block
    blocks = root.find_all("div", class_="def-block")
    if len(blocks) > 0:
        for block in blocks:

            print("------------------------------------------------------")

            # definition
            try:
                definitionEN = block.find("div", class_="ddef_h").find(
                    "div", class_="ddef_d").text

                definitionENStr = ""
                try:
                    definitionENStr = definitionEN
                except:
                    definitionENStr = "None"
                # print("EN(def): ", definitionENStr)
                definitionCH = block.find("div", class_="ddef_b")
                definitionCHStr = ""
                try:
                    definitionCHStr = definitionCH.span.string
                except:
                    definitionCHStr = "None"

                # print("CH(def): " + definitionCHStr)
            except:
                definitionENStr = "None (in example exception)"
                definitionCHStr = "None (in example exception)"

            new_row = [[definitionENStr, definitionCHStr]]  # row:0; column:1
            if len(definitionList) == 0:
                definitionList = new_row
            else:
                definitionList = np.append(definitionList, new_row, axis=0)

            # example
            examples = block.find_all("div", class_="examp")

            itemNum = 0
            currentList = []
            for example in examples:
                try:
                    exampleEN = example.find("span", class_="eg")

                    exampleENStr = ""
                    try:
                        exampleENStr = exampleEN.text
                    except:
                        exampleENStr = "None"
                    print("EN(examp): " + exampleENStr)

                    exampleCH = example.find("span", class_="trans")
                    exampleCHStr = ""
                    try:
                        exampleCHStr = exampleCH.text
                    except:
                        exampleCHStr = "None"
                    print("CH(examp): " + exampleCHStr)
                except:
                    exampleENStr = "None (in example exception)"
                    exampleCHStr = "None (in example exception)"

                new_row = [[exampleENStr, exampleCHStr]]  # row:0; column:1
                # print("currentList first in= (" + new_row[0][0])

                if len(currentList) == 0:
                    currentList = new_row
                else:
                    currentList = np.append(currentList, new_row, axis=0)

                # print("currentList = (" + currentList[0][0] + ", " +
                #       currentList[0][1] + ")")
                print("currentList = (" + str(len(currentList)) + ", " +
                      str(len(currentList[0])) + ")")

                itemNum += 1
            try:
                exampleList.append(currentList)
                print("exampleList 加一, len= " + str(len(exampleList)))
            except:
                exampleList = currentList
            print("exampleList = " + str(len(exampleList)))
        isPageFound = True
    else:
        print("back to homepage")
        isPageFound = False


# nextLink = root.find("a", string="‹ 上頁")
#return nextLink["href"]
def getTitle():
    return "The word is: " + titleStr


def getIsPageFound():
    return isPageFound


def getDefinitionAll():
    # EN: 0, CH: 1
    count = 0
    EN = 0
    CH = 1

    print("len(definitionList): " + str(len(definitionList)))
    defStr = ""
    for definition in definitionList:
        defStr += ("[" + str(count + 1) + "]" + "\n" +
                   definitionList[count][EN] + "\n" +
                   definitionList[count][CH] + "\n")
        count += 1
    return defStr


def getDefinitionOne(count, inputNum):
    defStr = ""
    EN = 0
    CH = 1
    # EN: 0, CH: 1
    if len(definitionList) == 0:
        defStr = "definitionList is null"
    else:
        defStr = (definitionList[count][EN] + "\n" +
                  definitionList[count][CH] + "\n")
    return defStr


def getExample(inputNum):
    global exampleList
    # EN: 0, CH: 1
    outputStr = ""
    exampStr = ""
    count = 0
    EN = 0
    CH = 1
    num = (inputNum - 1 + len(exampleList)) % len(exampleList)
    print("exp(num) = " + str(len(exampleList)))
    outputStr = getDefinitionOne(num, inputNum)  #選擇的編號對應的解釋

    try:
        for example in exampleList[num]:
            exampStr += ("[" + str(count + 1) + "]" + "\n" +
                         exampleList[num][count][0] + "\n" +
                         exampleList[num][count][1] + "\n")
            count += 1
        outputStr += ("\n" + exampStr)
    except:
        if (inputNum > len(exampleList)):
            outputStr = "The number is too big!"
        else:
            outputStr = "[!] Unexcepted Error! Please email to the developer."

    return outputStr


pageURL = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crisis"

# run test
# getData(pageURL)
# print("defStr = " + getExample(3))
# print("getTitle = " + getTitle())
# print("defStr = " + getDefinitionAll())


def RunTest_Input(text):
    #輸入
    # pageURL = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crisis"
    pageURL = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/" + text
    #url 寫入 .json檔
    with open("dataBase.json", mode="r") as file:
        data = json.load(file)
        data["url"] = text
    with open("dataBase.json", mode="w") as file:
        json.dump(data, file)

    getData(pageURL)  #搜尋字典頁面
    isFinded = getIsPageFound()  #根據回傳內容判斷輸入文字是否找得到對應的字典頁面

    if isFinded == True:
        try:
            #傳送搜尋結果
            print("Your input: " + "event.message.text" + ", 搜尋結果: \n" +
                  getTitle() + "\n單字意思: \n" + getDefinitionAll())

        except:
            print("Error! Can't Find The Definition.")
    else:
        #找不到單字
        print("Page not found. Please enter the correct word.")
    global txtNum
    txtNum = input("Type Num: ")
    print("沒輸入數字之前會到這裡嗎")
    RunTest_Num(int(txtNum))


def RunTest_Num(textNum):
    #搜尋字典頁面
    pageURL = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/"
    with open("dataBase.json", mode="r") as file:
        data = json.load(file)
        url = data["url"]
        pageURL += url
    print("pageURL = " + pageURL)
    getData(pageURL)

    print("Your input: " + "event.message.text" + "\n\n" +
          "搜尋結果(example): \n" + getExample(textNum))
    isContinue = input("Type isContinue(Y/N): ")
    if isContinue == "y" or isContinue == "Y":
        txtStr = input("Type Str: ")
        RunTest_Input(txtStr)


# run test
# txtStr = input("Type Str: ")
# RunTest_Input(txtStr)

# count = 0
# while count < 3:
#     pageURL = "https://www.ptt.cc" + getData(pageURL)
#     print(pageURL)
#     count += 1
