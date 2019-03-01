from flask import Flask, render_template
from flask import request
import psycopg2
import re
import base64
import os, time, http.client
import requests
import urllib.request
import threading
import time

app = Flask(__name__)

def run_check():
    threading.Timer(60.0, run_check).start()
    SITES = []
    SITE_ID = {}
    try:
        conn = psycopg2.connect(host="localhost",database="websitechecker", user="postgres", password="")
        """
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        """
        cur = conn.cursor()
        query = "SELECT * from websites"
        cur.execute(query)
        results = cur.fetchall()
        #"""
        for res in results:
            #print(res)
            SITES.append(res[0])
            SITE_ID[res[0]] = res[1]
        #"""
        conn.close()
    except Exception as e:
        print(e)    
    for site in SITES:
        sheraa = site
        if sheraa == "":
            break
        global response_status
        response_time = 0
        try:
            # conn = http.client.HTTPSConnection(site+'/?', timeout=10)
            # conn.request("HEAD", "/?")
            # response = conn.getresponse()
            response = requests.get(sheraa);
            if response.status_code != 200:
                response_status = 'DOWN'	
            else:
                response_time = requests.get(sheraa).elapsed.total_seconds()
                response_status = 'OK'
            print (site+" " + str(response.status_code)+" " + str(response_status)+" " +str(response_time))
            
            try:
                conn = psycopg2.connect(host="localhost",database="websitechecker", user="postgres", password="")
                """
                DATABASE_URL = os.environ['DATABASE_URL']
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                """
                cur = conn.cursor()
                query = "INSERT INTO websiteinfo (site_name, site_id, response_code, response_type, response_time) VALUES (%s, %s,%s,%s,%s)"
                values = (sheraa, SITE_ID[sheraa], str(response.status_code), str(response_status), str(response_time))
                cur.execute(query, values)
                conn.commit()
                count = cur.rowcount
                print(count)
                """
                filelist = []
                for res in results:
                    filelist.append(res[1])
                    print(res)
                    count+=1
                """
                conn.close()
            except Exception as e:
                print(e)
            conn.close()

        except Exception as e:
            print (site+" "+str(e))
 
run_check()

@app.route('/')
def runpy():
    global datacount
    filelist = []
    print("reloading....")
    return render_template('index.html')

@app.route('/',methods=['post'])
def form_post():
    global sitename
    sitename = request.form['addr']
    print(sitename)
    if(sitename != ""):
        try:
            conn = psycopg2.connect(host="localhost",database="websitechecker", user="postgres", password="")
            """
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            """
            cur = conn.cursor()
            query = "INSERT INTO websites (site_name, monitoring_from) VALUES (%s, current_timestamp)"
            values = (sitename,)
            cur.execute(query, values)
            conn.commit()
            count = cur.rowcount
            print(count)
            """
            filelist = []
            for res in results:
                filelist.append(res[1])
                print(res)
                count+=1
            """
            conn.close()
        except Exception as e:
            print(e)
    try:
        conn = psycopg2.connect(host="localhost",database="websitechecker", user="postgres", password="")
        """
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        """
        cur = conn.cursor()
        query = "SELECT * from websites"
        cur.execute(query)
        results = cur.fetchall()
        #"""
        for res in results:
            print(res)
        #"""
        conn.close()
    except Exception as e:
        print(e)
    return render_template('dashboard.html', results=results)

@app.route('/dashboard')
def dashboard():
    print("dashboard....")
    try:
        conn = psycopg2.connect(host="localhost",database="websitechecker", user="postgres", password="")
        """
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        """
        cur = conn.cursor()
        query = "SELECT * from websites"
        cur.execute(query)
        results = cur.fetchall()
        #"""
        for res in results:
            print(res)
        #"""
        conn.close()
    except Exception as e:
        print(e)
    return render_template('dashboard.html', results=results)

@app.route('/dashboard/<int:website_id>')
def websiteinfo(website_id):
    print(website_id)
    global website_name
    print("dashboard....")
    try:
        conn = psycopg2.connect(host="localhost",database="websitechecker", user="postgres", password="")
        """
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        """
        cur = conn.cursor()
        query = "SELECT * from websiteinfo WHERE site_id = %s"
        values = (website_id,)
        cur.execute(query, values)
        results = cur.fetchall()
        #"""
        for res in results:
            website_name = res[0]
        #"""
        conn.close()
    except Exception as e:
        print(e)
    return render_template('dashboard-websiteinfo.html', results=results, website_name=website_name)

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
