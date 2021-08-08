import re


#輸入是句子 [A-Za-z]\s[A-Za-z]  e.g. hello world
def IsSentence(input):
    ptn = r"[A-Za-z]\s[A-Za-z]"
    n1 = re.search(ptn, input)
    if n1:
        # print("Input is Sentense: " + input)
        return True
    else:
        # print("Input is a character or word: " + input)
        return False


#輸入是中文 [A-Za-z]\s[A-Za-z]  e.g. hello world
def IsChinese(input):
    ptn = r"[\u4e00-\u9fa5]"
    n1 = re.search(ptn, input)
    if n1:
        print("Input is Chinese: " + input)
        return True
    else:
        print("Input is not Chinese: " + input)
        return False


## testcase

# IsSentence("hello World and goodbyE world")
# IsSentence("hello")
# IsChinese("hello")
# IsChinese("哈囉")
# IsChinese("哈囉hi")

# def TestInput(text):
#     try:
#         #輸入為數字整數
#         textNum = int(text)
#         print("Input is an integer number. Number = ", textNum)
#     except:

#         try:
#             #輸入為數字整數
#             textNum = float(text)
#             print("Input is an float number. Number = ", textNum)
#         except:
#             IsChinese(text)
# TestInput("hello")
# TestInput("哈囉")
# TestInput("哈囉hi")


#特殊功能 e.g. -profile
def IsFunction(input):
    ptn = r"^-"
    n1 = re.search(ptn, input)
    if n1:
        # print("Input is Funtion: " + input)
        return True
    else:
        # print("Input is a character or word: " + input)
        return False


def GetFunctionName(input):
    ptnSub = r'[-]'
    output = re.sub(ptnSub, '', input)
    return output
    # print("Funtion Name: " + output)


## testcase
# IsFunction("-profile")
# IsFunction("profile")
# GetFunctionName("-profile")
# GetFunctionName("profile")