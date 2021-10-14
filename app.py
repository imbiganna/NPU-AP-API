from flask import Flask,jsonify,request,render_template
from flask_jwt_extended import *
from flask_cors import CORS

import api
import datetime

jwt = JWTManager()
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'biganna326'
jwt.init_app(app)
app.config['JSON_AS_ASCII'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers','query_string']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=60)
app.config['JWT_QUERY_STRING_NAME'] = 'token'
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/api/score',methods=['POST','GET'])
@jwt_required()
def score():
    myCookie = get_jwt_identity()['cookie']
    myScore = api.getScore(myCookie)
    return jsonify(myScore)
    #return jsonify(api.getScore(tempcookie))

@app.route('/api/info', methods=['GET', 'POST'])
@jwt_required()
def getInfo(): 
    myInfo = get_jwt_identity()
    del myInfo['cookie']
    return jsonify(myInfo)


@app.route('/api/login',methods=['POST','GET'])
def login():
    uid = request.values.get('uid')
    pwd = request.values.get('pwd')
    if uid == None or pwd == None:
        return jsonify({"error" : '帳號或密碼為空'})
    loginPayload = api.login(uid,pwd)
    if 'error' in loginPayload:
        return jsonify(loginPayload)
    
    access_token = create_access_token(identity=loginPayload)
    return jsonify({'token': access_token,
                    'error' : 'noError'})

@app.route('/api/reward',methods=['POST','GET'])
@jwt_required()
def getReward():
    myCookie = get_jwt_identity()['cookie']
    myReward = api.getReward(myCookie)
    return jsonify(myReward)

@app.route('/api/noshow',methods=['POST','GET'])
@jwt_required()
def getNoShow():
    myCookie = get_jwt_identity()['cookie']
    myNoShow = api.getNoShow(myCookie)
    return jsonify(myNoShow)

@app.route('/api/coursetable',methods=['POST','GET'])
@jwt_required()
def getMyCourse():
    myCookie = get_jwt_identity()['cookie']
    myCourse = api.getCourse(myCookie)
    return jsonify(myCourse)

@app.route('/api/getGreaduate',methods=['POST','GET'])
@jwt_required()
def getMyGread():
    myCookie = get_jwt_identity()['cookie']
    numberOf = request.values.get('numberOf')
    myGread = api.getGreaduate(myCookie,numberOf)
    return jsonify(myGread)


@app.route("/api/status",methods=['GET'])
def checkStatus():
    return jsonify(api.checkStatus())

@app.route("/api/newsList",methods=['GET'])
def getNews():
    print(request.remote_addr + "-LOGIN AND GET NEWS!!")
    return jsonify(api.newsList())

@app.route("/test/getCList",methods=['get'])
@jwt_required()
def getCList():
    myCookie = get_jwt_identity()['cookie']
    getList = api.requestLeaveCanList(myCookie)
    return getList

@app.route("/api/ckeckVersion", methods=['GET'])
def getVersion():
    return jsonify({"iOS" : "1.21" , "URL" : "https://apps.apple.com/tw/app/tw/id1580528288"})
