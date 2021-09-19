from flask import Flask ,session
from flask_socketio import SocketIO, emit
import json
from hacker_bot_model import predict_best_match 
# import poc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app,cors_allowed_origins='*')
SESSION_TYPE = 'redis'

f = open('course_branch.json',encoding="utf8")
course_branch = json.load(f)

f = open('branch_fees.json',encoding="utf8")
branch_fees = json.load(f)

all_al = dict(branch_fees)
all_branches=list(branch_fees.keys())
all_courses=list(course_branch['courses'].keys())



@app.route('/')
def index():
    return 200,{'success':True}
    # return render_template('index.html')

@socketio.on('start')
def handleMessage(msg):
    session['is_last_res']=False

    emit("bot-message",{'message':"Hii! I am a chatbot developed by Deja Vu in Hackathon 1.0 "})
    emit("bot-message",{'message':"Do you want to know about Admissions ?",'isOption' : True,'options':['Yes','No']})

def emit_message(a, select_data):
    #print(a)
    if a['select']:
        if select_data in all_courses:
            emit("bot-message",{'message':f"Here are the branches provided by us on program {select_data} .", 'isOption' : True,'options': course_branch['courses'][select_data]['branch']})
        elif select_data in all_branches:
            intake=list(branch_fees[select_data])
            intake.remove('branch_importance')
            emit("bot-message",{'message':f"Here are the branches provided by us on program {select_data } {branch_fees[select_data]['branch_importance']} . : ",'isOption' : True,'options': intake})
            session['branch'] = select_data
        elif select_data.lower() == 'yes':
            # print(session['is_last_res'])
            if session['is_last_res']: 
                req,res,ratio =predict_best_match(session['last_res'])
                print(ratio)
                session['is_last_res']=False
                emit("bot-message",{'message':f" {res}",'isOption' : False})
                return True
            emit("bot-message",{'message':"Please select any program : ",'isOption' : True,'options':list(all_courses)})
        elif select_data.lower() == 'no' or select_data=='No':
            emit("bot-message",{'message':f" If you have any queries please ask.",'isOption' : False})
        else:
            if a['select_data']=='Fees':
                Fees_session=all_al[session['branch']]['Fees']
                emit("bot-message",{'message':f" Fees for {session['branch']} per year {Fees_session}",'isOption' : False,'options':list(all_courses)})
                emit("bot-message",{'message':f" If you have any queries please ask.",'isOption' : False})
            elif a['select_data']=='Intake' :
                intakes_branch=all_al[session['branch']]['Intake']
                emit("bot-message",{'message':f" Intake for {session['branch']} is {intakes_branch} per year.",'isOption' : False,'options':list(all_courses)})
                emit("bot-message",{'message':f" If you have any queries please ask.",'isOption' : False})
            else:
                emit("bot-message",{'message':f" If you have any queries please ask.",'isOption' : False})

    elif a['message'].lower() == 'yes':
        a['select']=True
        a['message']=select_data
        emit_message(a,select_data)
    elif 'program' in a['message'].lower().split() :
        emit("bot-message",{'message':"Please select any program : ",'isOption' : True,'options':list(all_courses)})
        # emit("bot-message",{'message':f"Here are the branches provided by us on program {select_data} .", 'isOption' : True,'options': course_branch['courses'][select_data]['branch']})
    else:
        inp = a['message']
        req,res,ratio =predict_best_match(inp)
        print(ratio)
        if req:
            emit("bot-message",{'message':f'''{res}''','isOption' : False})
        else:
            session['is_last_res']=True;session['last_res']=res
            emit("bot-message",{'message':f"Sorry, I didn't get you. ",'isOption' : False})
            emit("bot-message",{'message':f'Did you mean, {str(res)}','isOption' : True,'options':['Yes','No']})
            # emit("bot-message",{'message':"Sorry , how may I help you today ?",'isOption' : False,'options':list(all_courses)})
    return True

@socketio.on('client-message')
def abc(msg):
    a = msg
    if len(a['message']) == 0:
        select_data=a['select_data']
    else:
        select_data=a['message']
    emit_message(a,select_data)
    
if __name__ == '__main__':
	socketio.run(app)