#Replaced ttc -> ttp
#Replaced TTC_URL -> TTP_URL

Total_images = 1200 

from distutils.log import debug
import os
import pathlib
import re
import requests
import random
import json
from pip._vendor import cachecontrol
from flask import Flask, render_template, request, url_for, session, abort, redirect, send_from_directory
import sqlite3
from flask_session import Session
from google.oauth2 import id_token
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
import os
import stats as st							#Commented this as we are not using it anymore
from datetime import timedelta
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# os.environ['USE_SESSION_FOR_NEXT']='1'

app = Flask(__name__, static_url_path='/static',static_folder="static")
app.config['SESSION_PERMANENT']=True
app.config['SESSION_TYPE']="filesystem"
Session(app)

HOST_URL = "http://127.0.0.1:5000"
TTP_URL = "/ttp"
GENERATED = 1
REAL = 2
# db_table_structure = "(uid,email_id,given_name,family_name,name,user_img,occupation,real_start,real_inc,real_cur,real_count,fake_start,fake_inc,fake_cur,fake_count,R0,F0,R1,F1,R2,F2,R3,F3,R4,F4,R5,F5,total,image_evaluated,image_skipped,rand_num,class)"    #Replaced recipe_evaluated --> image_evaluated, image_skipped--> image_skipped, also added class as an extra columnn class
user_db_structure = "(uid ,email ,name, random_counter, total_count,total_skip,total_pos,total_real)"
user_eval_structure = "(uid,imgId,fake_or_real,emotion)"
# yaha se start h

app.secret_key = "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"                                                  #Changed this to our google auth creds
app.config['SESSION_PERMANENT']=True
app.config['SESSION_TYPE']="filesystem"
Session(app)
GOOGLE_CLIENT_ID = "478795011834-r6h2opts3roa2ojb7bpc6uuh1n60srf2.apps.googleusercontent.com"           #Changed this to our google auth creds
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=HOST_URL+TTP_URL+"/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper


@app.route(TTP_URL+"/")
def main_page():
    print(session.get('email_id'))
    if session.get('email_id') != None:
        return redirect(TTP_URL+"/protected_area")
    return redirect(TTP_URL+"/profile")


