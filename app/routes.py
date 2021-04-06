from flask import current_app as app
from flask import json, request,render_template
from .extensions import mydb
import datetime as dt

@app.route('/index', methods=["GET"])
def index(): # Returns UI for Actions on Repository
    l=[]
    my_col=mydb['items'].find()
    for i in my_col:
        if i['action']=='PR':
            l.append('"{}" submitted a Pull Request from "{}" to "{}"  on {}'.format(i["author"],i["from_branch"].split(':')[-1],i["to_branch"].split(":")[-1],convert(i["timestamp"])))
        if i['action']=='MR':
            l.append('"{}" merged "{}" to "{}"  on {}'.format(i["author"],i["from_branch"].split(':')[-1],i["to_branch"].split(":")[-1],convert(i["timestamp"])))
        if i['action']=='PUSH':
            l.append('"{}" pushed to "{}"  on {}'.format(i["author"],i["to_branch"],convert(i["timestamp"])))
    return render_template('index.html',l=l)

@app.route('/data/<counts>', methods=["GET"])
def data(counts): #Returns the updates to UI
    data={}
    if int(counts)<mydb['items'].find().count():
        my_col=mydb['items'].find()
        for j,i in enumerate(my_col[int(counts):]):
            if i['action']=='PR':
                data[j]='"{}" submitted a Pull Request from "{}" to "{}"  on {}'.format(i["author"],i["from_branch"].split(':')[-1],i["to_branch"].split(":")[-1],convert(i["timestamp"]))
            if i['action']=='MR':
                data[j]='"{}" merged "{}" to "{}"  on {}'.format(i["author"],i["from_branch"].split(':')[-1],i["to_branch"].split(":")[-1],convert(i["timestamp"]))
            if i['action']=='PUSH':
                data[j]='"{}" pushed to "{}"  on {}'.format(i["author"],i["to_branch"],convert(i["timestamp"]))
        return json.dumps(data)
    else:
        return {}
    

def convert(timestamp): #Conversion of timestamp to required format
    date,time=timestamp.split('T')[0],timestamp.split('T')[1]
    time=time.split(':')[0]+" "+time.split(":")[1]
    d_t=dt.datetime.strptime(date+" "+time,"%Y-%m-%d %H %M")
    day=d_t.strftime("%d")
    
    if day[0]!='1' and (day[1] in ['1','2','3']):
        if day[1]=="1":
            suffix="st"
        elif day[1]=="2":
            suffix="nd"
        else:
            suffix="rd"
    else:
        suffix="th"

    if day[0]=="0":
        day=day[1]

    date_time=d_t.strftime(" %B %Y-%I:%M %p UTC")
    return str(day+suffix+date_time)