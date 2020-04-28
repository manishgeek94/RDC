import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
from datetime import timedelta
import pandas as pd
import plotly
import plotly.express as pe
import plotly.graph_objects as g
from flask import Flask, render_template, redirect, url_for, flash, request, session
import pickle
import numpy as np
from RDC.forms import Loginform, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# app initiates here
app = Flask(__name__)
app.secret_key = 'mud123456789'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# config file gets read


class Application(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(50), unique=True)
    app_status = db.Column(db.Integer, nullable=True)
    app_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)


file = open("model.pkl", 'rb')
clf = pickle.load(file)
file.close()

with open("config.json", "r") as c:
    params = json.load(c)["params"]  # loading the parameters here from config file

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.img_file}')"


cases = 'https://raw.github.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deaths = 'https://raw.github.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

RENAMED_COLUMNS = {
    'Province/State': 'province_state',
    'Country/Region': 'country',
    'Lat': 'lat',
    'Long': 'long',
}


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Loginform()
    session.permanent = True
    if form.validate_on_submit():
        if form.email.data == params['admin_user'] and form.password.data == params['admin_password']:
            session['user'] = params['admin_user']
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/visits')
def visits():
    if 'user' in session and session['user'] == params['admin_user']:
        if 'visits' in session:
            session['visits'] = session.get('visits') + 1  # reading and updating session data
        else:
            session['visits'] = 1  # setting session data
        value = f"Total visits: {(session.get('visits'))}"
        return render_template('visits.html', params=params, visits=value)
    else:
        return redirect(url_for('login'))


@app.route('/')
def home():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('index.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc')
def rdcwc():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('rdcwc.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/about')
def about():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('about.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/services')
def services():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('services.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/contact')
def contact():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('contact.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/transition')
def transition():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('transition.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/rdc')
def rdc():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('rdc.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/pcload')
def pcload():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('pcload.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/webservices')
def webservices():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('webservices.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/distribution')
def distribution():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('distribution.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/eswtagging')
def eswtagging():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('eswtagging.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/coverage')
def coverage():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('coverage.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/elasticsearch')
def elasticsearch():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('elasticsearch.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/create-cmr&find-cmr')
def cfcmr():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('cfcmr.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/ci-translation-services')
def citranslationservices():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('citranslationservices.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/ierp')
def ierp():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('ierp.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/tgmeservices')
def tgmeservices():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('tgmeservices.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/tgme3')
def tgme3():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('tgme3.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/TWS')
def tws():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('tws.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/CCBT')
def ccbt():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('ccbt.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/digitalservices')
def digitalservices():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('digitalservices.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/salesConnect')
def salesConnect():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('salesConnect.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/TC')
def tc():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('tc.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/AWF')
def awf():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('awf.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/DPROP')
def dprop():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('dprop.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/FDB')
def fdb():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('fdb.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/LH')
def lh():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('lh.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/cl360')
def cl360():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('cl360.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/cl360/index-refresh')
def indexrefresh():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('indexrefresh.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/fs')
def fs():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('fs.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcwc/was-server-logs')
def wasserver():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('wasserverlog.html', params=params)
    else:
        return redirect(url_for('login'))


# @app.route('/rdcda1')
# def rdcda1():
#     if 'user' in session and session['user'] == params['admin_user']:
#         erdat = pd.read_csv('erdate.csv')
#         df = pd.DataFrame(erdat)
#         # df.plot(kind='bar', x='ERDAT', y='NO_OF_RECORDS')
#         plt.barh(df['ERDAT'], df['NO_OF_RECORDS'], color='g')
#         plt.xlabel('records_counts')
#         plt.ylabel('Create_date')
#         plt.title("RDC Customers Created")
#         plt.savefig('static/images/createR.png', bbox_inches='tight', dpi=1000)
#         plt.tight_layout()
#         create_img = True
#         return render_template('rdcda1.html', create_img=create_img, params=params)
#     else:
#         return redirect(url_for('login'))