@app.route(TTP_URL+"/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route(TTP_URL+"/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session['email_id'] = id_info.get("email")
    session['given_name'] = id_info.get("given_name")
    session['family_name'] = id_info.get("family_name")
    session['user_img'] = id_info.get("picture")
    return redirect(TTP_URL+"/protected_area")


@app.route(TTP_URL+"/logout")
def logout():
    session.clear()
    return redirect(TTP_URL+"/profile")


@app.route(TTP_URL+"/profile")
def profile():
    return render_template('login.html')


@app.route(TTP_URL+"/protected_area")
@login_is_required
def protected_area():
    con2 = sqlite3.connect('data.db')        #Replaced generated_recipes --> turing_test_image_DB
    cur2 = con2.cursor()
    cur2.execute(f"SELECT name FROM user WHERE uid = '{session['google_id']}'")
    res = cur2.fetchone()
    con2.close()
    if res == None:
        return profile_occupation(session['name'].split(' ')[0])
    else:
        return index()


@app.route(TTP_URL+"/profile_occupation")
def profile_occupation(name):
    con2 = sqlite3.connect('data.db')				#Replaced generated_recipes --> turing_test_image_DB
    cur2 = con2.cursor()
    print("Before insert operation")
    cur2.execute(f"INSERT INTO user {user_db_structure} VALUES('{session['google_id']}','{session['email_id']}','{session['name']}','{random.randint(0,Total_images-1)}',0,0,0,0)")  #added '{request.form.get('class_type')}' as an extra column is being inserted from UI
    print("After insert operation")
    con2.commit()
    con2.close()
    return render_template('occupation.html', name=name)


@app.route(TTP_URL+"/occupation_adder", methods=["GET", "POST"])
def occupation_adder():
    return about()

@app.route(TTP_URL+"/about", methods=["GET", "POST"])
def about():
    return render_template('help.html')
#added this here for classes type for global variables
org_tot_count = 0
gen_tot_count = 0




@app.route(TTP_URL+"/index")
def index():
    con2 = sqlite3.connect('data.db')					#Replaced generated_recipes --> turing_test_image_DB
    cur2 = con2.cursor()
    cur2.execute(f"SELECT * FROM user WHERE uid = '{session['google_id']}'")
    # print(cur2.fetchone())
    ress = tuple(cur2.fetchone()) 
    if ress[4] + ress[5] >= Total_images:
        return render_template('statistics.html', name = session['given_name']+ ",You have evaluated all the images", image_evaluated=ress[4], ress = ress)
    imgid = (ress[3] % Total_images) + 1 
    cur2.execute(f"SELECT * FROM Images WHERE imgId = '{ress[3]}' ")
    ress2 = tuple(cur2.fetchone()) 
    img_path = ress2[1]
    print("IMAGEEEEEEEEEEEEEE" , img_path)
    data = []
    con2.commit()
    con2.close()

    
    #data[1] = data[1].split('|')					#data[2] -> data[1]
    print(data)
    # img_path = "data_images/generated_images/"+ img_path +'.png'
    # print(img_path)
    

    return render_template('index.html', data=data, img_path = img_path , name=session['given_name'],imgid=imgid)



@app.route(TTP_URL+'/sbt', methods=['POST'])
def sbt():
    # if request.method == 'POST':
    #     output = request.get_json()
    #     # This is the output that was stored in the JSON within the browser
    #     print(output)
    #     print(type(output))
    #     print("submit clicked")

    #     string =""
    #     if output['image_val']==f"{REAL}":														#Replaced recp_val --> image_val
    #         string+='R'
    #     else :
    #         string+='F'
    #     string+=f"{output['button_val']}"
    
    # print(request.POST.json())
    print(request.get_json())
    
    request_data=request.get_json()
    try:
        fake_or_real,emotion=int(request_data['button_val']),int(request_data['button_2_val'])
    except Exception as ee:
        return skip()
    
    con2 = sqlite3.connect('data.db')				#Replaced generated_recipes --> turing_test_image_DB
    cur2 = con2.cursor()
    cur2.execute(f"SELECT * FROM user WHERE uid = '{session['google_id']}'")
    ress = tuple(cur2.fetchone()) 
    imgid = (ress[3] % Total_images) + 1 
    print("Before insert operation")
    cur2.execute(f"INSERT INTO user_evaluation {user_eval_structure} VALUES('{session['google_id']}','{imgid}','{fake_or_real}',{emotion})")  #added '{request.form.get('class_type')}' as an extra column is being inserted from UI
    cur2.execute(f"Update user set random_counter = random_counter + 1 WHERE uid = '{session['google_id']}'")
    cur2.execute(f"Update user set total_count = total_count + 1 WHERE uid = '{session['google_id']}'")

    cur2.execute(f"SELECT * FROM Images WHERE imgId = '{ress[3]}' ")
    ress2 = tuple(cur2.fetchone()) 
    print(ress2)
    if ress2[2] == 'real':
        cur2.execute(f"Update user set total_real = total_real + 1 WHERE uid = '{session['google_id']}'")
    if ress2[3] == 1:
        cur2.execute(f"Update user set total_pos = total_pos + 1 WHERE uid = '{session['google_id']}'")


    con2.commit()
    con2.close()

    return "1"

@app.route(TTP_URL+'/skip',methods=['POST'])
def skip():
    con2 = sqlite3.connect('data.db')										#Replaced generated_recipes --> turing_test_image_DB
    cur2 = con2.cursor() 
    cur2.execute(f"Update user set random_counter = random_counter + 1 WHERE uid = '{session['google_id']}'")
    cur2.execute(f"Update user set total_skip = total_skip + 1 WHERE uid = '{session['google_id']}'")
    con2.commit()
    con2.close()
    return "1"

@app.route(TTP_URL+'/stats')
def stats():
    con = sqlite3.connect('data.db')											#Replaced generated_recipes --> turing_test_image_DB
    curr = con.cursor()
    lst = []
    curr.execute(f"SELECT * FROM user WHERE uid = '{session['google_id']}'")
    ress = tuple(curr.fetchone())
    # image_evaluated = tuple(curr.fetchone())[4]
    return render_template('statistics.html', name = session['given_name'], image_evaluated=ress[4], ress = ress)


    
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    from waitress import serve
    app = app = Flask(__name__)
    serve(app, host="0.0.0.0", port=5000)
