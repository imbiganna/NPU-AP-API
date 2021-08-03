import requests
import lxml
from bs4 import BeautifulSoup

headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

def login(uid,pwd):

    mySession:requests = requests.session()
    mySession.get("https://as2.npu.edu.tw/npu/index.html")
    myLoginPayload = {
        "uid": uid,
        "pwd": pwd
    }

    loginSystem = mySession.post("https://as2.npu.edu.tw/npu/perchk.jsp", data=myLoginPayload, timeout=5,headers=headers)
    if loginSystem.text.find("不正確") > 0 :
        return {"error" : '帳號密碼錯誤'}

    soup = str(BeautifulSoup(loginSystem.text, 'html.parser').find_all('script')[0])
    infoStart = soup.find('innerHTML') + 10
    infoEnd = soup.find('window.parent.document.getElementById("Menufrm").cols = "215,*";')
    myStr = soup[infoStart:infoEnd]
    infoString = BeautifulSoup(myStr, 'html.parser').find_all('span')

    loginCookie = mySession.cookies.get_dict()

    returnPayload = {
        "cookie" : loginCookie,
        "stdid" : uid,
        "grade" : infoString[0].text,
        "name"  : infoString[2].text,
        "myClass" : infoString[1].text
    }   

    return returnPayload


def getScore(cookie) :
    mySession = requests.session()
    data = {
        "yms" : "109,1",
        "arg01" : "109",
        "arg02" : "2"
    }
    get = mySession.post("https://as2.npu.edu.tw/npu/ag_pro/ag008.jsp",data = data, timeout=5 ,cookies = cookie,headers=headers)
    if get.text.find('教學評量') > 0:
        return {"error" : "未填寫教學評量"}

    soup = BeautifulSoup(get.text, 'html.parser')
    rowsa = soup.find_all('td')
    i = 0
    scoreJson = {
        "value" : [

        ],
        "avgScore" : "",
        "rank" : "",
        "conduct" : ""
    }
    maxrow = len(rowsa)
    for row in rowsa:
        i += 1
        if row == rowsa[maxrow -1] or i >= maxrow -1:
            break
        if i >= 15:
            tempScore = {
                "courseName" : rowsa[i].text,
                "midScore" : rowsa[i+1].text,
                "finalScore" : rowsa[i+2].text
            }
            i += 3
            scoreJson["value"].append(tempScore)
    lastScore = rowsa[maxrow-1].text.split('\u3000')
    scoreJson["avgScore"] = lastScore[2]
    scoreJson["rank"] = lastScore[4]
    scoreJson['conduct'] = lastScore [0]
    return scoreJson

def getReward(cookie):
    mySession = requests.session()
    data = {
        "yms" : "109,2",
        "arg01" : "109",
        "arg02" : "2"
    }
    get = mySession.post("https://as2.npu.edu.tw/npu/ak_pro/ak010.jsp",data = data, timeout=5 ,cookies = cookie,headers=headers)
    soup = BeautifulSoup(get.text, 'html.parser')
    rowsa = soup.find_all('td')
    if rowsa[22].text == '\xa0':
        return{
            "status" : "沒有獎懲紀錄"
        }
    rewardJson = {
        "value" : [

        ],
        "status": "Seccuss"
    }
    i = 0
    maxrow = len(rowsa)
    for row in rowsa:
        i += 1
        if row == rowsa[maxrow -1] or i >= maxrow -1:
            break
        if i >= 22:
            tempReward = {
                "date" : rowsa[i].text,
                "category" : rowsa[i+1].text,
                "count" :rowsa[i+2].text,
                "info" :rowsa[i+3].text
            }
            i += 3
            rewardJson["value"].append(tempReward)
    return rewardJson


def getNoShow(cookie):
    mySession = requests.session()
    data = {
        "yms" : "109,2",
        "arg01" : "109",
        "arg02" : "2"
    }
    get = mySession.post("https://as1.npu.edu.tw/npu/ak_pro/ak002_01.jsp",data = data, timeout=5 ,cookies = cookie,headers=headers)
    if get.text.find('查無') > 0:
        return {"error" : "查無缺曠資料"}
    soup = BeautifulSoup(get.text, 'html.parser')
    rowsa = soup.find_all('td')
    noShowJson = {
        "value" : [

        ],
        "status": "Seccuss"
    }
    i = 0
    maxrow = len(rowsa)
    for row in rowsa:
        i += 1
        if row == rowsa[maxrow -1] or i >= maxrow -1:
            break
        if i >= 21:
            tempNoShow = {
                "id" : rowsa[i].text,
                "date" : rowsa[i+1].text,
                "course1" : rowsa[i+4].text,
                "course2" : rowsa[i+5].text,
                "course3" : rowsa[i+6].text,
                "course4" : rowsa[i+7].text,
                "course5" : rowsa[i+8].text,
                "course6" : rowsa[i+9].text,
                "course7" : rowsa[i+10].text,
                "course8" : rowsa[i+11].text,
                "course9" : rowsa[i+12].text,
                "course10" : rowsa[i+13].text,
                "course11" : rowsa[i+14].text,
                "course12" : rowsa[i+15].text,
                "course13" : rowsa[i+16].text,
                "course14" : rowsa[i+17].text,
                "course15" : rowsa[i+18].text
            }
            i += 18
            noShowJson["value"].append(tempNoShow)
    return noShowJson


def getCourse(cookie) :

    timetable = ["No1","No2","No3","No4","No5","No6","No7","No8","No9","No10","No11","No12","No13","No14"]
    week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    mySession = requests.session()
    data = {
        "yms" : "109,1",
        "arg01" : "109",
        "arg02" : "2"
    }
    get = mySession.post("https://as1.npu.edu.tw/npu/ag_pro/ag001.jsp",data = data, timeout=5 ,cookies = cookie,headers=headers)

    soup = BeautifulSoup(get.text, 'html.parser')
    rowsa = soup.find_all('td')

    courseJson = {
        "value" : [

        ],
        "status": "Seccuss"
    }

    i = 13
    for time in timetable:
        tempWeek = {time:{

            }
        }
        for weekName in week:
            i+=1

            courseNameFirst = str(rowsa[i]).find('title')+13
            myString = str(rowsa[i])[courseNameFirst::]
            endCourseString = myString.find('</a')
            courseName = myString[:endCourseString]
            if courseName.find('bgcolor') > 0:
                courseName = " "

            teacherNameStart = myString[myString.find("/>") +2::]
            teacherNameEnd = teacherNameStart.find('<')
            teacherName = teacherNameStart[:teacherNameEnd]
            if teacherName.find('bgcolor') > 0:
                teacherName = " "

            startRoomID = teacherNameStart.find('>') +1
            endRoomID = teacherNameStart.find('td')-3
            roomName = teacherNameStart[startRoomID:endRoomID]

            tempCourse = {
                "courseName" : courseName,
                "teacher"   : teacherName,
                "room"      : roomName
            }
            tempWeek[time][weekName]=tempCourse
        i+=1
        courseJson["value"].append(tempWeek)

    return courseJson

def checkStatus():
    request = requests.get('http://as2.npu.edu.tw/npu')
    if request.status_code == 200:
        return {"as2" : "ON"}
    else:
       return {"as2" : "DOWN"}


def newsList():
    mySession = requests.session()
    newsJson = []
    for page in range(3):
        get = mySession.get("https://www.npu.edu.tw/latestevent/Index.aspx?Parser=9,3,23,,,,,,,,"+str(page))
        soup = BeautifulSoup(get.text, 'html.parser')
        rowsa = soup.find_all('span')
        i = 9
        for _ in range(10):
            tempData = {
                "newsTitle" : rowsa[i].text,
                "newsTeam"  : rowsa[i+1].text,
                "newsDate"  : rowsa[i+3].text,
                "newsURL"   : "https://www.npu.edu.tw/latestevent/"+rowsa[i].find(name='a').get('href')
            }
            newsJson.append(tempData)
            i+=4
    return newsJson


print("API...INITED")