@app.route('/rdcda0')
def rdcda0():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('rdcda0.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/rdcda1')
def rdcda1():
    if 'user' in session and session['user'] == params['admin_user']:
        df = pd.read_csv('static/RDC_Data/erdate.csv')

        gra = g.Figure(g.Scatter(x=df['ERDAT'], y=df['NO_OF_RECORDS'],
                                 name='records created'))

        gra.update_layout(title='Number of Customers created in March',
                          plot_bgcolor='rgb(230, 230,230)',
                          showlegend=True)

        # gra.show()

        graphJSON = json.dumps(gra, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('rdcda1.html', plot=graphJSON, params=params)
    else:
        return redirect(url_for('login'))


@app.route("/rdcda2")
def rdcda2():
    if 'user' in session and session['user'] == params['admin_user']:
        df = pd.read_csv('static/RDC_Data/Coverage_March.csv')
        gra1 = g.Figure(g.Scatter(x=df['COV_EFFDATE'], y=df['NO_OF_RECORDS'],
                                  name='coverage'))

        gra1.update_layout(title='Number of Customers got Coverage in March',
                           plot_bgcolor='rgb(230, 230,230)',
                           showlegend=True)

        graphJSON1 = json.dumps(gra1, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('rdcda2.html', plot=graphJSON1, params=params)
    else:
        return redirect(url_for('login'))


@app.route("/rdcda3")
def rdcda3():
    if 'user' in session and session['user'] == params['admin_user']:
        # idm_sources = pd.read_csv('static/RDC_Data/IDM_March_Sources.csv')
        # idm = pd.DataFrame(idm_sources)

        # Record_count = list(range(idm['RECORD_CREATED']))
        Record_count = [2300, 7240, 7600, 8982, 2977, 4101, 9519, 2901]
        add = 0
        for item in Record_count:
            add = add + item
        total_records = add
        # Record_count = [3, 15, 23, 76, 84, 87, 97, 206, 218, 2108, 2317, 2977, 4101, 9519, 35022, 72402, 175821, 245743, 396858, 546193, 898298]
        # Data_sources = list(range(idm['DATA_SOURCE']))
        Data_sources = ['ATLAS', 'CLOUD', 'CSA', 'DM', 'WHI', 'SFDC', 'WH', 'THIRDPARTY']
        # Data_sources = ['TWCB2C', 'INEWS', 'ATLAS', 'CSA', 'Siebel', 'TWCB2B', 'TWCVC', 'LIST ACQUIRED', 'WHI', 'SFDC', 'WH', 'THIRDPARTY', 'Sales Connect', 'DSW SAP', 'DSW SQO', 'CLOUD', 'LIST LEASED', 'Web Identity', 'IWM', 'GRP', 'DM']
        plt.pie(Record_count, labels=Data_sources, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})

        # plt.xlabel('Data_Source')
        # plt.ylabel('Count')
        plt.title("Record_Count/Data_Source")
        plt.savefig('static/images/idm_sources.png', bbox_inches='tight', dpi=1000)
        return render_template('rdcda3.html', total_records=total_records, params=params)
    else:
        return redirect(url_for('login'))


#
#
@app.route("/rdcda4")
def rdcda4():
    if 'user' in session and session['user'] == params['admin_user']:
        timestamp = pd.read_csv('static/RDC_Data/Update_March_ts.csv')
        tmp = pd.DataFrame(timestamp)
        indexes = np.arange(0, len(tmp['UPDATE_TIME_TODAY']), 1)
        plt.plot(indexes, tmp['RECORD_COUNT'], color='r', linestyle='--', marker='o')
        plt.ylabel('Count')
        plt.xlabel('Date')
        plt.title('Record/Day-MARCH')
        plt.grid(True)
        plt.savefig('static/images/update.png', bbox_inches='tight', dpi=1000)
        return render_template('rdcda4.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route("/covid19")
def covid19():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('covid19.html', params=params)
    else:
        return redirect(url_for('login'))


def df_from_csv(file_name):
    df = pd.read_csv(file_name)
    df = df.rename(columns=RENAMED_COLUMNS)
    date_cols = df.filter(regex='^\d+/\d+/\d+$').columns
    df = pd.melt(df, id_vars=['province_state', 'country', 'lat', 'long'], value_vars=date_cols, var_name='date',
                 value_name='cases')
    df.replace(to_replace=1, value=-1)

    return df[['date', 'cases', 'province_state', 'country', 'lat', 'long']]


""" df_cases is the main dataframe which has all the values """
# df_cases = df_from_csv(cases)
# df_deaths = df_from_csv(deaths)
# df_cases['deaths'] = df_deaths['cases']
# # df_final = df_cases.append(df_deaths['cases'])
# df_cases.to_csv('output.csv', index=False)
# # print(df_final)


''' reading the data from output.csv '''
data = pd.read_csv('output.csv', parse_dates=['date'])
# print(data.head())


''' recent data '''
recent_data = data[data['date'] == data['date'].max()]
# print(recent_data)

''' max death'''
max_death = data[data['deaths'] == data['deaths'].max()].reset_index(drop=True).drop(['lat', 'long'], axis=1)
# print(max_death)


''' total cases and deaths group by counties'''
affected_countries = recent_data.groupby('country').sum().reset_index()
final = affected_countries.drop(['lat', 'long'], axis=1)


@app.route('/covidda')
def covidda():
    if 'user' in session and session['user'] == params['admin_user']:
        figure = g.Figure(data=g.Choropleth(
            locations=affected_countries['country'],
            locationmode='country names',
            z=affected_countries['cases'],
            colorscale='reds',
            autocolorscale=True,
            reversescale=False,
            marker_line_color='black',
            marker_line_width=0.5,
            colorbar_title='Confirmed Cases',
        ))

        figure.update_layout(width=1500,
                             height=600,
                             title_text='Countries affected by Coronavirus (COVID-19)',
                             geo=dict(
                                 showframe=False,
                                 showcoastlines=True,
                                 projection_type='equirectangular',

                             ),
                             annotations=[dict(
                                 x=0.50,
                                 y=0.2,
                             )]
                             )
        graphJSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('coviddata.html', plot=graphJSON, params=params)
    else:
        return redirect(url_for('login'))


''' plotly  data '''
data_spreading = data.groupby(['date', 'country', 'deaths']).max().drop(['lat', 'long'], axis=1).reset_index()
data_spreading['count'] = data_spreading['cases'].pow(0.1).fillna(0)
data_spreading['date'] = pd.to_datetime(data_spreading['date']).dt.strftime('%m/%d/%Y')


@app.route('/covidt')
def covidt():
    if 'user' in session and session['user'] == params['admin_user']:
        figure_world = pe.scatter_geo(data_spreading,
                                      locations=data_spreading['country'],
                                      locationmode='country names',
                                      color='cases',
                                      hover_name="country",
                                      size='count',
                                      animation_frame="date",
                                      projection="natural earth",
                                      title='Spreading of Coronavirus disease (COVID-19) w.r.t time',
                                      width=1500, height=700)

        graphJSON = json.dumps(figure_world, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('covidwtdata.html', plot=graphJSON, params=params)
    else:
        return redirect(url_for('login'))


#
# @app.route('/covid_pre', methods=['GET', 'POST'])
# def covid_pre():
#     if 'user' in session and session['user'] == params['admin_user']:
#         if request.method == 'POST':
#             dict = request.form
#             fever = float(dict['fever'])
#             age = int(dict['age'])
#             body_pain = int(dict['body_pain'])
#             runny_nose = int(dict['runny_nose'])
#             diff_breath = int(dict['diff_breath'])
#             # code for inference
#             input_features = [fever, age, body_pain, runny_nose, diff_breath]
#             virus_prob = clf.predict_proba([input_features])[0][1]
#             print(virus_prob)
#             return render_template('show_proba.html', params=params, inf=round(virus_prob * 100))
#         return render_template('covid_pre.html', params=params)
#     else:
#         return redirect(url_for('login'))


@app.route('/who')
def who():
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('who.html', params=params)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))


@app.route("/status_app", methods=['GET', 'POST'])
def appstat():
    # if 'user' in session and session['user'] == params['admin_user']:

    applications = Application.query.all()
    if request.method == 'POST':
        for app in applications:
            application_status = request.form.get(app.app_name)
            print(application_status)
            if app.app_status == application_status:
                pass
            else:
                app.app_status = application_status
                app.app_date = datetime.utcnow()
                db.session.commit()

        applications = Application.query.all()
        return redirect('status')

    return render_template('status_apps.html', applications=applications, params=params)


@app.route("/status", methods=['GET', 'POST'])
def app_current_stat():
    applications = Application.query.all()
    return render_template('updated_status.html', applications=applications, params=params)


if __name__ == '__main__':
    app.run(debug=True)
