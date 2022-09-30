import datetime
import pickle
from flask import jsonify
from flask import Flask, request, redirect
import flask
import random
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from skfuzzy import control as ctrl
from flask_cors import CORS

app = Flask(__name__)
app.debug = True

CORS(app)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)


# Import for Migrations
from flask_migrate import Migrate, migrate
 
# Settings for migrations
migrate = Migrate(app, db)

green_time = pickle.load(open('./green_time.pkl', 'rb'))

# function to render index page
@app.route('/')
def index():
    return render_template('simulation2.html')


@app.route('/traffic', methods=['POST'])
def traffic():
    global green_time

    emv1 = int(flask.request.form.get('emv1', 0))
    emv2 = int(flask.request.form.get('emv2', 0))
    emv3 = int(flask.request.form.get('emv3', 0))
    emv4 = int(flask.request.form.get('emv4', 0))

    density1 = flask.request.form.get('density1', 0)
    density2 = flask.request.form.get('density2', 0)
    density3 = flask.request.form.get('density3', 0)
    density4 = flask.request.form.get('density4', 0)
    
    #inputs
    cur_lane = int(flask.request.form.get('cur_lane', random.randint(0, 3)))        #default = random
    cur_time = float(flask.request.form.get('cur_time', random.randint(25, 35)))     #default = random
    
    resp_time = flask.request.form.get('resp_time', None)
    print(resp_time)
    interval = random.uniform(1,3)
    if resp_time is not None:
        interval = datetime.datetime.now() - datetime.datetime.strptime(resp_time, '%Y-%m-%d %H:%M:%S')
        interval = interval.total_seconds()
        
    lane_density = None

    emv = [ int(emv1),
            int(emv2),
            int(emv3),
            int(emv4) ]


    lane_density = [float(density1),
                float(density2),
                float(density3),
                float(density4) ]

    emergency_current=0
    emergency_other =0
    if cur_lane!=4:
        #if the ev present in current lane
        emergency_current = emv[cur_lane]           
        #if the ev present in any other lane
        emergency_other = emv[(cur_lane+1)%4] or emv[(cur_lane+2)%4] or emv[(cur_lane+3)%4]
    else:
        emergency_other=emergency_other or emv[(cur_lane)%4]


    if emergency_other:
        cur_time = 0
    else:
        if cur_lane==4:
            cur_time -= interval
        else:
            green_time.input['current'] = lane_density[cur_lane]
            green_time.input['others'] = (sum(lane_density)-lane_density[cur_lane])/3
            green_time.compute()

    if not emergency_current:
        if cur_lane!=4:
            cur_time = min(cur_time-interval,green_time.output['green'])
    else:
        cur_time = float(flask.request.form.get('cur_time', random.randint(0, 3)))  

    resp=None
    

    if cur_time<=0:
        resp = {
            "cur_lane":(cur_lane+1)%5,
            "cur_time":45,
            "resp_time":datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            }
        if cur_lane==3:
            resp['cur_time']=12
    else:
        resp = {
            "cur_lane":cur_lane,
            "cur_time":round(cur_time,2),
            "resp_time":datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            }
    
    return jsonify(resp)


if __name__ == '__main__':
    app.run()




# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade